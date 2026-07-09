# Task 3: ROS Topic Database

This database contains every active topic in the Keenon T2 system, including their message types, publishing nodes, subscribing nodes, and functional descriptions.

| Topic | Type | Publisher(s) | Subscriber(s) | Description |
| :--- | :--- | :--- | :--- | :--- |
| `/add_label` | `keenon_label_msgs/add_label` | /rosbridge_websocket | /robot_pose_location_label_node, /ros_label_fusion, /rosbag_record_node |  |
| `/aligned_pointcloud_inliers` | `sensor_msgs/PointCloud2` | /peanut_localization_node |  |  |
| `/aligned_pointcloud_outliers` | `sensor_msgs/PointCloud2` | /peanut_localization_node |  |  |
| `/amcl/on_off_switch` | `std_msgs/Bool` | /elevator_detection_node |  |  |
| `/amcl_pose_laser` | `unknown` |  | /rosbag_record_node |  |
| `/app_cmd_charge` | `keenon_database_msgs/poseInfo` | /coap_bridge_server | /interactive, /rosbag_record_node | Automatic charging task state / command |
| `/app_navigation_status` | `keenon_move_base_msgs/MoveBaseFeedback` | /interactive, /coap_bridge_server | /coap_bridge_server, /rosbag_record_node |  |
| `/app_schedule_live_status` | `std_msgs/String` |  | /coap_bridge_server |  |
| `/app_schedule_server` | `keenon_database_msgs/poseInfo` | /interactive |  |  |
| `/app_schedule_status` | `std_msgs/String` |  | /coap_bridge_server |  |
| `/battery_state` | `sensor_msgs/BatteryState` | /chassis | /coap_bridge_server, /rosbridge_websocket, /rosbag_record_node |  |
| `/beam` | `sensor_msgs/PointCloud2` | /chassis | /rosbag_record_node |  |
| `/better_location_pose` | `unknown` |  | /rosbag_record_node |  |
| `/block_pcl` | `sensor_msgs/PointCloud2` | /move_base | /rosbag_record_node |  |
| `/bump` | `sensor_msgs/PointCloud2` | /chassis | /move_base, /rosbag_record_node |  |
| `/camera_1/camera_1_nodelet_manager/bond` | `bond/Status` | /camera_1/camera_1_nodelet_manager, /camera_1/depth_metric_rect, /camera_1/depth_metric, /camera_1/depth_points, /camera_1/driver, /camera_1/depth_rectify_depth | /camera_1/camera_1_nodelet_manager, /camera_1/depth_metric_rect, /camera_1/depth_metric, /camera_1/depth_points, /camera_1/driver, /camera_1/depth_rectify_depth | Front depth camera stream / driver parameter |
| `/camera_1/depth/camera_info` | `sensor_msgs/CameraInfo` | /camera_1/camera_1_nodelet_manager | /camera_1/camera_1_nodelet_manager | Front depth camera stream / driver parameter |
| `/camera_1/depth/image` | `sensor_msgs/Image` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/image/compressed` | `sensor_msgs/CompressedImage` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/image/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/image/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/image_raw` | `sensor_msgs/Image` | /camera_1/camera_1_nodelet_manager | /camera_1/camera_1_nodelet_manager | Front depth camera stream / driver parameter |
| `/camera_1/depth/image_raw/compressed` | `sensor_msgs/CompressedImage` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/image_raw/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/image_raw/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/image_rect` | `sensor_msgs/Image` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/image_rect/compressed` | `sensor_msgs/CompressedImage` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/image_rect/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/image_rect/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/image_rect_raw` | `sensor_msgs/Image` | /camera_1/camera_1_nodelet_manager | /camera_1/camera_1_nodelet_manager | Front depth camera stream / driver parameter |
| `/camera_1/depth/image_rect_raw/compressed` | `sensor_msgs/CompressedImage` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/image_rect_raw/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/image_rect_raw/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth/points` | `sensor_msgs/PointCloud2` | /camera_1/camera_1_nodelet_manager | /move_base | Front depth camera stream / driver parameter |
| `/camera_1/depth_rectify_depth/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth_rectify_depth/parameter_updates` | `dynamic_reconfigure/Config` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth_registered/camera_info` | `sensor_msgs/CameraInfo` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth_registered/image_raw` | `sensor_msgs/Image` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth_registered/image_raw/compressed` | `sensor_msgs/CompressedImage` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth_registered/image_raw/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/depth_registered/image_raw/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/driver/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/driver/parameter_updates` | `dynamic_reconfigure/Config` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/ir/camera_info` | `sensor_msgs/CameraInfo` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/ir/image` | `sensor_msgs/Image` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/ir/image/compressed` | `sensor_msgs/CompressedImage` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/ir/image/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/ir/image/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/projector/camera_info` | `sensor_msgs/CameraInfo` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/rgb/camera_info` | `sensor_msgs/CameraInfo` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/rgb/image_raw` | `sensor_msgs/Image` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/rgb/image_raw/compressed` | `sensor_msgs/CompressedImage` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/rgb/image_raw/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_1/rgb/image_raw/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_1/camera_1_nodelet_manager |  | Front depth camera stream / driver parameter |
| `/camera_2/camera_2_nodelet_manager/bond` | `bond/Status` | /camera_2/camera_2_nodelet_manager, /camera_2/driver, /camera_2/depth_points, /camera_2/depth_metric_rect, /camera_2/depth_metric, /camera_2/depth_rectify_depth | /camera_2/camera_2_nodelet_manager, /camera_2/driver, /camera_2/depth_points, /camera_2/depth_metric_rect, /camera_2/depth_metric, /camera_2/depth_rectify_depth | Rear depth camera stream / driver parameter |
| `/camera_2/depth/camera_info` | `sensor_msgs/CameraInfo` | /camera_2/camera_2_nodelet_manager | /camera_2/camera_2_nodelet_manager | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image` | `sensor_msgs/Image` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image/compressed` | `sensor_msgs/CompressedImage` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image_raw` | `sensor_msgs/Image` | /camera_2/camera_2_nodelet_manager | /camera_2/camera_2_nodelet_manager | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image_raw/compressed` | `sensor_msgs/CompressedImage` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image_raw/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image_raw/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image_rect` | `sensor_msgs/Image` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image_rect/compressed` | `sensor_msgs/CompressedImage` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image_rect/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image_rect/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image_rect_raw` | `sensor_msgs/Image` | /camera_2/camera_2_nodelet_manager | /camera_2/camera_2_nodelet_manager | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image_rect_raw/compressed` | `sensor_msgs/CompressedImage` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image_rect_raw/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/image_rect_raw/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth/points` | `sensor_msgs/PointCloud2` | /camera_2/camera_2_nodelet_manager | /move_base | Rear depth camera stream / driver parameter |
| `/camera_2/depth_rectify_depth/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth_rectify_depth/parameter_updates` | `dynamic_reconfigure/Config` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth_registered/camera_info` | `sensor_msgs/CameraInfo` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth_registered/image_raw` | `sensor_msgs/Image` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth_registered/image_raw/compressed` | `sensor_msgs/CompressedImage` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth_registered/image_raw/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/depth_registered/image_raw/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/driver/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/driver/parameter_updates` | `dynamic_reconfigure/Config` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/ir/camera_info` | `sensor_msgs/CameraInfo` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/ir/image` | `sensor_msgs/Image` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/ir/image/compressed` | `sensor_msgs/CompressedImage` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/ir/image/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/ir/image/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/projector/camera_info` | `sensor_msgs/CameraInfo` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/rgb/camera_info` | `sensor_msgs/CameraInfo` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/rgb/image_raw` | `sensor_msgs/Image` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/rgb/image_raw/compressed` | `sensor_msgs/CompressedImage` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/rgb/image_raw/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/camera_2/rgb/image_raw/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /camera_2/camera_2_nodelet_manager |  | Rear depth camera stream / driver parameter |
| `/charge_cmd_toSTM32` | `keenon_charge_msgs/ChargeCMD` | /matching_task | /rosbag_record_node, /chassis | Automatic charging task state / command |
| `/charge_fake_goal` | `std_msgs/UInt8` |  | /matching_task, /rosbag_record_node | Automatic charging task state / command |
| `/charge_report_toUI` | `std_msgs/UInt8` | /interactive | /coap_bridge_server, /rosbag_record_node | Automatic charging task state / command |
| `/charge_state_fromSTM32` | `keenon_charge_msgs/ChargeFB` | /chassis | /interactive, /matching_task, /peanut_localization_node, /rosbag_record_node | Automatic charging task state / command |
| `/charge_task/cancel` | `actionlib_msgs/GoalID` | /interactive | /matching_task, /rosbag_record_node | Automatic charging task state / command |
| `/charge_task/feedback` | `keenon_charge_msgs/ChargeTaskActionFeedback` | /matching_task | /interactive, /rosbag_record_node | Automatic charging task state / command |
| `/charge_task/goal` | `keenon_charge_msgs/ChargeTaskActionGoal` | /matching_task, /interactive | /matching_task, /rosbag_record_node | Automatic charging task state / command |
| `/charge_task/result` | `keenon_charge_msgs/ChargeTaskActionResult` | /matching_task | /interactive, /rosbag_record_node | Automatic charging task state / command |
| `/charge_task/status` | `actionlib_msgs/GoalStatusArray` | /matching_task | /interactive, /rosbag_record_node | Automatic charging task state / command |
| `/charge_trigger` | `std_msgs/UInt8` | /matching_task | /interactive, /rosbag_record_node | Automatic charging task state / command |
| `/chassis_imu_data` | `sensor_msgs/Imu` | /chassis | /front_end_node, /rosbag_record_node |  |
| `/chassis_sensor` | `keenon_sensor_msgs/SensorData` | /chassis | /rosbag_record_node |  |
| `/click_map_pub_` | `nav_msgs/OccupancyGrid` | /schedule_map_builder |  |  |
| `/clicked_point` | `geometry_msgs/PointStamped` |  | /schedule_map_builder, /move_base |  |
| `/cmd_vel` | `geometry_msgs/Twist` | /coap_bridge_server, /matching_task, /move_base | /move_base, /rosbag_record_node, /chassis |  |
| `/curr_icp_score` | `std_msgs/Float32` | /ros_label_fusion |  |  |
| `/current_active_dest` | `std_msgs/UInt16` | /interactive | /coap_bridge_server |  |
| `/deal_label_file` | `std_msgs/Bool` | /gmapping_location_label_node | /robot_pose_location_label_node |  |
| `/debug_mode` | `std_msgs/UInt8` |  | /peanut_localization_node |  |
| `/diagnostics` | `diagnostic_msgs/DiagnosticArray` | /sdkeli_front, /sdkeli_back |  |  |
| `/elev_4g_send` | `keenon_elevator_msgs/elev_request` | /interactive | /coap_bridge_server | Elevator passage coordination / communication |
| `/elev_detect_cloud` | `sensor_msgs/PointCloud2` | /move_base | /rosbag_record_node | Elevator passage coordination / communication |
| `/elev_detect_cloud2` | `sensor_msgs/PointCloud2` | /move_base | /rosbag_record_node | Elevator passage coordination / communication |
| `/elev_loc_signal` | `std_msgs/Bool` | /elevator_detection_node | /move_base, /rosbag_record_node | Elevator passage coordination / communication |
| `/elev_lora_receive` | `keenon_elevator_msgs/elev_lora_driver` |  | /interactive | Elevator passage coordination / communication |
| `/elev_lora_send` | `keenon_elevator_msgs/elev_lora_driver` | /interactive |  | Elevator passage coordination / communication |
| `/elev_pos_state` | `std_msgs/UInt8` | /move_base | /peanut_localization_node, /rosbag_record_node | Elevator passage coordination / communication |
| `/elev_process_signal` | `std_msgs/UInt8` | /move_base | /elevator_detection_node, /peanut_localization_node, /rosbag_record_node | Elevator passage coordination / communication |
| `/elevator_4g_request` | `keenon_elevator_msgs/elev_request` | /interactive | /interactive | Elevator passage coordination / communication |
| `/elevator_lora_request` | `keenon_elevator_msgs/elev_request` | /interactive | /interactive | Elevator passage coordination / communication |
| `/elevator_map` | `nav_msgs/OccupancyGrid` | /switch_map | /move_base, /rosbag_record_node | Elevator passage coordination / communication |
| `/elevator_position` | `keenon_ui_msgs/position_report` | /interactive | /rosbag_record_node | Elevator passage coordination / communication |
| `/elevator_request` | `unknown` |  | /rosbag_record_node | Elevator passage coordination / communication |
| `/elevator_response` | `keenon_elevator_msgs/elev_response` | /coap_bridge_server | /interactive, /rosbag_record_node | Elevator passage coordination / communication |
| `/elevator_state` | `unknown` |  | /rosbag_record_node | Elevator passage coordination / communication |
| `/elevator_task_status` | `keenon_elevator_msgs/elev_task_status` | /interactive | /coap_bridge_server, /rosbag_record_node | Elevator passage coordination / communication |
| `/enable_urgency_button` | `std_msgs/Bool` | /coap_bridge_server | /rosbag_record_node, /chassis |  |
| `/encoder_odom` | `nav_msgs/Odometry` | /chassis | /rosbag_record_node | Motor control / raw wheel ticks / locks |
| `/encoder_raw` | `keenon_motor_msgs/encoder` | /chassis | /front_end_node, /sensor_monitor_node, /rosbag_record_node | Motor control / raw wheel ticks / locks |
| `/error_report` | `keenon_ui_msgs/error_report` | /database, /location_lost_detecthion_node, /robot_settings, /interactive, /sensor_monitor_node, /move_base, /chassis | /interactive, /rosbag_record_node |  |
| `/error_report_handle` | `keenon_ui_msgs/error_list_report` | /interactive | /coap_bridge_server |  |
| `/feature_detection_node/pairs_leg_cloud` | `sensor_msgs/PointCloud` |  | /move_base, /rosbag_record_node |  |
| `/free_pub_cloud` | `sensor_msgs/PointCloud2` | /peanut_localization_node |  |  |
| `/free_space_pub_cloud_point` | `sensor_msgs/PointCloud2` | /peanut_localization_node |  |  |
| `/fusion_curr_label` | `keenon_label_msgs/label_msg` | /ros_label_fusion |  |  |
| `/fusion_label_array` | `keenon_label_msgs/fusion_label_array` | /ros_label_fusion |  |  |
| `/fusion_label_robot_pose` | `keenon_label_msgs/label_robot_pose` | /ros_label_fusion |  |  |
| `/fusion_label_visualization` | `visualization_msgs/Marker` | /ros_label_fusion |  |  |
| `/gate_cloud` | `sensor_msgs/PointCloud2` | /move_base | /move_base, /rosbag_record_node | Automatic gate opening / wifi triggering |
| `/gate_cmd` | `keenon_gate_msgs/gate_cmd` | /move_base | /interactive, /rosbag_record_node | Automatic gate opening / wifi triggering |
| `/gate_get_mode` | `keenon_gate_msgs/gate_get_mode` |  | /interactive | Automatic gate opening / wifi triggering |
| `/gate_lora_receive` | `keenon_gate_msgs/gate_lora_driver` |  | /interactive | Automatic gate opening / wifi triggering |
| `/gate_lora_send` | `keenon_gate_msgs/gate_lora_driver` | /interactive |  | Automatic gate opening / wifi triggering |
| `/gate_map` | `nav_msgs/OccupancyGrid` | /switch_map | /web_backend_node, /move_base, /rosbag_record_node | Automatic gate opening / wifi triggering |
| `/gate_map/to_web` | `sensor_msgs/Image` | /web_backend_node |  | Automatic gate opening / wifi triggering |
| `/gate_map/to_web/compressed` | `sensor_msgs/CompressedImage` | /web_backend_node |  | Automatic gate opening / wifi triggering |
| `/gate_map/to_web/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /web_backend_node |  | Automatic gate opening / wifi triggering |
| `/gate_map/to_web/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /web_backend_node |  | Automatic gate opening / wifi triggering |
| `/gate_mode` | `std_msgs/UInt8` | /interactive |  | Automatic gate opening / wifi triggering |
| `/gate_ping` | `std_msgs/Empty` |  | /interactive | Automatic gate opening / wifi triggering |
| `/gate_set_channel` | `keenon_gate_msgs/gate_set_channel` |  | /interactive | Automatic gate opening / wifi triggering |
| `/gate_set_mode` | `keenon_gate_msgs/gate_set_mode` |  | /interactive | Automatic gate opening / wifi triggering |
| `/gate_set_robot_channel` | `std_msgs/UInt8` |  | /interactive | Automatic gate opening / wifi triggering |
| `/gate_status` | `keenon_gate_msgs/gate_status` | /interactive | /move_base, /rosbag_record_node | Automatic gate opening / wifi triggering |
| `/gauss_cloud_point` | `sensor_msgs/PointCloud2` | /peanut_localization_node |  |  |
| `/gmapping_label_pose` | `keenon_label_msgs/gmapping_label_array` |  | /gmapping_location_label_node |  |
| `/gmapping_location_label` | `keenon_label_msgs/location_label` | /gmapping_location_label_node |  |  |
| `/gmapping_map` | `nav_msgs/OccupancyGrid` |  | /web_backend_node |  |
| `/gmapping_map/to_web` | `sensor_msgs/Image` | /web_backend_node |  |  |
| `/gmapping_map/to_web/compressed` | `sensor_msgs/CompressedImage` | /web_backend_node |  |  |
| `/gmapping_map/to_web/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /web_backend_node |  |  |
| `/gmapping_map/to_web/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /web_backend_node |  |  |
| `/imu_raw` | `sensor_msgs/Imu` | /chassis | /sensor_monitor_node, /rosbag_record_node |  |
| `/init_location_pose` | `std_msgs/Int8` | /interactive | /coap_bridge_server, /interactive, /move_base, /rosbag_record_node |  |
| `/initialpose` | `geometry_msgs/PoseWithCovarianceStamped` | /rosbridge_websocket | /interactive, /peanut_localization_node, /rosbag_record_node |  |
| `/joint_states` | `sensor_msgs/JointState` |  | /robot_state_publisher |  |
| `/label_map` | `keenon_label_msgs/gmapping_label_array` | /switch_map | /robot_pose_location_label_node, /ros_label_fusion, /rosbag_record_node |  |
| `/label_pose` | `geometry_msgs/PoseArray` | /robot_pose_location_label_node |  |  |
| `/label_posearray` | `geometry_msgs/PoseArray` | /robot_pose_location_label_node, /gmapping_location_label_node |  |  |
| `/label_reatime_location_status` | `std_msgs/Int8` | /ros_label_fusion | /interactive |  |
| `/label_ref` | `keenon_label_msgs/location_label_ref_array` | /label_camera_node | /ros_label_fusion, /rosbag_record_node |  |
| `/label_show` | `keenon_label_msgs/gmapping_label_array` | /robot_pose_location_label_node, /gmapping_location_label_node |  |  |
| `/laser_odom` | `sensor_msgs/Imu` | /srf_node | /front_end_node |  |
| `/line_params` | `std_msgs/Float64MultiArray` | /elevator_detection_node |  |  |
| `/load_label` | `std_msgs/Int16` |  | /switch_map |  |
| `/localization/map_check` | `std_msgs/Header` | /peanut_localization_node |  | Planar localization estimates / matching cloud |
| `/localization/pose_visualization_marker` | `visualization_msgs/Marker` | /peanut_localization_node |  | Planar localization estimates / matching cloud |
| `/localization/robot_pose` | `geometry_msgs/PoseWithCovarianceStamped` | /peanut_localization_node | /rosbag_record_node | Planar localization estimates / matching cloud |
| `/localization/visualization_marker` | `sensor_msgs/PointCloud2` | /peanut_localization_node |  | Planar localization estimates / matching cloud |
| `/location_label` | `keenon_label_msgs/location_label_cov` | /robot_pose_location_label_node |  |  |
| `/location_lost_score` | `std_msgs/Float64` | /location_lost_detecthion_node |  |  |
| `/lora_run_status` | `std_msgs/Bool` |  | /interactive |  |
| `/loss_location_status` | `std_msgs/Int8` | /location_lost_detecthion_node | /coap_bridge_server |  |
| `/map` | `nav_msgs/OccupancyGrid` | /switch_map | /location_lost_detecthion_node, /web_backend_node, /peanut_localization_node, /move_base, /rosbag_record_node |  |
| `/map/to_web` | `sensor_msgs/Image` | /web_backend_node |  |  |
| `/map/to_web/compressed` | `sensor_msgs/CompressedImage` | /web_backend_node |  |  |
| `/map/to_web/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /web_backend_node |  |  |
| `/map/to_web/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /web_backend_node |  |  |
| `/map_metadata` | `nav_msgs/MapMetaData` | /switch_map | /rosbag_record_node |  |
| `/mapping_status` | `std_msgs/UInt8` | /cartographer_node | /web_backend_node, /rosbag_record_node |  |
| `/matching_output_model` | `sensor_msgs/PointCloud2` | /matching_task | /rosbag_record_node |  |
| `/matching_output_scan` | `sensor_msgs/PointCloud2` | /matching_task | /rosbag_record_node |  |
| `/mileage` | `std_msgs/Float64` | /chassis | /coap_bridge_server, /rosbag_record_node |  |
| `/min_dy_obs_distance` | `std_msgs/Float64` |  | /coap_bridge_server, /rosbag_record_node |  |
| `/motor_error_code` | `keenon_motor_msgs/error_code` | /chassis | /coap_bridge_server, /rosbag_record_node | Motor control / raw wheel ticks / locks |
| `/motor_lock` | `std_msgs/Bool` | /coap_bridge_server, /interactive, /control/rosbridge_websocket, /move_base | /rosbag_record_node, /chassis | Motor control / raw wheel ticks / locks |
| `/motor_lock_status` | `keenon_motor_msgs/lock_status` | /chassis | /coap_bridge_server, /rosbridge_websocket, /move_base, /rosbag_record_node | Motor control / raw wheel ticks / locks |
| `/move_base/KPlannerROS/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/KPlannerROS/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/KPlannerROS/path_1` | `nav_msgs/Path` | /move_base | /rosbag_record_node | Navigation / path planning topic |
| `/move_base/KPlannerROS/path_2` | `nav_msgs/Path` | /move_base | /rosbag_record_node | Navigation / path planning topic |
| `/move_base/KPlannerROS/plan_calc` | `nav_msgs/Path` | /move_base | /rosbag_record_node | Navigation / path planning topic |
| `/move_base/KPlannerROS/plan_output` | `nav_msgs/Path` | /move_base | /rosbag_record_node | Navigation / path planning topic |
| `/move_base/TebLocalPlannerROS/global_plan` | `nav_msgs/Path` | /move_base |  | Navigation / path planning topic |
| `/move_base/TebLocalPlannerROS/local_plan` | `nav_msgs/Path` | /move_base |  | Navigation / path planning topic |
| `/move_base/TebLocalPlannerROS/obstacles` | `teb_local_planner/ObstacleMsg` |  | /move_base | Navigation / path planning topic |
| `/move_base/TebLocalPlannerROS/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/TebLocalPlannerROS/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/TebLocalPlannerROS/polygon_test` | `geometry_msgs/PolygonStamped` | /move_base |  | Navigation / path planning topic |
| `/move_base/TebLocalPlannerROS/teb_feedback` | `teb_local_planner/FeedbackMsg` | /move_base |  | Navigation / path planning topic |
| `/move_base/TebLocalPlannerROS/teb_markers` | `visualization_msgs/Marker` | /move_base |  | Navigation / path planning topic |
| `/move_base/TebLocalPlannerROS/teb_poses` | `geometry_msgs/PoseArray` | /move_base | /rosbag_record_node | Navigation / path planning topic |
| `/move_base/cancel` | `actionlib_msgs/GoalID` | /interactive | /move_base, /rosbag_record_node | Navigation / path planning topic |
| `/move_base/current_goal` | `geometry_msgs/PoseStamped` | /move_base | /rosbag_record_node | Navigation / path planning topic |
| `/move_base/feedback` | `keenon_move_base_msgs/MoveBaseActionFeedback` | /move_base | /interactive, /rosbag_record_node | Navigation / path planning topic |
| `/move_base/function_costmap/costmap` | `nav_msgs/OccupancyGrid` | /move_base |  | Navigation / path planning topic |
| `/move_base/function_costmap/costmap_updates` | `map_msgs/OccupancyGridUpdate` | /move_base |  | Navigation / path planning topic |
| `/move_base/function_costmap/elevator_layer/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/function_costmap/elevator_layer/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/function_costmap/footprint` | `geometry_msgs/PolygonStamped` | /move_base | /move_base | Navigation / path planning topic |
| `/move_base/function_costmap/gate_layer/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/function_costmap/gate_layer/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/function_costmap/motion_layer/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/function_costmap/motion_layer/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/function_costmap/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/function_costmap/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/global_costmap/costmap` | `nav_msgs/OccupancyGrid` | /move_base | /web_backend_node, /rosbag_record_node | Navigation / path planning topic |
| `/move_base/global_costmap/costmap/to_web` | `sensor_msgs/Image` | /web_backend_node |  | Navigation / path planning topic |
| `/move_base/global_costmap/costmap/to_web/compressed` | `sensor_msgs/CompressedImage` | /web_backend_node |  | Navigation / path planning topic |
| `/move_base/global_costmap/costmap/to_web/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /web_backend_node |  | Navigation / path planning topic |
| `/move_base/global_costmap/costmap/to_web/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /web_backend_node |  | Navigation / path planning topic |
| `/move_base/global_costmap/costmap_updates` | `map_msgs/OccupancyGridUpdate` | /move_base | /rosbag_record_node | Navigation / path planning topic |
| `/move_base/global_costmap/footprint` | `geometry_msgs/PolygonStamped` | /move_base | /move_base, /rosbag_record_node | Navigation / path planning topic |
| `/move_base/global_costmap/inflation_layer/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/global_costmap/inflation_layer/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/global_costmap/obstacle_layer/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/global_costmap/obstacle_layer/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/global_costmap/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/global_costmap/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/global_costmap/static_layer/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/global_costmap/static_layer/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/goal` | `keenon_move_base_msgs/MoveBaseActionGoal` | /interactive, /move_base | /move_base, /rosbag_record_node | Navigation / path planning topic |
| `/move_base/local_costmap/costmap` | `nav_msgs/OccupancyGrid` | /move_base | /web_backend_node, /rosbag_record_node | Navigation / path planning topic |
| `/move_base/local_costmap/costmap/to_web` | `sensor_msgs/Image` | /web_backend_node |  | Navigation / path planning topic |
| `/move_base/local_costmap/costmap/to_web/compressed` | `sensor_msgs/CompressedImage` | /web_backend_node |  | Navigation / path planning topic |
| `/move_base/local_costmap/costmap/to_web/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /web_backend_node |  | Navigation / path planning topic |
| `/move_base/local_costmap/costmap/to_web/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /web_backend_node |  | Navigation / path planning topic |
| `/move_base/local_costmap/costmap_updates` | `map_msgs/OccupancyGridUpdate` | /move_base | /web_backend_node, /rosbag_record_node | Navigation / path planning topic |
| `/move_base/local_costmap/footprint` | `geometry_msgs/PolygonStamped` | /move_base | /move_base, /rosbag_record_node | Navigation / path planning topic |
| `/move_base/local_costmap/inflation_layer/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/local_costmap/inflation_layer/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/local_costmap/obstacle_layer/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/local_costmap/obstacle_layer/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/local_costmap/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/local_costmap/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/local_costmap/virtual_wall/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/local_costmap/virtual_wall/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/move_base_global_plan` | `nav_msgs/Path` | /move_base | /rosbag_record_node | Navigation / path planning topic |
| `/move_base/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /move_base |  | Navigation / path planning topic |
| `/move_base/parameter_updates` | `dynamic_reconfigure/Config` | /move_base |  | Navigation / path planning topic |
| `/move_base/result` | `keenon_move_base_msgs/MoveBaseActionResult` | /move_base | /interactive, /rosbag_record_node | Navigation / path planning topic |
| `/move_base/status` | `actionlib_msgs/GoalStatusArray` | /move_base | /interactive, /rosbag_record_node | Navigation / path planning topic |
| `/move_base_simple/goal` | `geometry_msgs/PoseStamped` |  | /move_base, /rosbag_record_node | Navigation / path planning topic |
| `/movebaseActionDone` | `keenon_database_msgs/poseInfo` | /interactive |  |  |
| `/mx/cloud1` | `sensor_msgs/PointCloud2` |  | /move_base |  |
| `/mx/cloud2` | `sensor_msgs/PointCloud2` |  | /move_base |  |
| `/occupied_pub_cloud_point_` | `sensor_msgs/PointCloud2` | /peanut_localization_node |  |  |
| `/odom` | `nav_msgs/Odometry` |  | /coap_bridge_server, /move_base, /rosbag_record_node |  |
| `/odom_combined` | `nav_msgs/Odometry` | /chassis | /rosbag_record_node |  |
| `/partial_potential_map` | `nav_msgs/OccupancyGrid` | /move_base |  |  |
| `/particlecloud` | `unknown` |  | /rosbag_record_node |  |
| `/path_cost` | `nav_msgs/OccupancyGrid` | /move_base |  |  |
| `/path_cost_map` | `nav_msgs/OccupancyGrid` | /move_base |  |  |
| `/pending_map` | `nav_msgs/OccupancyGrid` | /move_base |  |  |
| `/planner_scan` | `sensor_msgs/LaserScan` | /multi_lidar_filter_for_planner | /move_base |  |
| `/pose_mac_address_cmd` | `std_msgs/String` | /interactive | /interactive |  |
| `/publish_line_markers` | `visualization_msgs/Marker` | /elevator_detection_node |  |  |
| `/reboot` | `std_msgs/Bool` |  | /web_backend_node, /rosbag_record_node |  |
| `/reference_pointcloud` | `sensor_msgs/PointCloud2` | /peanut_localization_node |  |  |
| `/reference_pointcloud_filtered` | `sensor_msgs/PointCloud2` | /peanut_localization_node |  |  |
| `/robot_current_floor` | `std_msgs/Int16` | /switch_map | /schedule_map_builder, /coap_bridge_server, /rosbridge_websocket, /rosbag_record_node |  |
| `/robot_elevator_percent` | `std_msgs/UInt8` | /move_base | /rosbag_record_node | Elevator passage coordination / communication |
| `/robot_pose` | `geometry_msgs/PoseStamped` |  | /schedule_map_builder, /rosbag_record_node |  |
| `/robot_state` | `web_backend/robot_state` | /web_backend_node | /rosbridge_websocket, /rosbag_record_node |  |
| `/rosout` | `rosgraph_msgs/Log` | /database, /elevator_detection_node, /location_lost_detecthion_node, /sensor_monitor_node, /robot_state_publisher, /tf2_web_republisher, /coap_bridge_server, /robot_pose_location_label_node, /gmapping_location_label_node, /front_end_node, /srf_node, /sdkeli_front, /sdkeli_back, /multi_lidar_filter_for_planner, /slam_gmapping, /interactive, /lora_driver, /move_base, /robot_settings, /camera_1/driver, /cartographer_occupancy_grid_node, /camera_1/depth_rectify_depth, /camera_1/depth_metric_rect, /camera_1/depth_metric, /camera_1/depth_points, /rosbridge_websocket, /control/rosbridge_websocket, /camera_1/camera_1_nodelet_manager, /camera_1_base_link, /camera_1_base_link1, /camera_1_base_link2, /camera_1_base_link3, /camera_2/driver, /camera_2/depth_rectify_depth, /camera_2/depth_metric_rect, /camera_2/depth_metric, /camera_2/depth_points, /camera_2/camera_2_nodelet_manager, /camera_2_base_link, /cartographer_node, /topo_mapper, /camera_2_base_link2, /camera_2_base_link1, /virtual_wall_generator, /switch_map, /camera_2_base_link3, /schedule_map_builder, /web_backend_node, /label_camera_node, /ros_label_fusion, /multi_goals_planner, /matching_task, /rosapi, /control/rosapi, /peanut_localization_node, /rosbag_record_node, /chassis, /multi_lidar_filter, /tf_monitor_1783603417662489982 | /keenonrosout, /rosbag_record_node |  |
| `/rosout_agg` | `rosgraph_msgs/Log` | /keenonrosout |  |  |
| `/run_amcl` | `unknown` |  | /rosbag_record_node |  |
| `/run_mapping` | `std_msgs/UInt8` | /web_backend_node | /robot_pose_location_label_node, /cartographer_occupancy_grid_node, /cartographer_node, /peanut_localization_node, /rosbag_record_node |  |
| `/run_rosbag` | `std_msgs/Bool` | /cartographer_node, /move_base | /interactive, /rosbag_record_node |  |
| `/save_new_map` | `std_msgs/Bool` |  | /slam_gmapping, /cartographer_node, /rosbag_record_node |  |
| `/scan` | `sensor_msgs/LaserScan` | /multi_lidar_filter | /elevator_detection_node, /web_backend_node, /matching_task, /sensor_monitor_node, /move_base, /rosbag_record_node |  |
| `/scan_back_orig` | `sensor_msgs/LaserScan` | /sdkeli_back | /multi_lidar_filter_for_planner, /rosbag_record_node, /multi_lidar_filter |  |
| `/scan_base_map` | `web_backend/PointArray` | /web_backend_node | /control/rosbridge_websocket |  |
| `/scan_front_orig` | `sensor_msgs/LaserScan` | /sdkeli_front | /multi_lidar_filter_for_planner, /rosbag_record_node, /multi_lidar_filter |  |
| `/scan_orig` | `sensor_msgs/LaserScan` | /multi_lidar_filter_for_planner, /multi_lidar_filter | /srf_node, /peanut_localization_node, /rosbag_record_node |  |
| `/scan_pointcloud_filtered` | `sensor_msgs/PointCloud2` | /peanut_localization_node |  |  |
| `/schedule_feedback` | `keenon_schedule_msgs/scheduleCmd` |  | /interactive |  |
| `/schedule_path` | `geometry_msgs/PoseArray` |  | /schedule_map_builder, /rosbag_record_node |  |
| `/schedule_path_test` | `std_msgs/UInt32MultiArray` |  | /schedule_map_builder |  |
| `/schedule_speed_ctl` | `geometry_msgs/Twist` |  | /move_base, /rosbag_record_node |  |
| `/schedule_state` | `std_msgs/Bool` | /schedule_map_builder | /move_base, /rosbag_record_node |  |
| `/schedule_sw_state` | `std_msgs/Bool` | /coap_bridge_server | /interactive |  |
| `/sdkeli_back/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /sdkeli_back |  | Rear LiDAR scanner driver topic |
| `/sdkeli_back/parameter_updates` | `dynamic_reconfigure/Config` | /sdkeli_back |  | Rear LiDAR scanner driver topic |
| `/sdkeli_front/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /sdkeli_front |  | Front LiDAR scanner driver topic |
| `/sdkeli_front/parameter_updates` | `dynamic_reconfigure/Config` | /sdkeli_front |  | Front LiDAR scanner driver topic |
| `/seller_fake_goal` | `std_msgs/UInt8` |  | /matching_task, /rosbag_record_node |  |
| `/seller_report_toUI` | `std_msgs/UInt8` | /interactive | /coap_bridge_server, /rosbag_record_node |  |
| `/seller_request` | `std_msgs/UInt8` | /coap_bridge_server | /interactive, /rosbag_record_node |  |
| `/seller_task/cancel` | `actionlib_msgs/GoalID` | /interactive | /matching_task, /rosbag_record_node |  |
| `/seller_task/feedback` | `keenon_seller_msgs/SellerTaskActionFeedback` | /matching_task | /interactive, /rosbag_record_node |  |
| `/seller_task/goal` | `keenon_seller_msgs/SellerTaskActionGoal` | /matching_task, /interactive | /matching_task, /rosbag_record_node |  |
| `/seller_task/result` | `keenon_seller_msgs/SellerTaskActionResult` | /matching_task | /interactive, /rosbag_record_node |  |
| `/seller_task/status` | `actionlib_msgs/GoalStatusArray` | /matching_task | /interactive, /rosbag_record_node |  |
| `/set_block_state_duration` | `std_msgs/Int16` | /coap_bridge_server | /move_base, /rosbag_record_node |  |
| `/shortest_path_activate` | `std_msgs/Int8` | /coap_bridge_server | /move_base, /rosbag_record_node |  |
| `/stm32_down` | `std_msgs/String` | /coap_bridge_server | /chassis |  |
| `/stm32_up` | `std_msgs/String` | /chassis | /coap_bridge_server |  |
| `/stm32_version` | `std_msgs/String` | /chassis | /coap_bridge_server, /rosbag_record_node |  |
| `/suspend_obs_cloud_left` | `unknown` |  | /rosbag_record_node |  |
| `/suspend_obs_cloud_right` | `unknown` |  | /rosbag_record_node |  |
| `/test_cloud` | `sensor_msgs/PointCloud` | /location_lost_detecthion_node |  |  |
| `/test_virtual_wall_1` | `nav_msgs/OccupancyGrid` | /move_base |  |  |
| `/test_virtual_wall_2` | `nav_msgs/OccupancyGrid` | /move_base |  |  |
| `/tf` | `tf2_msgs/TFMessage` | /robot_state_publisher, /front_end_node, /gmapping_location_label_node, /camera_1_base_link, /camera_1_base_link2, /camera_1_base_link1, /camera_1_base_link3, /camera_2_base_link, /camera_2_base_link1, /camera_2_base_link2, /camera_2_base_link3, /label_camera_node, /peanut_localization_node, /chassis | /elevator_detection_node, /location_lost_detecthion_node, /tf2_web_republisher, /robot_pose_location_label_node, /gmapping_location_label_node, /multi_lidar_filter_for_planner, /interactive, /move_base, /front_end_node, /switch_map, /schedule_map_builder, /web_backend_node, /label_camera_node, /matching_task, /peanut_localization_node, /rosbag_record_node, /chassis, /multi_lidar_filter, /tf_monitor_1783603417662489982 |  |
| `/tf2_web_republisher/cancel` | `actionlib_msgs/GoalID` | /rosbridge_websocket, /control/rosbridge_websocket | /tf2_web_republisher |  |
| `/tf2_web_republisher/feedback` | `tf2_web_republisher/TFSubscriptionActionFeedback` | /tf2_web_republisher | /rosbridge_websocket, /control/rosbridge_websocket |  |
| `/tf2_web_republisher/goal` | `tf2_web_republisher/TFSubscriptionActionGoal` | /rosbridge_websocket, /control/rosbridge_websocket | /tf2_web_republisher |  |
| `/tf2_web_republisher/result` | `tf2_web_republisher/TFSubscriptionActionResult` | /tf2_web_republisher |  |  |
| `/tf2_web_republisher/status` | `actionlib_msgs/GoalStatusArray` | /tf2_web_republisher |  |  |
| `/tf2_web_republisher/tf_repub_0` | `tf2_web_republisher/TFArray` | /tf2_web_republisher | /rosbridge_websocket |  |
| `/tf2_web_republisher/tf_repub_1` | `tf2_web_republisher/TFArray` | /tf2_web_republisher | /control/rosbridge_websocket |  |
| `/tf_static` | `tf2_msgs/TFMessage` | /robot_state_publisher, /cartographer_node | /elevator_detection_node, /location_lost_detecthion_node, /tf2_web_republisher, /robot_pose_location_label_node, /gmapping_location_label_node, /multi_lidar_filter_for_planner, /interactive, /move_base, /front_end_node, /switch_map, /schedule_map_builder, /web_backend_node, /label_camera_node, /matching_task, /peanut_localization_node, /rosbag_record_node, /chassis, /multi_lidar_filter, /tf_monitor_1783603417662489982 |  |
| `/topo_action/cancel` | `actionlib_msgs/GoalID` |  | /topo_mapper |  |
| `/topo_action/feedback` | `keenon_schedule_msgs/topuMapActActionFeedback` | /topo_mapper |  |  |
| `/topo_action/goal` | `keenon_schedule_msgs/topuMapActActionGoal` |  | /topo_mapper |  |
| `/topo_action/result` | `keenon_schedule_msgs/topuMapActActionResult` | /topo_mapper |  |  |
| `/topo_action/status` | `actionlib_msgs/GoalStatusArray` | /topo_mapper |  |  |
| `/ui_command_topic` | `std_msgs/UInt64` | /interactive |  |  |
| `/uknow_pub_cloud` | `sensor_msgs/PointCloud2` | /peanut_localization_node |  |  |
| `/uknow_space_pub_cloud_point_` | `sensor_msgs/PointCloud2` | /peanut_localization_node |  |  |
| `/urgency_button_status` | `std_msgs/Bool` | /chassis | /coap_bridge_server, /move_base, /rosbag_record_node |  |
| `/urgency_stop` | `std_msgs/Float64` | /chassis | /matching_task, /move_base, /rosbag_record_node |  |
| `/use_label_location` | `std_msgs/Bool` | /robot_pose_location_label_node |  |  |
| `/vel_map` | `nav_msgs/OccupancyGrid` | /switch_map | /move_base, /rosbag_record_node |  |
| `/version` | `keenon_database_msgs/version` | /database, /interactive | /coap_bridge_server, /rosbag_record_node |  |
| `/virtual_wall` | `nav_msgs/OccupancyGrid` | /switch_map | /matching_task, /web_backend_node, /move_base, /rosbag_record_node |  |
| `/virtual_wall/to_web` | `sensor_msgs/Image` | /web_backend_node |  |  |
| `/virtual_wall/to_web/compressed` | `sensor_msgs/CompressedImage` | /web_backend_node |  |  |
| `/virtual_wall/to_web/compressed/parameter_descriptions` | `dynamic_reconfigure/ConfigDescription` | /web_backend_node |  |  |
| `/virtual_wall/to_web/compressed/parameter_updates` | `dynamic_reconfigure/Config` | /web_backend_node |  |  |
| `/virtual_wall_1` | `nav_msgs/OccupancyGrid` | /schedule_map_builder |  |  |
| `/virtual_wall_updates` | `map_msgs/OccupancyGridUpdate` | /schedule_map_builder | /move_base |  |
| `/welcome` | `std_msgs/UInt8` |  | /coap_bridge_server, /rosbag_record_node |  |
| `/whole_potential_map` | `nav_msgs/OccupancyGrid` | /move_base |  |  |
