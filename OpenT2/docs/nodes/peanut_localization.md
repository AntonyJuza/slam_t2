# Peanut Localization Node (`peanut_localization_node`)

## Purpose
The `peanut_localization_node` is the primary localization engine of the robot during active deliveries. It subscribes to the merged raw laser scans (`/scan_orig`) and aligns them against the static grid map using a modular, high-precision 2D Iterative Closest Point (ICP) scan matcher, broadcasting the dynamic `map` -> `odom` coordinate transform.

---

## Executable
* **Binary Path:** `/opt/ros/indigo/lib/peanut_localization/peanut_localization_node`
* **Package Name:** `peanut_localization`
* **Node Name:** `/peanut_localization_node`

---

## Launch File
* **Path:** `OpenT2/launch/include/peanut_localization.launch`
* **Parameter Files Loaded:**
  * `OpenT2/parameters/peanut_localization/location_common/common.yaml`
  * `OpenT2/parameters/peanut_localization/filters/filters_2d.yaml`
  * `OpenT2/parameters/peanut_localization/pose_estimation/initial_pose_estimation_large_map_2d.yaml`
  * `OpenT2/parameters/peanut_localization/pose_tracking/cluttered_environments_dynamic_fast_2d.yaml`
  * `OpenT2/parameters/peanut_localization/pose_recovery/recovery_2d.yaml`

---

## Parameters

### Voxel Filtering (`filters_2d.yaml`)
* **Reference Point Cloud (Map):** Downsampled with a leaf size of $0.1\text{ m} \times 0.1\text{ m} \times 0.1\text{ m}$. Height filter limit: $-0.001\text{ m}$ to $1.8\text{ m}$.
* **Scan Point Cloud (Lidar):** Downsampled with a leaf size of $0.02\text{ m} \times 0.02\text{ m} \times 0.02\text{ m}$. Height filter limit: $-0.001\text{ m}$ to $1.8\text{ m}$.

### Scan Matching (ICP Tracking) (`cluttered_environments_dynamic_fast_2d.yaml`)
* `convergence_time_limit_seconds:` `0.05` s.
* `max_correspondence_distance:` `0.1` m (Limits scan search to nearby boundaries to minimize CPU load).
* `max_number_of_registration_iterations:` `20`.
* `ransac_outlier_rejection_threshold:` `0.10` m.
* `rotation_epsilon:` `0.00002` rad.
* `maximum_optimizer_iterations:` `10`.

### Scan Matching (ICP Recovery Mode) (`recovery_2d.yaml`)
* `max_correspondence_distance:` `2.5` m (Wider search window to search for matching boundaries when lost).
* `max_number_of_registration_iterations:` `80`.
* `maximum_optimizer_iterations:` `100`.

### Validation Thresholds (`cluttered_environments_dynamic_fast_2d.yaml`)
* `max_transformation_angle:` `1.2` rad.
* `max_transformation_distance:` `0.8` m.
* `max_root_mean_square_error:` `0.25`.
* `max_outliers_percentage:` `0.6` (Triggers recovery mode if more than $60\%$ of laser points are outliers).

---

## Subscribed Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/scan_orig` | `sensor_msgs/LaserScan` | Raw merged laser scans before obstacle/footprint filtering ($28\text{ Hz}$). |
| `/map` | `nav_msgs/OccupancyGrid` | Global static map of the current floor from `/switch_map`. |
| `/initialpose` | `geometry_msgs/PoseWithCovarianceStamped` | Manual/automatic initial pose overrides. |
| `/elev_pos_state` / `/elev_process_signal` | Custom | Elevator location cues used to transition localization states during floor changes. |
| `/run_mapping` | `std_msgs/UInt8` | Disables localization updates when active mapping is running. |
| `/charge_state_fromSTM32` | `keenon_charge_msgs/ChargeFB` | State feedback from the charging contacts. |
| `/tf` & `/tf_static` | `tf2_msgs/TFMessage` | Frame transforms. |

---

## Published Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/localization/robot_pose` | `geometry_msgs/PoseWithCovarianceStamped` | Estimated global pose of the robot on the map. |
| `/tf` | `tf2_msgs/TFMessage` | Broadcasts the dynamic `map` -> `odom` coordinate transform. |
| `/gauss_cloud_point` | `sensor_msgs/PointCloud2` | Point cloud visualization of the laser matches. |
| `/aligned_pointcloud_inliers` | `sensor_msgs/PointCloud2` | Points that successfully matched the map. |
| `/aligned_pointcloud_outliers`| `sensor_msgs/PointCloud2` | Points that failed to match the map (moving obstacles, changes). |
| `/reference_pointcloud` | `sensor_msgs/PointCloud2` | The local slice of the static map. |
| `/localization/map_check` | `std_msgs/Header` | Heartbeat/diagnostic packet. |

---

## Services

* `/localization/set_pose` (Directly sets the current robot pose coordinate).
* `/localization/better_location` (Triggers intensive pose optimization).
* `/localization/label_pose_check` (Verifies pose against waypoint labels).
* `/peanut_localization_node/get_loggers` / `/peanut_localization_node/set_logger_level`

---

## TF
* **Broadcaster:** Broadcasts the dynamic `map` -> `odom` coordinate transform at $\approx 50\text{ Hz}$.
* **Listener:** Expects the dynamic transform `odom` -> `base_link` (from `/front_end_node`) and sensor link offsets.

---

## Dependencies
* **Nodes:**
  * `/switch_map` (Provides the static occupancy grid `/map`).
  * `/front_end_node` (Provides the fused odometry transform `odom` -> `base_link`).

---

## Known Issues
1. **CPU Peaks during Recovery:** Entering recovery mode triggers intensive ICP searches ($2.5\text{ m}$ correspondence window, up to 100 iterations), which can spike CPU core usage.

---

## Reverse Engineered Notes
* **Dual-Rate Matcher:** Normal tracking operates with a very narrow window (`max_correspondence_distance: 0.1` m) to stay lightweight and real-time. If the match quality drops (e.g. RMSE $> 0.25$, outliers $> 60\%$), it triggers recovery mode with a larger search radius (`2.5` m) to snap back.
* **Persistent Pose Cache:** At startup or shutdown, the estimated pose is cached inside `/etc/ros/runtime/pose/init_pose.json` to allow the robot to recover its position upon reboot.
* **Charging Dock Alignment:** Uses charging pile reflector positions to perform sub-centimeter localization refinement when docking.
