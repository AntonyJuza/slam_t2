# Move Base Node (`move_base`)

## Verification Status
| Status | Items |
| :--- | :--- |
| **✅ Verified** | Running node `/move_base` (PID 34393). Active subscriptions to sensor inputs (`/scan`, `/planner_scan`, `/camera_1/depth/points`, `/camera_2/depth/points`, `/bump`), layers (`/map`, `/virtual_wall`, `/elevator_map`, `/vel_map`, `/gate_map`), control (`/move_base/goal`, `/move_base/cancel`), and output `/cmd_vel` confirmed via `rosnode info`. Timed Elastic Band local planner parameters loaded. |
| **🟡 Inferred** | `kplanner/KPlannerROS` global path planning behavior and restricted speed zone costmap triggers (inferred from parameters and node connections, but not tested in all edge cases). |
| **🔴 Unknown** | Exact elevator safety obstacle verification logic and human leg cluster tracking algorithms. |

## Purpose
The `move_base` node manages path planning, obstacle avoidance, costmap maintenance, and velocity command generation. It hosts a global planner to generate paths to waypoints and a local planner to handle dynamic obstacle avoidance, guide the robot through narrow spaces (such as elevators), and control speed zones.

---

## Executable
* **Binary Path:** `/opt/ros/indigo/lib/move_base/move_base`
* **Package Name:** `move_base`
* **Node Name:** `/move_base`

---

## Launch File
* **Path:** `OpenT2/launch/include/move_base_teb.launch`
* **Parameter Files Loaded:** 
  * `OpenT2/parameters/T2/move_base_params.yaml`
  * `OpenT2/parameters/T2/costmap_common_params.yaml` (namespaced to `global_costmap`, `local_costmap`, `function_costmap`)
  * `OpenT2/parameters/T2/local_costmap_params.yaml`
  * `OpenT2/parameters/T2/global_costmap_params.yaml`
  * `OpenT2/parameters/T2/function_costmap_params.yaml`
  * `OpenT2/parameters/T2/teb_local_planner_params.yaml`

---

## Parameters

