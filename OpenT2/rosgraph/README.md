# Task 2: ROS Graph Specification

This document maps out the ROS Graph for each key node in the Keenon T2 system, outlining their published topics, subscribed topics, and service interfaces.

---

## 1. `chassis`
```
chassis
│
├── publishes
│       /motor_error_code [keenon_motor_msgs/error_code]
│       /charge_state_fromSTM32 [keenon_charge_msgs/ChargeFB]
│       /odom_combined [nav_msgs/Odometry]
│       /bump [sensor_msgs/PointCloud2]
│       /urgency_button_status [std_msgs/Bool]
│       /battery_state [sensor_msgs/BatteryState]
│       /urgency_stop [std_msgs/Float64]
│       /encoder_odom [nav_msgs/Odometry]
│       /encoder_raw [keenon_motor_msgs/encoder]
│       /stm32_up [std_msgs/String]
│       /tf [tf2_msgs/TFMessage]
│       /motor_lock_status [keenon_motor_msgs/lock_status]
│       /beam [sensor_msgs/PointCloud2]
│       /chassis_imu_data [sensor_msgs/Imu]
│       /stm32_version [std_msgs/String]
│       /error_report [keenon_ui_msgs/error_report]
│       /imu_raw [sensor_msgs/Imu]
│       /mileage [std_msgs/Float64]
│       /chassis_sensor [keenon_sensor_msgs/SensorData]
│
├── subscribes
│       /stm32_down [std_msgs/String]
│       /tf [tf2_msgs/TFMessage]
│       /tf_static [tf2_msgs/TFMessage]
│       /cmd_vel [geometry_msgs/Twist]
│       /enable_urgency_button [std_msgs/Bool]
│       /motor_lock [std_msgs/Bool]
│       /charge_cmd_toSTM32 [keenon_charge_msgs/ChargeCMD]
│
└── services
        /chassis/get_loggers
        /chassis/set_logger_level
```

---

## 2. `web_backend`
```
web_backend_node
│
├── publishes
│       /map/to_web/compressed [sensor_msgs/CompressedImage]
│       /virtual_wall/to_web/compressed [sensor_msgs/CompressedImage]
│       /gate_map/to_web/compressed [sensor_msgs/CompressedImage]
│       /move_base/global_costmap/costmap/to_web/compressed [sensor_msgs/CompressedImage]
│       /move_base/local_costmap/costmap/to_web/compressed [sensor_msgs/CompressedImage]
│       /robot_state [web_backend/robot_state]
│       /run_mapping [std_msgs/UInt8]
│       /scan_base_map [web_backend/PointArray]
│
├── subscribes
│       /scan [sensor_msgs/LaserScan]
│       /move_base/local_costmap/costmap [nav_msgs/OccupancyGrid]
│       /gate_map [nav_msgs/OccupancyGrid]
│       /mapping_status [std_msgs/UInt8]
│       /map [nav_msgs/OccupancyGrid]
│       /virtual_wall [nav_msgs/OccupancyGrid]
│       /move_base/global_costmap/costmap [nav_msgs/OccupancyGrid]
│       /tf [tf2_msgs/TFMessage]
│       /tf_static [tf2_msgs/TFMessage]
│
└── services
        /web_command
        /web_backend_node/get_loggers
        /web_backend_node/set_logger_level
```

---

