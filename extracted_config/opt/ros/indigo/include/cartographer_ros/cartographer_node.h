#include "cartographer/mapping/map_builder.h"
#include "cartographer_ros/node.h"
#include "cartographer_ros/node_options.h"
#include "cartographer_ros/ros_log_sink.h"
#include "gflags/gflags.h"
#include "tf2_ros/transform_listener.h"
#include <tf/transform_listener.h>
#include "cartographer/transform/rigid_transform.h"
#include <std_msgs/Bool.h>
#include <nav_msgs/Path.h>
#include <geometry_msgs/PoseWithCovarianceStamped.h>
#include "cartographer_ros/msg_conversion.h"

DEFINE_string(configuration_directory, "",
              "First directory in which configuration files are searched, "
              "second is always the Cartographer installation to allow "
              "including files from there.");
DEFINE_string(configuration_basename, "",
              "Basename, i.e. not containing any directory prefix, of the "
              "configuration file.");
DEFINE_string(load_state_filename, "",
              "If non-empty, filename of a .pbstream file to load, containing "
              "a saved SLAM state.");
DEFINE_bool(load_frozen_state, true,
            "Load the saved state as frozen (non-optimized) trajectories.");
DEFINE_bool(
        start_trajectory_with_default_topics, true,
        "Enable to immediately start the first trajectory with default topics.");
DEFINE_string(
        save_state_filename, "",
        "If non-empty, serialize state and write it to disk before shutting down.");

