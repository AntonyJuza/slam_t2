/*
 * Copyright 2016 The Cartographer Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef CARTOGRAPHER_ROS_CARTOGRAPHER_ROS_NODE_H
#define CARTOGRAPHER_ROS_CARTOGRAPHER_ROS_NODE_H

#include <map>
#include <memory>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <std_msgs/Bool.h>

#include "cartographer/common/fixed_ratio_sampler.h"
#include "cartographer/common/mutex.h"
#include "cartographer/mapping/map_builder_interface.h"
#include "cartographer/mapping/pose_extrapolator.h"
#include "cartographer_ros/map_builder_bridge.h"
#include "cartographer_ros/node_constants.h"
#include "cartographer_ros/node_options.h"
#include "cartographer_ros/trajectory_options.h"
#include "cartographer_ros_msgs/FinishTrajectory.h"
#include "cartographer_ros_msgs/SensorTopics.h"
#include "cartographer_ros_msgs/StartTrajectory.h"
#include "cartographer_ros_msgs/StatusResponse.h"
#include "cartographer_ros_msgs/SubmapEntry.h"
#include "cartographer_ros_msgs/SubmapList.h"
#include "cartographer_ros_msgs/SubmapQuery.h"
#include "cartographer_ros_msgs/TrajectoryOptions.h"
#include "cartographer_ros_msgs/WriteState.h"
#include "nav_msgs/Odometry.h"
#include "ros/ros.h"
#include "sensor_msgs/Imu.h"
#include "sensor_msgs/LaserScan.h"
#include "sensor_msgs/MultiEchoLaserScan.h"
#include "sensor_msgs/NavSatFix.h"
#include "sensor_msgs/PointCloud2.h"
#include "tf2_ros/transform_broadcaster.h"
#include <tf/tf.h>
#include <tf/transform_listener.h>
#include <unordered_map>
#include <set>
#include <queue>
#include <nav_msgs/Path.h>
#include <geometry_msgs/PoseArray.h>
#include "visualization_msgs/MarkerArray.h"
#include "keenon_database_msgs/pbstreamConfig.h"
//#include "cartographer_ros_msgs/ManualLoop.h"
#include "keenon_database_msgs/ManualLoop.h"
#include "keenon_vslam_msgs/vslam_keyframe_info.h"
#include "keenon_vslam_msgs/keyframe_write_progress.h"
//#include "keenon_vslam_msgs/vslam_keyframe_pose.h"
#include "keenon_vslam_msgs/vslam_keyframe_pose_array.h"
#include "cartographer/sensor/vslam_data.h"
#include "cartographer_ros_msgs/WriteVslamPose.h"
#include "keenon_label_msgs/fusion_label_array.h"
#include "cartographer/mapping/id.h"
#include "cartographer/mapping/trajectory_node.h"
#include "cartographer/sensor/point_cloud.h"
#include "pcl/point_cloud.h"
#include "pcl/point_types.h"
#include "pcl_conversions/pcl_conversions.h"
#include <pcl/io/pcd_io.h>
#include "cartographer_ros_msgs/RebuildMap.h"
#include "keenon_event_tracking/event_report.h"
#include <geometry_msgs/PoseWithCovarianceStamped.h>
namespace cartographer_ros {
using ::cartographer::mapping::NodeId;
using ::cartographer::mapping::MapById;
using ::cartographer::mapping::TrajectoryNode;
struct CustomPose
{
public:
  CustomPose()
  {
  }
  CustomPose(double x_in, double y_in)
    : x(x_in)
    , y(y_in)
    , count(1)
  {
  }
  double x;
  double y;
  std::unordered_map<int,int> label_id;
  unsigned int count;
  geometry_msgs::Quaternion q;
  double getDist(const CustomPose& c1) const
  {
    return sqrt(pow((c1.x-this->x), 2)+pow((c1.y-this->y), 2));
  }
  bool operator==(const CustomPose& c1) const
  {
    return sqrt(pow((c1.x-this->x), 2)+pow((c1.y-this->y), 2))<0.01;
  }
};

struct CustomPoseHash
{
  std::size_t operator()(const CustomPose& c) const
  {
    return std::hash<double>()(c.x)^std::hash<double>()(c.y);
  }
};
struct CustomPoseEqual
{
  bool operator()(const CustomPose& c1, const CustomPose& c2) const
  {
    return sqrt(pow((c1.x-c2.x), 2)+pow((c1.y-c2.y), 2))<1.0;
  }
};
typedef std::unordered_map<CustomPose, int, CustomPoseHash, CustomPoseEqual> LabelMap;


// Wires up ROS topics to SLAM.
class Node {
public:
  Node(const NodeOptions& node_options, std::unique_ptr<cartographer::mapping::MapBuilderInterface> map_builder, tf2_ros::Buffer* tf_buffer);
  ~Node();

  Node(const Node &)              = delete;
  Node & operator =(const Node &) = delete;

  // Finishes all yet active trajectories.
  void FinishAllTrajectories();
  // Finishes a single given trajectory. Returns false if the trajectory did not
  // exist or was already finished.
  bool FinishTrajectory(int trajectory_id);

  // Runs final optimization. All trajectories have to be finished when calling.
  void RunFinalOptimization();

  // Starts the first trajectory with the default topics.
  void StartTrajectoryWithDefaultTopics(TrajectoryOptions& options);

  // Returns unique SensorIds for multiple input bag files based on
  // their TrajectoryOptions.
  // 'SensorId::id' is the expected ROS topic name.
  std::vector<
    std::set<::cartographer::mapping::TrajectoryBuilderInterface::SensorId> >
  ComputeDefaultSensorIdsForMultipleBags(
    const std::vector<TrajectoryOptions>& bags_options) const;

  // Adds a trajectory for offline processing, i.e. not listening to topics.
  int AddOfflineTrajectory(
    const std::set<
      cartographer::mapping::TrajectoryBuilderInterface::SensorId> &
    expected_sensor_ids, const TrajectoryOptions& options);

  // The following functions handle adding sensor data to a trajectory.
  void HandleOdometryMessage(int trajectory_id, const std::string& sensor_id, const geometry_msgs::PoseWithCovarianceStamped::ConstPtr& msg);
  void HandleImuFilter(int trajectory_id, const std::string& sensor_id, const sensor_msgs::Imu::ConstPtr& msg);
  void HandleNavSatFixMessage(int trajectory_id, const std::string& sensor_id, const sensor_msgs::NavSatFix::ConstPtr& msg);
  void HandleVSlamMessage(const int trajectory_id, const std::string& sensor_id, const keenon_vslam_msgs::vslam_keyframe_info::ConstPtr& msg);
  void HandleRebuildMap(int trajectory_id, const std::string& sensor_id, const cartographer_ros_msgs::RebuildMap::ConstPtr& msg);
  void HandleLandmarkMessage(
    int trajectory_id, const std::string& sensor_id, const cartographer_ros_msgs::LandmarkList::ConstPtr& msg);
  void HandleImuMessage(int trajectory_id, const std::string& sensor_id, const sensor_msgs::Imu::ConstPtr& msg);
  void HandleLaserScanMessage(int trajectory_id, const std::string& sensor_id, const sensor_msgs::LaserScan::ConstPtr& msg);
  void HandleMultiEchoLaserScanMessage(
    int trajectory_id, const std::string& sensor_id, const sensor_msgs::MultiEchoLaserScan::ConstPtr& msg);
  void HandlePointCloud2Message(int trajectory_id, const std::string& sensor_id, const sensor_msgs::PointCloud2::ConstPtr& msg);

  // Serializes the complete Node state.
  void SerializeState(const std::string& filename);

  // Loads a serialized SLAM state from a .pbstream file.
  void LoadState(const std::string& state_filename, bool load_frozen_state);
  float distance(const float a, const float b);
  bool SavePbstream(std::string path);
  int SaveVslamPose(const std::string &pose_file_name);

  ::ros::NodeHandle * node_handle();

private:
  struct Subscriber {
    ::ros::Subscriber subscriber;

    // ::ros::Subscriber::getTopic() does not necessarily return the same
    // std::string
    // it was given in its constructor. Since we rely on the topic name as the
    // unique identifier of a subscriber, we remember it ourselves.
    std::string topic;
  };
  bool HandleManualLoop(keenon_database_msgs::ManualLoopRequest& request, keenon_database_msgs::ManualLoopResponse& response);
  void HandleManualLoopPosition(int trajectory_id, const std::string& sensor_id, const std_msgs::Bool::ConstPtr& msg);
  void HandleManualLoopClosure(int trajectory_id, const std::string& sensor_id, const std_msgs::Bool::ConstPtr& msg);
  bool HandleSubmapQuery(
    cartographer_ros_msgs::SubmapQuery::Request& request, cartographer_ros_msgs::SubmapQuery::Response& response);
  bool HandleStartTrajectory(
    cartographer_ros_msgs::StartTrajectory::Request& request, cartographer_ros_msgs::StartTrajectory::Response& response);
  bool HandleFinishTrajectory(
    cartographer_ros_msgs::FinishTrajectory::Request& request, cartographer_ros_msgs::FinishTrajectory::Response& response);
  bool HandleWriteVslamPose(cartographer_ros_msgs::WriteVslamPose::Request& request, cartographer_ros_msgs::WriteVslamPose::Response& response);
  bool HandleWriteState(cartographer_ros_msgs::WriteState::Request& request, cartographer_ros_msgs::WriteState::Response& response);
  bool HandlePbstream(keenon_database_msgs::pbstreamConfigRequest & request, keenon_database_msgs::pbstreamConfigResponse & response);
  // Returns the set of SensorIds expected for a trajectory.
  // 'SensorId::id' is the expected ROS topic name.
  std::set<::cartographer::mapping::TrajectoryBuilderInterface::SensorId>
  ComputeExpectedSensorIds(
    const TrajectoryOptions& options, const cartographer_ros_msgs::SensorTopics& topics) const;
  int AddTrajectory(const TrajectoryOptions& options, const cartographer_ros_msgs::SensorTopics& topics);
  void LaunchSubscribers(const TrajectoryOptions& options, const cartographer_ros_msgs::SensorTopics& topics, int trajectory_id);
  void PublishSubmapList(const ::ros::WallTimerEvent& timer_event);
  void AddExtrapolator(int trajectory_id, const TrajectoryOptions& options);
  void AddSensorSamplers(int trajectory_id, const TrajectoryOptions& options);
  void PublishTrajectoryStates(const ::ros::WallTimerEvent& timer_event);
  void PublishTrajectoryNodeList(const ::ros::WallTimerEvent& timer_event);
  void PublishLandmarkPosesList(const ::ros::WallTimerEvent& timer_event);
  void PublishConstraintList(const ::ros::WallTimerEvent& timer_event);
  void PublishScheduledLabels(const ::ros::WallTimerEvent &timer_event);
  void PublishVslamKeyframePose(const ::ros::WallTimerEvent& unused_timer_event);
  void PublishPointCloudMap(const ::ros::WallTimerEvent& timer_event);
  void PublishSharpEdgeInfo(const ::ros::WallTimerEvent& timer_event);
  void ReportRebuildInfo(const ::ros::WallTimerEvent& timer_event);
  void SpinOccupancyGridThreadForever();
  bool ValidateTrajectoryOptions(const TrajectoryOptions& options);
  bool ValidateTopicNames(const ::cartographer_ros_msgs::SensorTopics& topics, const TrajectoryOptions& options);
  cartographer_ros_msgs::StatusResponse FinishTrajectoryUnderLock(
    int trajectory_id) REQUIRES(mutex_);

  const NodeOptions node_options_;

  tf2_ros::TransformBroadcaster tf_broadcaster_;

  cartographer::common::Mutex          mutex_;
  MapBuilderBridge map_builder_bridge_ GUARDED_BY(mutex_);

  ::ros::NodeHandle node_handle_;
  ::ros::Publisher submap_list_publisher_;
  ::ros::Publisher trajectory_node_list_publisher_;
  ::ros::Publisher landmark_poses_list_publisher_;
  ::ros::Publisher constraint_list_publisher_;
  ::ros::Publisher vslam_pose_pub_;
  ::ros::Publisher scheduled_label_pub_;
  ::ros::Publisher point_cloud_map_publisher_;
  ::ros::Publisher fit_line_pub_;
  ::ros::Publisher fitpoints_pub_;
  ::ros::Publisher fillpoints_pub_;
  ::ros::Publisher elipoints_pub_;
  //::ros::ServiceClient database_save_pbstream_;
  // These ros::ServiceServers need to live for the lifetime of the node.
  std::vector<::ros::ServiceServer> service_servers_;
  ::ros::Publisher scan_matched_point_cloud_publisher_;

  struct TrajectorySensorSamplers {
    TrajectorySensorSamplers(const double rangefinder_sampling_ratio, const double odometry_sampling_ratio, const double fixed_frame_pose_sampling_ratio, const double imu_sampling_ratio, const double landmark_sampling_ratio)
      : rangefinder_sampler(rangefinder_sampling_ratio)
      , odometry_sampler(odometry_sampling_ratio)
      , fixed_frame_pose_sampler(fixed_frame_pose_sampling_ratio)
      , imu_sampler(imu_sampling_ratio)
      , landmark_sampler(landmark_sampling_ratio)
    {
    }

    ::cartographer::common::FixedRatioSampler rangefinder_sampler;
    ::cartographer::common::FixedRatioSampler odometry_sampler;
    ::cartographer::common::FixedRatioSampler fixed_frame_pose_sampler;
    ::cartographer::common::FixedRatioSampler imu_sampler;
    ::cartographer::common::FixedRatioSampler landmark_sampler;
  };

  // These are keyed with 'trajectory_id'.
  std::map<int, ::cartographer::mapping::PoseExtrapolator> extrapolators_;
  std::unordered_map<int, TrajectorySensorSamplers>        sensor_samplers_;
  std::unordered_map<int, std::vector<Subscriber> >        subscribers_;
  std::unordered_set<std::string>                          subscribed_topics_;
  std::unordered_map<int, bool> is_active_trajectory_      GUARDED_BY(mutex_);

  std::vector<cartographer::sensor::KeyFrameInfo> vslam_frames_;

  // We have to keep the timer handles of ::ros::WallTimers around, otherwise
  // they do not fire.
  std::vector<::ros::WallTimer>          wall_timers_;
  ros::Subscriber                        manual_position_sub_;
  ros::Subscriber                        manual_closure_sub_;
  ros::Subscriber                        custom_command_sub_;
  ros::Time                              last_scan_time_;
  ros::Time                              last_odom_time_;
  ros::Time                              last_report_time_;
  int odom_jump_ = 0;
  int scan_jump_ = 0;
  int last_rebuild_time_ = 0;
  tf::TransformListener                  tf_;
  int current_id_ ;
  size_t last_trajectory_nodes_size_ = 0;
  ::cartographer::transform::Rigid3d base2tracking_ = ::cartographer::transform::Rigid3d::Identity();
};
}  // namespace cartographer_ros

#endif  // CARTOGRAPHER_ROS_CARTOGRAPHER_ROS_NODE_H