## 3. `move_base`
```
move_base
│
├── publishes
│       /cmd_vel [geometry_msgs/Twist]
│       /move_base/status [actionlib_msgs/GoalStatusArray]
│       /move_base/feedback [keenon_move_base_msgs/MoveBaseActionFeedback]
│       /move_base/result [keenon_move_base_msgs/MoveBaseActionResult]
│       /move_base/global_costmap/costmap [nav_msgs/OccupancyGrid]
│       /move_base/local_costmap/costmap [nav_msgs/OccupancyGrid]
│       /move_base/current_goal [geometry_msgs/PoseStamped]
│       /robot_elevator_percent [std_msgs/UInt8]
│       /elev_process_signal [std_msgs/UInt8]
│       /elev_pos_state [std_msgs/UInt8]
│       /gate_cmd [keenon_gate_msgs/gate_cmd]
│
├── subscribes
│       /scan [sensor_msgs/LaserScan]
│       /planner_scan [sensor_msgs/LaserScan]
│       /camera_1/depth/points [sensor_msgs/PointCloud2]
│       /camera_2/depth/points [sensor_msgs/PointCloud2]
│       /bump [sensor_msgs/PointCloud2]
│       /virtual_wall [nav_msgs/OccupancyGrid]
│       /virtual_wall_updates [map_msgs/OccupancyGridUpdate]
│       /gate_map [nav_msgs/OccupancyGrid]
│       /elevator_map [nav_msgs/OccupancyGrid]
│       /vel_map [nav_msgs/OccupancyGrid]
│       /feature_detection_node/pairs_leg_cloud [sensor_msgs/PointCloud]
│       /gate_status [keenon_gate_msgs/gate_status]
│       /schedule_state [std_msgs/Bool]
│       /move_base/goal [keenon_move_base_msgs/MoveBaseActionGoal]
│       /move_base_simple/goal [geometry_msgs/PoseStamped]
│       /move_base/cancel [actionlib_msgs/GoalID]
│       /tf [tf2_msgs/TFMessage]
│       /tf_static [tf2_msgs/TFMessage]
│
└── services
        /move_base/make_plan
        /move_base/clear_costmaps
        /run_movebase
        /move_base/get_loggers
        /move_base/set_logger_level
```

---

## 4. `front_end`
```
front_end_node
│
├── publishes
│       /tf [tf2_msgs/TFMessage]
│
├── subscribes
│       /chassis_imu_data [sensor_msgs/Imu]
│       /encoder_raw [keenon_motor_msgs/encoder]
│       /laser_odom [sensor_msgs/Imu]
│       /tf [tf2_msgs/TFMessage]
│       /tf_static [tf2_msgs/TFMessage]
│
└── services
        /front_end_node/get_loggers
        /front_end_node/set_logger_level
```

---

## 5. `multi_lidar_filter`
```
multi_lidar_filter
│
├── publishes
│       /scan_orig [sensor_msgs/LaserScan]
│       /scan [sensor_msgs/LaserScan]
│
├── subscribes
│       /scan_front_orig [sensor_msgs/LaserScan]
│       /scan_back_orig [sensor_msgs/LaserScan]
│       /tf [tf2_msgs/TFMessage]
│       /tf_static [tf2_msgs/TFMessage]
│
└── services
        /multi_lidar_filter/get_loggers
        /multi_lidar_filter/set_logger_level
```

---

## 6. `cartographer`
```
cartographer_node
│
├── publishes
│       /mapping_status [std_msgs/UInt8]
│       /run_rosbag [std_msgs/Bool]
│       /tf_static [tf2_msgs/TFMessage]
│
├── subscribes
│       /save_new_map [std_msgs/Empty]
│       /run_mapping [std_msgs/UInt8]
│
└── services
        /operate_pbstream
        /cartographer_node/get_loggers
        /cartographer_node/set_logger_level
```

---

## 7. `switch_map`
```
switch_map
│
├── publishes
│       /map [nav_msgs/OccupancyGrid]
│       /virtual_wall [nav_msgs/OccupancyGrid]
│       /gate_map [nav_msgs/OccupancyGrid]
│       /elevator_map [nav_msgs/OccupancyGrid]
│       /vel_map [nav_msgs/OccupancyGrid]
│       /map_metadata [nav_msgs/MapMetaData]
│       /robot_current_floor [std_msgs/Int16]
│       /label_map [keenon_label_msgs/gmapping_label_array]
│
├── subscribes
│       /load_label [std_msgs/Empty]
│       /tf [tf2_msgs/TFMessage]
│       /tf_static [tf2_msgs/TFMessage]
│
└── services
        /static_map
        /switch_dest_floor_map
        /config_map_trans
        /switch_map/get_loggers
        /switch_map/set_logger_level
```

