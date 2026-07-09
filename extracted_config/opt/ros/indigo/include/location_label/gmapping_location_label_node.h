#ifndef GMAPPING_LOCATION_LABEL_NODE_H
#define GMAPPING_LOCATION_LABEL_NODE_H

#include <ros/ros.h>
#include <tf/tf.h>
#include <string.h>
#include "location_label/location_label_base.h"
#include <tf/transform_listener.h>
#include <tf/transform_broadcaster.h>
#include <boost/thread.hpp>
#include <geometry_msgs/PoseWithCovarianceStamped.h>
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/PoseArray.h>
#include <std_msgs/Bool.h>
#include "location_label/LabelProcess.h"
#include "geometry_msgs/Pose.h"
#include <keenon_label_msgs/operate_label.h>
#include <sys/types.h>
#include "label_assemble.h"
#include <keenon_database_msgs/labelConfig.h>
#include <keenon_database_msgs/labelInfo.h>
#include <keenon_database_msgs/labelInfo_array.h>
namespace location_label {

class GmappingLocationLabel :public LocationLabelBase{
public:
  GmappingLocationLabel(tf::TransformListener& tf);
  ~GmappingLocationLabel();
  void getLabelData();
  void dealLabelData();
  void labelPoseCallback(keenon_label_msgs::gmapping_label_array msg);
  bool updateLabel();
  ros::ServiceClient client_;
  ros::NodeHandle nh_;
  std::string label_camera_frame_id,uart_id;
  tf::TransformBroadcaster br_;
  //tf::TransformListener& tf_;
  ros::Publisher pose_pub_,deal_label_pub_,label_pub_,label_posearray_pub_;
  keenon_label_msgs::gmapping_label_array pub_label_array_;
  geometry_msgs::PoseArray label_pose_array_;
  std::string labelfilename_;
  ros::Subscriber label_sub_;
  boost::thread* label_thread_;
  boost::thread* deal_label_thread_;
  bool recieve_flag_;
  tf::StampedTransform last_base2odom_;
  double min_angle_;
  double min_dis_;
};

}
#endif
