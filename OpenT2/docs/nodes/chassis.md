# Chassis Node (`chassis`)

## Purpose
The `chassis` node acts as the hardware abstraction layer and interface to the physical robot chassis. It handles bidirectional communication with the STM32 board to control the wheel motors, read encoders, retrieve IMU measurements, report safety sensors (bumpers, infrared beams), monitor battery/power state, and control automatic charging.

---

## Executable
* **Binary Path:** `/opt/ros/indigo/lib/chassis/chassis`
* **Package Name:** `chassis`
* **Node Name:** `/chassis`

---

## Launch File
* **Path:** `OpenT2/launch/include/chassis.launch`
* **Parameter File Loaded:** `OpenT2/parameters/T2/chassis_params.yaml`

```xml
<?xml version="1.0"?>
<launch>
    <arg name="OUTPUT_METHOD" default="screen"/>
    <arg name="RESPAWN" default="false"/>
    <arg name="ROBOT_TYPE" default="peanut"/>

    <node pkg="chassis" type="chassis" name="chassis" respawn="$(arg RESPAWN)" output="$(arg OUTPUT_METHOD)">
        <rosparam file="$(find robot_settings)/cfg/yaml/$(arg ROBOT_TYPE)/chassis_params.yaml" command="load"/>
    </node>
</launch>
```

---

## Parameters

| Parameter | Type | Value | Description |
| :--- | :--- | :--- | :--- |
| `port` | String | `/dev/ttyUSBStm32` | Serial port mapping for connection to the STM32 microcontroller. |
| `send_transform` | Boolean | `true` | Enables TF broadcasting (typically bypassed or disabled in runtime to prevent conflicts with `front_end_node`). |
| `max_acc` | Double | `0.32` | Maximum linear acceleration limit ($m/s^2$). |
| `use_imu` | Boolean | `false` | Disable use of a external standalone IMU. |
| `use_stm32_imu` | Boolean | `true` | Enable retrieving IMU data directly integrated on the STM32 board. |
| `mileage_record_filepath`| String | `mileage_record`| Filepath for recording the total physical mileage of the robot. |
| `bothsides_bump` | Boolean | `true` | Enables bumper detection events on both front/rear edges. |
| `size_sonar` | Integer | `0` | Number of sonar sensors connected (disabled). |
| `size_psd` | Integer | `0` | Number of PSD proximity sensors connected (disabled). |
| `scan_topic` | String | `/scan` | Primary laser scan topic to reference for safety. |
| `wheel_gauge` | Double | `366.0` | Outer distance between driving wheels in millimeters ($0.366\text{ m}$). |
| `wheel_perimeter` | Double | `517.2` | Perimeter of the driving wheel in millimeters ($0.5172\text{ m}$). |
| `imu_expect_rate` | Double | `40.0` | Expected update rate of IMU data packets from the STM32 (Hz). |

---

## Subscribed Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/cmd_vel` | `geometry_msgs/Twist` | Linear and angular target velocity commands. |
| `/charge_cmd_toSTM32` | `keenon_charge_msgs/ChargeCmd` | Target command to trigger/stop automatic charging docking. |
| `/motor_lock` | `std_msgs/Bool` | Locks or unlocks wheel motors (used to lock wheels when stationary or during errors). |
| `/enable_urgency_button`| `std_msgs/Bool` | Enables or disables physical emergency stop button reactions. |
| `/stm32_down` | Custom | Direct firmware update command packets. |

---

## Published Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/encoder_odom` | `nav_msgs/Odometry` | Raw wheel encoder odometry calculated directly from wheel clicks. |
| `/encoder_raw` | `keenon_motor_msgs/encoder` | Left and right wheel encoder raw ticks. |
| `/chassis_imu_data` | `sensor_msgs/Imu` | Fused IMU orientation, angular velocity, and linear acceleration (published at $50\text{ Hz}$). |
| `/imu_raw` | `sensor_msgs/Imu` | Raw IMU readings from the STM32 accelerometer/gyroscope. |
| `/odom_combined` | `geometry_msgs/PoseWithCovarianceStamped` | Odometry pose with covariance (published at $46\text{ Hz}$). |
| `/battery_state` | `sensor_msgs/BatteryState` | Battery voltage, current, percentage, and charging state. |
| `/urgency_stop` | `std_msgs/Bool` | Emergency stop state (triggered by bumpers, sensors, or e-stop). |
| `/urgency_button_status` | `std_msgs/Bool` | Real-time state of the physical e-stop switch. |
| `/charge_state_fromSTM32` | `keenon_charge_msgs/ChargeFB` | Real-time charging contacts, voltage, and connection feedback. |
| `/motor_lock_status` | `std_msgs/Bool` | Real-time motor lock/unlock feedback status. |
| `/motor_error_code` | Custom | Diagnostic error codes reported from the motor drivers. |
| `/mileage` | `std_msgs/Float64` | Total accumulated physical travel distance in meters. |
| `/chassis_sensor` | Custom | Proximity, sonar, and PSD raw sensor packets. |
| `/error_report` | Custom | Chassis hardware diagnostic logs. |
| `/bump` | `sensor_msgs/PointCloud2` | Bumper event points mapped into coordinates. |
| `/beam` | Custom | Infrared safety beam sensor events. |
| `/stm32_version` | `std_msgs/String` | Firmware version of the STM32 board. |
| `/stm32_up` | Custom | Firmware upgrade progress feedback. |
| `/tf` | `tf2_msgs/TFMessage` | Dynamic transforms (e.g., `base_link` -> `wheel_odom` or similar if enabled). |

---

## Services

* `/chassis/get_loggers` (`roscpp/GetLoggers`)
* `/chassis/set_logger_level` (`roscpp/SetLoggerLevel`)

---

## TF
* **Broadcaster:** Broadcasts the transform `base_link` -> `wheel_odom` at approximately $50\text{ Hz}$ based on static parameters.
* **Listener:** References `/tf` coordinate streams to verify coordinate alignments.

---

## Dependencies
* **Libraries:** `roscpp`, `tf`, `serial`
* **Custom Messages:** `keenon_motor_msgs`, `keenon_charge_msgs`
* **Hardware:** USB-to-Serial link connection to the STM32 board, mapped to `/dev/ttyUSBStm32` via udev rule.

---

## Known Issues
1. **Serial Interruption:** Communication is sensitive to electrical noise on the USB serial bus. Cable disconnects require a reload of the upstart system job.
2. **Transform Conflict:** If `send_transform` is set to `true` while the `front_end_node` is also broadcasting, it causes coordinate frame oscillation. In standard configurations, the dynamic transform is managed by `front_end_node` fusing raw encoder ticks.

---

## Reverse Engineered Notes
* Communicates with a custom STM32 microcontroller board using a proprietary serial packet framing.
* **Firmware Update:** Flashing is accomplished via an In-Application Programming (IAP) protocol. The `update_Stm32.sh` script stops the `keenonrobot` service, invokes the `./iap` flashing utility on `/dev/ttyUSBStm32` at a baudrate of `115200` using the binary `stm32_robot_APP_v2.1.2-0-g83926df.bin`, and restarts the service.
* Reads raw wheel ticks (`/encoder_raw`) and IMU orientation (`/chassis_imu_data`) and outputs them to the `front_end_node` for localization fusion.
