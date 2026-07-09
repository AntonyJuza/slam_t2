# Cartographer Node (`cartographer_node`)

## Purpose
The `cartographer_node` provides 2D SLAM (Simultaneous Localization and Mapping) back-end services. It constructs planar submaps by registering laser range scans and wheel odometry, performs loop closure optimization, and exports map trajectory databases (in `.pbstream` format) that are subsequently stored in the SQLite system database.

---

## Executable
* **Binary Path:** `/opt/ros/indigo/lib/cartographer_ros/cartographer_node`
* **Package Name:** `cartographer_ros`
* **Node Name:** `/cartographer_node`

---

## Launch File
* **Path:** `OpenT2/launch/include/cartographer.launch`
* **Lua Configuration File:** `OpenT2/parameters/cartographer_ros/keenon_T2.lua`

```xml
<?xml version="1.0"?>
<launch>
    <arg name="OUTPUT_METHOD" default="screen"/>
    <arg name="RESPAWN" default="false"/>
    <arg name="ROBOT_TYPE" default="peanut"/>

    <node name="cartographer_node" pkg="cartographer_ros" type="cartographer_node" 
          args="-configuration_directory $(find robot_settings)/cfg/cartographer_ros 
                -configuration_basename keenon_$(arg ROBOT_TYPE).lua"
          respawn="$(arg RESPAWN)" output="$(arg OUTPUT_METHOD)">
        <remap from="odom" to="odom_combined"/>
        <remap from="scan_1" to="scan_front_orig"/>
        <remap from="scan_2" to="scan_back_orig"/>
    </node>

    <node name="cartographer_occupancy_grid_node" pkg="cartographer_ros" type="cartographer_occupancy_grid_node" args="-resolution 0.05" />
</launch>
```

---

## Parameters (Lua Configuration)

Key configurations extracted from `keenon_T2.lua`:
* `map_frame:` `"map"`
* `tracking_frame:` `"base_link"`
* `published_frame:` `"odom"`
* `odom_frame:` `"odom"`
* `provide_odom_frame:` `false`
* `use_odometry:` `true` (enables wheel odometry integration)
* `use_nav_sat:` `false`
* `use_landmarks:` `false`
* `num_laser_scans:` `2` (Directly consumes separate front and rear lidar streams)
* `num_multi_echo_laser_scans:` `0`
* `num_subdivisions_per_laser_scan:` `1`
* `num_point_clouds:` `0`
* `TRAJECTORY_BUILDER_2D.num_accumulated_range_data = 2` (Collects scans from both lidars before inserting into submaps)
* `TRAJECTORY_BUILDER_2D.use_imu_data = false` (Disables IMU in 2D mapping to avoid pitch/roll noise)
* `TRAJECTORY_BUILDER_2D.min_range = 0.1` m
* `TRAJECTORY_BUILDER_2D.max_range = 25.0` m
* `POSE_GRAPH.optimize_every_n_nodes = 10`
* `POSE_GRAPH.constraint_builder.min_score = 0.65` (Minimum score for loop closure constraint acceptance)
* `POSE_GRAPH.constraint_builder.global_localization_min_score = 0.65`

---

## Subscribed Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/scan_front_orig` | `sensor_msgs/LaserScan` | Remapped to `scan_1` (front lidar scanner). |
| `/scan_back_orig` | `sensor_msgs/LaserScan` | Remapped to `scan_2` (rear lidar scanner). |
| `/odom_combined` | `geometry_msgs/PoseWithCovarianceStamped` | Remapped to `odom` (fused wheel odometry). |
| `/run_mapping` | `std_msgs/UInt8` | Triggers cartographer to start or stop mapping. |
| `/save_new_map` | StdSrvs/Empty style | Topic command to trigger serialization of the active map. |
| `/tf` & `/tf_static` | `tf2_msgs/TFMessage` | Frame transforms. |

---

## Published Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/submap_list` | `cartographer_ros_msgs/SubmapList` | List of active submaps. |
| `/mapping_status`| `std_msgs/UInt8` | Reports mapping state to the web backend. |
| `/run_rosbag` | `std_msgs/Bool` | Signal to start/stop rosbag logging of sensor data during mapping. |
| `/tf` | `tf2_msgs/TFMessage` | Broadcasts `map` -> `odom` dynamic transform *only* during active mapping. |

---

## Services

* `/operate_pbstream` (Custom serialization service to load/save `.pbstream` map databases).
* `/cartographer_node/get_loggers` / `/cartographer_node/set_logger_level`

---

## TF
* **Broadcaster:** Dynamically broadcasts the `map` -> `odom` transform *only* when actively running a mapping trajectory.
* **Listener:** Subscribes to `/tf` static frames (`base_link` -> `laser_front_link` and `laser_back_link`).

---

## Dependencies
* **Libraries:** `cartographer`, `cartographer_ros`.

---

## Known Issues
1. **CPU Saturation:** Loop closure optimization can lead to high CPU peaks. Real-time trajectory generation may stutter if the onboard single board computer is overloaded.

---

## Reverse Engineered Notes
* **Idle State:** When not mapping, `cartographer_node` disconnects its sensor subscriptions to free CPU cycles.
* **Dual Scan Accumulation:** Cartographer is configured with `num_accumulated_range_data = 2` and `num_laser_scans = 2` to register the front and rear lidars in lockstep. This allows the mapping process to see all directions simultaneously, preventing loop closure distortion when the robot makes sharp turns.
* **Database Serialization:** The generated `.pbstream` containing the optimized pose graph is saved under the `/map` table of `/etc/ros/runtime/database/peanut.db` as a BLOB entry of type `carto_map`.
