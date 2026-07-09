# Front End Node (`front_end_node`)

## Verification Status
| Status | Items |
| :--- | :--- |
| **✅ Verified** | Running node `/front_end_node` (PID 2878). Subscriptions to `/chassis_imu_data`, `/encoder_raw`, `/tf`, `/tf_static`, and `/laser_odom` (published by `/srf_node`). Dynamic broadcasting of the `odom` -> `base_link` transform at $\approx 50\text{ Hz}$. Config load from YAML. |
| **🟡 Inferred** | Extended Kalman Filter covariance matrices and noise model scaling (inferred from launch configurations and EKF structure). |
| **🔴 Unknown** | Exact internal calibration offsets applied to encoder ticks prior to EKF ingestion. |

## Purpose
The `front_end_node` acts as the primary sensor fusion and odometry estimator. It fuses high-frequency encoder counts, raw IMU accelerometer/gyroscope signals, and planar scan matcher odometry (`/laser_odom`) using an Extended Kalman Filter (EKF) to broadcast the dynamic `odom` -> `base_link` coordinate frame transform.

---

## Executable
* **Binary Path:** `/opt/ros/indigo/lib/robot_location/front_end_node`
* **Package Name:** `robot_location`
* **Node Name:** `/front_end_node`

---

## Launch File
* **Path:** `OpenT2/launch/robot_location/robot_location.launch`
* **Parameter File Loaded:** `OpenT2/launch/robot_location/common_FrontEnd.yaml`

```yaml
odom_frame_id: odom
base_frame_id: base_link
laser_odom_frame_id: srf
encoder_topic: /encoder_raw
imu_topic: /chassis_imu_data
laser_odom_topic: /laser_odom
laser_scan_topic: /scan_orig
imu_hz: 50.0
encoder_hz: 50.0
laser_hz: 30.0
```

---

## Parameters

| Parameter | Type | Value | Description |
| :--- | :--- | :--- | :--- |
| `odom_frame_id` | String | `odom` | The parent coordinate frame name. |
| `base_frame_id` | String | `base_link` | The child coordinate frame name (robot center). |
| `laser_odom_frame_id` | String | `srf` | Frame ID for laser-scan match odometry. |
| `encoder_topic` | String | `/encoder_raw` | Topic containing raw wheel encoder counts. |
| `imu_topic` | String | `/chassis_imu_data` | Topic containing IMU readings. |
| `laser_odom_topic` | String | `/laser_odom` | Topic containing the planar scan matcher odometry. |
| `laser_scan_topic` | String | `/scan_orig` | Raw merged laser scans before obstacle/footprint filtering. |
| `imu_hz` | Double | `50.0` | Expected IMU message frequency. |
| `encoder_hz` | Double | `50.0` | Expected encoder message frequency. |
| `laser_hz` | Double | `30.0` | Expected laser scan matcher update rate. |

---

## Subscribed Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/encoder_raw` | `keenon_motor_msgs/encoder` | Wheel encoder ticks from the `/chassis` node. |
| `/chassis_imu_data` | `sensor_msgs/Imu` | IMU measurements from the `/chassis` node. |
| `/laser_odom` | `sensor_msgs/Imu` / Custom | Planar odometry calculated from laser scan matching. |
| `/tf` & `/tf_static` | `tf2_msgs/TFMessage` | Frame transforms. |

---

## Published Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/tf` | `tf2_msgs/TFMessage` | Dynamic coordinate transform from `odom` -> `base_link`. |

---

## Services

* `/front_end_node/get_loggers`
* `/front_end_node/set_logger_level`

---

## TF
* **Broadcaster:** Dynamically broadcasts the `odom` -> `base_link` coordinate frame transform at $\approx 50\text{ Hz}$.
* **Listener:** Synchronizes timestamps across `/tf` inputs.

---

## Dependencies
* **Nodes:**
  * `/chassis` (Provides `/encoder_raw` and `/chassis_imu_data`).
  * `/srf_node` (Planar laser scan matcher which publishes `/laser_odom`).

---

## Known Issues
1. **Featureless Drift:** In long corridors, if the planar scan matcher (`srf_node`) fails to find environmental features, the Kalman filter relies heavily on wheel encoders, leading to drift along the travel axis.
2. **Timing Jitter:** Requires stable timestamps from the STM32 board via the chassis serial stream to prevent EKF covariance inflation.

---

## Reverse Engineered Notes
* Implements a custom Extended Kalman Filter (EKF).
* Leverages high-frequency IMU angular velocity to filter out wheel slippage, and uses planar laser scan matching (`/laser_odom`) to correct long-term wheel odometry integration drift.
* Keeps the odometry frame highly responsive for move_base local planning.