---

## 8. `schedule_map_builder`
```
schedule_map_builder
│
├── publishes
│       /virtual_wall_1 [nav_msgs/OccupancyGrid]
│       /virtual_wall_updates [map_msgs/OccupancyGridUpdate]
│       /schedule_state [std_msgs/Bool]
│       /click_map_pub_ [nav_msgs/OccupancyGrid]
│
├── subscribes
│       /clicked_point [geometry_msgs/PointStamped]
│       /robot_current_floor [std_msgs/Int16]
│       /schedule_path [nav_msgs/Path]
│       /schedule_path_test [nav_msgs/Path]
│       /robot_pose [geometry_msgs/PoseStamped]
│       /tf [tf2_msgs/TFMessage]
│       /tf_static [tf2_msgs/TFMessage]
│
└── services
        /schedule_map_builder/get_loggers
        /schedule_map_builder/set_logger_level
```

---

## 9. `interactive`
```
interactive
│
├── publishes
│       /elevator_task_status [keenon_elevator_msgs/elev_task_status]
│       /elev_lora_send [keenon_elevator_msgs/elev_lora_driver]
│       /seller_report_toUI [std_msgs/UInt8]
│       /init_location_pose [std_msgs/Int8]
│       /error_report_handle [keenon_ui_msgs/error_list_report]
│       /gate_status [keenon_gate_msgs/gate_status]
│       /elev_4g_send [keenon_elevator_msgs/elev_request]
│       /charge_task/goal [keenon_charge_msgs/ChargeTaskActionGoal]
│       /gate_lora_send [keenon_gate_msgs/gate_lora_driver]
│       /charge_report_toUI [std_msgs/UInt8]
│       /elevator_position [keenon_ui_msgs/position_report]
│       /move_base/goal [keenon_move_base_msgs/MoveBaseActionGoal]
│       /pose_mac_address_cmd [std_msgs/String]
│       /app_navigation_status [keenon_move_base_msgs/MoveBaseFeedback]
│       /ui_command_topic [std_msgs/UInt64]
│       /elevator_lora_request [keenon_elevator_msgs/elev_request]
│       /seller_task/cancel [actionlib_msgs/GoalID]
│       /seller_task/goal [keenon_seller_msgs/SellerTaskActionGoal]
│       /gate_mode [std_msgs/UInt8]
│       /elevator_4g_request [keenon_elevator_msgs/elev_request]
│       /current_active_dest [std_msgs/UInt16]
│       /movebaseActionDone [keenon_database_msgs/poseInfo]
│       /charge_task/cancel [actionlib_msgs/GoalID]
│       /move_base/cancel [actionlib_msgs/GoalID]
│       /error_report [keenon_ui_msgs/error_report]
│       /app_schedule_server [keenon_database_msgs/poseInfo]
│       /version [keenon_database_msgs/version]
│       /motor_lock [std_msgs/Bool]
│
├── subscribes
│       /charge_task/feedback [keenon_charge_msgs/ChargeTaskActionFeedback]
│       /elev_lora_receive [keenon_elevator_msgs/elev_lora_driver]
│       /elevator_4g_request [keenon_elevator_msgs/elev_request]
│       /app_cmd_charge [keenon_database_msgs/poseInfo]
│       /move_base/status [actionlib_msgs/GoalStatusArray]
│       /move_base/feedback [keenon_move_base_msgs/MoveBaseActionFeedback]
│       /charge_state_fromSTM32 [keenon_charge_msgs/ChargeFB]
│       /init_location_pose [std_msgs/Int8]
│       /gate_set_robot_channel [std_msgs/String]
│       /seller_task/status [actionlib_msgs/GoalStatusArray]
│       /gate_ping [std_msgs/Empty]
│       /elevator_response [keenon_elevator_msgs/elev_response]
│       /seller_task/result [keenon_seller_msgs/SellerTaskActionResult]
│       /gate_lora_receive [keenon_gate_msgs/gate_lora_driver]
│       /pose_mac_address_cmd [std_msgs/String]
│       /seller_request [std_msgs/UInt8]
│       /elevator_lora_request [keenon_elevator_msgs/elev_request]
│       /gate_cmd [keenon_gate_msgs/gate_cmd]
│       /run_rosbag [std_msgs/Bool]
│       /seller_task/feedback [keenon_seller_msgs/SellerTaskActionFeedback]
│       /error_report [keenon_ui_msgs/error_report]
│       /label_reatime_location_status [std_msgs/Int8]
│       /charge_trigger [std_msgs/UInt8]
│       /schedule_sw_state [std_msgs/Bool]
│       /initialpose [geometry_msgs/PoseWithCovarianceStamped]
│       /charge_task/status [actionlib_msgs/GoalStatusArray]
│       /charge_task/result [keenon_charge_msgs/ChargeTaskActionResult]
│       /move_base/result [keenon_move_base_msgs/MoveBaseActionResult]
│       /tf [tf2_msgs/TFMessage]
│       /tf_static [tf2_msgs/TFMessage]
│
└── services
        /interactive/get_loggers
        /init_location_node/config
        /dst_pose_sort
        /app_cmd_navigation
        /ui_cmd/fake_id_server
        /cfg_rosbag_sw_cmd
        /save_current_pose
        /elevator/fake_elevator_control
        /save_current_init_pose
```