namespace cartographer_ros {
    namespace {
        class cartographer_node
        {
        public:
            cartographer_node(geometry_msgs::PoseWithCovarianceStamped location, bool expand_mode = false)
                    : tf_buffer(::ros::Duration(kTfBufferCacheTimeInSeconds))
                    , tf2_listener(tf_buffer)
                    , tf_listener()
                    , nh_()
                    , odom_init(false)
            {
                path_.header.frame_id = "/map";

                //state_pub                                  = nh_.advertise<std_msgs::Bool>("/motor_lock", 1, true);
               // odom_path_pub                              = nh_.advertise<nav_msgs::Path>("/odom_path", 1, true);
                //odom_sub                                   = nh_.subscribe("/odom_combined", 1, &cartographer_node::odom_combinedCB, this);
                std::tie(node_options, trajectory_options) =
                        LoadOptions(FLAGS_configuration_directory, FLAGS_configuration_basename);
                auto map_builder =
                        cartographer::common::make_unique<cartographer::mapping::MapBuilder>(
                                node_options.map_builder_options);
                node_ptr.reset(new Node(node_options, std::move(map_builder), &tf_buffer));
                if (expand_mode)
                {
                    ROS_INFO("Enter Expand Mode!");
                    boost::shared_ptr<nav_msgs::OccupancyGrid const> msg;
                    msg = ros::topic::waitForMessage<nav_msgs::OccupancyGrid>("/map",
                                                                              ros::Duration(3));
                    if(msg != nullptr) {
                        const std::vector<int8_t> &map_data(msg->data);
                        std::vector<float> data_map;
                        data_map.reserve(msg->info.width*msg->info.height);
                        for (int y = msg->info.width - 1; y >= 0; --y) {
                            //int idx_map_y = y * msg->info.height;
                            for (int x = msg->info.height - 1; x >= 0; --x) {
                                switch (map_data[x * msg->info.width + y]) {
                                    case -1:
                                        data_map.emplace_back(0);
                                        break;
                                    case 0:
                                        data_map.emplace_back(0.1);
                                        break;
                                    case 100:
                                        data_map.emplace_back(0.9);
                                        break;
                                    default:
                                        ROS_WARN("The map have another value: %f",map_data[x * msg->info.width + y]);
                                        data_map.emplace_back(0.1);
                                        break;
                                }
                            }
                        }

                        ROS_INFO("Get init map with width: %d height: %d, with Max: %f  %f",msg->info.width,msg->info.height,
                                                msg->info.origin.position.x+msg->info.resolution*msg->info.width,
                                                msg->info.origin.position.y+msg->info.resolution*msg->info.height);
                        tf::Quaternion quat;
                        tf::quaternionMsgToTF(location.pose.pose.orientation, quat);
                        double roll, pitch, yaw;
                        tf::Matrix3x3(quat).getRPY(roll, pitch, yaw);
                        ROS_INFO("pose x: %f, pose y: %f, yaw: %f", location.pose.pose.position.x,
                                 location.pose.pose.position.y, yaw);
                        cartographer::transform::Rigid3d pose = cartographer_ros::ToRigid3d(location.pose.pose);
                        ::cartographer::mapping::InitMappingInfo *initmap = new ::cartographer::mapping::InitMappingInfo();
                        initmap->width = msg->info.width;
                        initmap->hight = msg->info.height;
                        initmap->origin_x = msg->info.origin.position.x;
                        initmap->origin_y = msg->info.origin.position.y;
                        initmap->relative_pose = pose;
                        initmap->to_trajectory_id = 0;
                        initmap->cost_cells = data_map;
                        initmap->timestamp = cartographer::common::ToUniversal(cartographer_ros::FromRos(ros::Time::now()));
                        initmap->resolution = msg->info.resolution;
                        initmap->if_expand = true;
                        trajectory_options.init_info = initmap;
                    }else{
                        ROS_ERROR("cant receive topic /map, enter mode 2");
                        trajectory_options.init_info = NULL;
                    }
                } else
                {
                    trajectory_options.init_info = NULL;
                }

                if (FLAGS_start_trajectory_with_default_topics)
                {
                    node_ptr->StartTrajectoryWithDefaultTopics(trajectory_options);
                    delete trajectory_options.init_info;
                    trajectory_options.init_info =NULL;
                }
            }
            ~cartographer_node()
            {
                if(node_ptr!=nullptr)
                {
                    ROS_INFO("~cartographer_node()");
                    node_ptr.reset();
                }
            }
            std::shared_ptr<Node>      node_ptr;
        private:
            // void odom_combinedCB(const nav_msgs::Odometry& msg)
            // {
            //     geometry_msgs::PoseStamped pose;
            //     if(!odom_init)
            //     {
            //         last_odom               = msg;
            //         pose.pose.position.x    = 0;
            //         pose.pose.position.y    = 0;
            //         pose.pose.position.z    = 0;
            //         pose.pose.orientation.x = 0;
            //         pose.pose.orientation.y = 0;
            //         pose.pose.orientation.z = 0;
            //         pose.pose.orientation.w = 1;
            //         odom_init               = true;
            //     }
            //     else
            //     {
            //         pose.pose.position.y = -msg.pose.pose.position.y+last_odom.pose.pose.position.y;
            //         pose.pose.position.x = -msg.pose.pose.position.x+last_odom.pose.pose.position.x;
            //         pose.pose.position.z = msg.pose.pose.position.z-last_odom.pose.pose.position.z;
            //     }


            //     path_.header.stamp = ros::Time::now();
            //     path_.poses.push_back(pose);
            //     odom_path_pub.publish(path_);
            // }

            const double               kTfBufferCacheTimeInSeconds = 10.;
            tf2_ros::Buffer            tf_buffer;
            tf2_ros::TransformListener tf2_listener;
            tf::TransformListener      tf_listener;
            NodeOptions                node_options;
            TrajectoryOptions          trajectory_options;
           
            ros::NodeHandle            nh_;
            ros::Publisher             state_pub;
            ros::Publisher             odom_path_pub;
            ros::Subscriber            odom_sub;
            nav_msgs::Odometry         last_odom;
            nav_msgs::Path             path_;
            bool                       odom_init;
        };
    }  // namespace
}  // namespace cartographer_ros
