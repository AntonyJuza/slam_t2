# OpenT2: Keenon T2 Reverse Engineering Project

Welcome to the **OpenT2** project. The goal of this repository is to clean-room reverse engineer the hardware and software subsystems of the Keenon T2 delivery robot. This workspace compiles the necessary information to allow developers to construct open-source firmware, drivers, localization, and navigation nodes without depending on proprietary Keenon software.

---

## 📋 Reverse Engineering TODO Board

### Stage 1: Datasheet & Reverse Engineering

- [x] **Robot Type Identification**
  - *Status:* Verified as the differential-drive Keenon T2 base.
- [x] **Launch Files Cataloging**
  - *Status:* Documented and organized under `/launch`.
- [x] **Cartographer Lua Configurations**
  - *Status:* Recovered and documented under `/parameters/cartographer_ros`.
- [x] **LiDAR Topics & Drivers**
  - *Status:* Verified dual SDKELI LS-L100 streams at $28\text{ Hz}$ on `/scan_front_orig` and `/scan_back_orig`, combined in `/multi_lidar_filter`.
- [x] **Encoder Topics & Odometry**
  - *Status:* Verified `/encoder_raw` and `/odom_combined` topics at $45.8\text{ Hz}$.
- [x] **IMU Topics & Status**
  - *Status:* Verified `/chassis_imu_data` and `/imu_raw` are dummy topics because the physical IMU sensor chip is unpopulated on the motion control board.
- [x] **Depth Cameras Verification**
  - *Status:* Configured and mapped front/rear RealSense D435 and side MX cameras under `/hardware`.
- [x] **STM32 Serial Protocol**
  - *Status:* Recovered packet frame format (`AA AA 00 E0` -> Payload -> `55 55`), encoder (`2D 00`), motor (`2F 00`), and dummy IMU (`32 01`) messages, flashing procedure (`iap`), and firmware version (`v2.1.2`).
- [ ] **cmd_vel Flow Analysis**
  - *Goal:* Map the path of `/cmd_vel` velocity commands from local planners to physical motors and document speed/acceleration safety scaling.
- [ ] **TF Tree Verification**
  - *Goal:* Graph and verify the live coordinate frames against the recovered URDF files, identifying parent-child relationships and static/dynamic transforms.
- [ ] **Charging System Reverse Engineering**
  - *Goal:* Analyze the charging pile search, alignment control loop, and `/charge_state_fromSTM32`/`/charge_ctrl` topic interactions.
- [ ] **Safety Controller Mechanics**
  - *Goal:* Map the physical bumpers (`/bump`), LiDAR safety zones, and camera obstacle avoidance threshold loops.
- [ ] **Localization Flow Analysis**
  - *Goal:* Document the startup sequence, initial pose seeding via SQLite/pose cache file, relocalization triggers, and scan matcher parameters.
- [ ] **Navigation Flow Analysis**
  - *Goal:* Document the local/global costmaps, `teb_local_planner` configurations, elevator doors, automatic gates MAC trigger systems, and goal dispatching.

---

## 📂 Repository Structure

* `docs/`: Comprehensive technical specification datasheets and node-by-node documentation.
* `hardware/`: Component inventory and real-time sensor verification logs.
* `firmware/`: STM32 USART protocols, command structures, and In-Application Programming (IAP) flashing routines.
* `launch/`: Recovered ROS launch file architectures.
* `parameters/`: Extracted YAML and Lua configurations for localization, mapping, and planning.
* `rosgraph/`: Publications, subscriptions, services, and topic database mappings.
* `tf/`: Active coordinate transformation tree structure and offsets.
* `urdf/`: Recovered robot physical geometry description files.