---

## 10. `robot_settings`
```
robot_settings
│
├── publishes
│       /error_report [keenon_ui_msgs/error_report]
│
├── subscribes
│
└── services
        /robot_settings/set_logger_level
        /robot_settings/get_loggers
        /robot_settings/cfg_origin_floor_cmd
        /robot_settings/cfg_schedule_sw_cmd
        /robot_settings/cfg_launch_type_cmd
```

---

## 11. `peanut_localization`
```
peanut_localization_node
│
├── publishes
│       /gauss_cloud_point [sensor_msgs/PointCloud2]
│       /aligned_pointcloud_inliers [sensor_msgs/PointCloud2]
│       /localization/pose_visualization_marker [visualization_msgs/Marker]
│       /localization/visualization_marker [sensor_msgs/PointCloud2]
│       /scan_pointcloud_filtered [sensor_msgs/PointCloud2]
│       /tf [tf2_msgs/TFMessage]
│       /localization/robot_pose [geometry_msgs/PoseWithCovarianceStamped]
│       /reference_pointcloud [sensor_msgs/PointCloud2]
│       /aligned_pointcloud_outliers [sensor_msgs/PointCloud2]
│       /reference_pointcloud_filtered [sensor_msgs/PointCloud2]
│       /localization/map_check [std_msgs/Header]
│
├── subscribes
│       /elev_pos_state [std_msgs/UInt8]
│       /scan_orig [sensor_msgs/LaserScan]
│       /charge_state_fromSTM32 [keenon_charge_msgs/ChargeFB]
│       /run_mapping [std_msgs/UInt8]
│       /elev_process_signal [std_msgs/UInt8]
│       /map [nav_msgs/OccupancyGrid]
│       /initialpose [geometry_msgs/PoseWithCovarianceStamped]
│       /tf [tf2_msgs/TFMessage]
│       /tf_static [tf2_msgs/TFMessage]
│
└── services
        /localization/label_pose_check
        /peanut_localization_node/set_logger_level
        /peanut_localization_node/get_loggers
        /localization/better_location
        /localization/set_pose
```