### Planners
* **Global Planner (`base_global_planner`):** `kplanner/KPlannerROS` (Keenon's custom grid/topological planner).
* **Local Planner (`base_local_planner`):** `teb_local_planner/TebLocalPlannerROS` (Timed Elastic Band local planner).

### General Settings (`move_base_params.yaml`)
* `controller_frequency:` `20.0` Hz.
* `controller_patiente:` `15.0` seconds (Wait time before recovery behavior triggers).
* `allow_location_fail_move:` `false` (Robot will immediately stop moving if localization is lost).
* `pause_costmaps:` `true` (Pauses costmap updates when the robot is idle/docked).

### Motion Limits (`teb_local_planner_params.yaml`)
* `max_vel_x:` `0.8` m/s (Maximum forward speed).
* `max_vel_x_backwards:` `0.8` m/s (Maximum backward speed).
* `low_speed_vel_x:` `0.5` m/s (Speed in restricted speed zones).
* `elev_mode_vel_x:` `0.5` m/s (Speed when entering/exiting elevators).
* `max_vel_theta:` `0.6` rad/s (Maximum pivot turning speed).
* `low_speed_vel_theta:` `1.0` rad/s (Higher turning speed in low-speed zones for pivots).
* `acc_lim_x:` `0.4` m/s² (Maximum linear acceleration).
* `deceleration_lim_x:` `0.7` m/s² (Maximum linear deceleration).
* `elev_mode_acc_x:` `0.2` m/s² (Reduced acceleration for elevator maneuvers).
* `acc_lim_theta:` `0.6` rad/s²
* `deceleration_lim_theta:` `0.6` rad/s²

### Footprint Model
* **Type:** `multi_circles`
* **Circles:** 6 overlapping circles representing the physical dimensions:
  `[[0.18875, 0.12625, 0.12625], [0.18875, -0.12625, 0.12625], [-0.18875, 0.12625, 0.12625], [-0.18875, -0.12625, 0.12625], [0.0625, 0.0, 0.2525], [-0.0625, 0.0, 0.2525]]`
* **Static Footprint Polygon:** 8 vertices:
  `[[0.3150, 0.2125], [0.2750, 0.2525], [-0.2750, 0.2525], [-0.3150, 0.2125], [-0.3150, -0.2125], [-0.2750, -0.2525], [0.2750, -0.2525], [0.3150, -0.2125]]` (approx. $0.63\text{ m}$ length $\times$ $0.505\text{ m}$ width).

### Costmaps (`local_costmap_params.yaml`, `global_costmap_params.yaml`)
* **Local Costmap:** Global frame: `odom`, width: $4.0\text{ m}$, height: $4.0\text{ m}$, resolution: $0.03\text{ m}$.
  * **Layers:** `static_layer` (Virtual Walls), `obstacle_layer` (2D Lidar, PointClouds), `inflation_layer` (radius: $0.5\text{ m}$).
* **Global Costmap:** Global frame: `map`, resolution: $0.05\text{ m}$.
  * **Layers:** `static_layer` (Static grid map - disabled on active path planning), `obstacle_layer` (Planner scan, bump, foot, mx cameras), `inflation_layer` (radius: $1.5\text{ m}$).

---

## Subscribed Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/move_base_simple/goal` | `geometry_msgs/PoseStamped` | Simple target goal pose from Rviz or scripts. |
| `/move_base/goal` | `move_base_msgs/MoveBaseActionGoal` | Target action server goal from UI/Android app. |
| `/scan` | `sensor_msgs/LaserScan` | Merged and filtered laser scan used for local costmap updates. |
| `/planner_scan` | `sensor_msgs/LaserScan` | Filtered scan with wider parameters for global costmap updates. |
| `/camera_1/depth/points` | `sensor_msgs/PointCloud2` | Front Intel RealSense depth camera pointcloud. |
| `/camera_2/depth/points` | `sensor_msgs/PointCloud2` | Rear Intel RealSense depth camera pointcloud. |
| `/mx/cloud1` / `/mx/cloud2` | `sensor_msgs/PointCloud2` | Side/accessory depth cameras. |
| `/bump` | `sensor_msgs/PointCloud2` | Point cloud representing physical bumper hit coordinates. |
| `/virtual_wall` | `nav_msgs/OccupancyGrid` | Grid layer representing virtual walls. |
| `/gate_map` | `nav_msgs/OccupancyGrid` | Grid layer representing automatic doors/gates. |
| `/elevator_map` | `nav_msgs/OccupancyGrid` | Grid layer containing elevator regions. |
| `/vel_map` | `nav_msgs/OccupancyGrid` | Grid layer outlining restricted speed zones. |
| `/feature_detection_node/pairs_leg_cloud` | `sensor_msgs/PointCloud` | Human legs detected for safety stopping. |
| `/tf` & `/tf_static` | `tf2_msgs/TFMessage` | Frame transforms. |

---

## Published Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/cmd_vel` | `geometry_msgs/Twist` | Linear and angular velocity outputs sent to the `/chassis` node. |
| `/move_base/global_costmap/costmap` | `nav_msgs/OccupancyGrid` | Visualization of the global planning costmap. |
| `/move_base/local_costmap/costmap` | `nav_msgs/OccupancyGrid` | Visualization of the local planning costmap. |
| `/move_base/current_goal` | `geometry_msgs/PoseStamped` | Current target coordinates. |
| `/move_base/feedback` | `move_base_msgs/MoveBaseActionFeedback` | Action feedback (current pose, status). |
| `/move_base/result` | `move_base_msgs/MoveBaseActionResult` | Action results (success, failure code). |
| `/move_base/status` | `actionlib_msgs/GoalStatusArray` | Active goal state. |

---

## Services

* Standard ROS Move Base services:
  * `/move_base/make_plan` (`nav_msgs/GetPlan`)
  * `/move_base/clear_costmaps` (`std_srvs/Empty`)
* `/move_base/get_loggers` / `/move_base/set_logger_level`

---

## TF
* **Listener:** Expects the complete TF chain from `map` -> `odom` -> `base_link` as well as the relative sensor coordinate frames (`laser_link`, `camera_1_link`, etc.).

---

## Dependencies
* **Libraries:** `move_base`, `costmap_2d`, `teb_local_planner`
* **Custom Packages:** `kplanner` (proprietary global path planner)

---

## Known Issues
1. **Spelling Mistake:** Parameter `controller_patiente` is used instead of `controller_patience`. Setting the standard parameter will be ignored by this binary.

---

## Reverse Engineered Notes
* **Elevator Logic:** Incorporates built-in state transitions when interacting with elevators. Uses `elevator_move_in_overtime` (5.0s), `elevator_open_wait_overtime` (10.0s), and `elevator_length` (1.6m) to slow down, plan specific center-aligned trajectories, detect if elevator is crowded using depth cameras (`use_elevator_crowd_detector: true`), and wait for door openings.
* **Automatic Gate Control:** Subscribes to the `/gate_map` to check for wireless automatic gates. When approaching a gate within `open_gate_distance` (2.0m), it signals the system to trigger gate open commands, waiting up to `open_gate_overtime` (20.0s).
