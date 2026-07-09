# Task 1: Hardware Inventory

This document lists and details every physical hardware component, sensor, and actuator on the Keenon T2 delivery robot, along with their interface, ROS driver, and current operational status.

---

## Component Inventory

| Component | Model | Interface | ROS Driver Node | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Front LiDAR** | SDKELI LS-L100 ($180^\circ$ planar) | Ethernet (UDP) | `/sdkeli_front` (pkg: `sdkeli_ls_udp`) | ✅ Working |
| **Rear LiDAR** | SDKELI LS-L100 ($180^\circ$ planar) | Ethernet (UDP) | `/sdkeli_back` (pkg: `sdkeli_ls_udp`) | ✅ Working |
| **Front Depth Camera** | Intel RealSense D435 | USB 3.0 | `/camera_1/driver` (pkg: `realsense2_camera`) | ✅ Working |
| **Rear Depth Camera** | Intel RealSense D435 | USB 3.0 | `/camera_2/driver` (pkg: `realsense2_camera`) | ✅ Working |
| **Ceiling Camera** | Label Camera (Visual QR/Tag) | USB 2.0 | `/label_camera_node` (pkg: `label_camera`) | ✅ Working |
| **Accessory/Side Sensor**| MX Depth Camera | USB 3.0 | `/mx_camera_node` (pkg: `mx_camera`) | ✅ Working |
| **IMU** | None (Unpopulated) | N/A | `/chassis` (publishes dummy values) | ❌ Not Present |
| **Encoder** | Quadrature Optical Encoders | Timer Interface (Internal to STM32) | `/chassis` (pkg: `chassis` via serial read) | ✅ Working |
| **Motor Driver** | Dual BLDC Hub Motor Driver | CAN / UART (Internal to STM32) | `/chassis` (pkg: `chassis` via serial cmd) | ✅ Working |
| **Charging Board / BMS** | Custom Power Management Board | UART / GPIO to STM32 | `/chassis` (pkg: `chassis` via `/charge_state_fromSTM32`) | ✅ Working |

---

## Interface Details & Specifications

### 1. Planar LiDARs (SDKELI LS-L100)
* **Purpose:** Obstacle detection, safety zones, and mapping/localization reference.
* **Network Settings:** Communicates over UDP to the CPU host. The drivers are run as individual nodes `sdkeli_front` and `sdkeli_back`, subscribing to the raw UDP socket and publishing standard `sensor_msgs/LaserScan` messages.
* **Scan Frequency:** $28\text{ Hz}$ per LiDAR.

### 2. Depth Cameras (Intel RealSense D435)
* **Purpose:** 3D obstacle avoidance (detecting tables, chair legs, overhead obstacles), elevator detection, and crowd detection.
* **Mounting Angles:** 
  * Front camera: mounted at $Z = 1.184\text{ m}$, tilted forward by $0.61\text{ rad}$ ($\approx 35^\circ$).
  * Rear camera: mounted at $Z = 1.184\text{ m}$, tilted backward by $0.61\text{ rad}$ ($\approx 35^\circ$).
* **Data Stream:** Output is transformed into point clouds (`sensor_msgs/PointCloud2`) on topics `/camera_1/depth/points` and `/camera_2/depth/points`.

### 3. Ceiling Camera (Label Camera)
* **Purpose:** Absolute visual localization reference by reading ceiling-mounted visual labels/QR codes.
* **Orientation:** Pointing straight up ($Pitch = 180^\circ$, Yaw = $-90^\circ$ relative to `base_link` frame).

### 4. STM32 Motion Controller Board
* **Purpose:** Acts as the real-time controller for the wheels, encoders, safety bumpers, and BMS.
* **Communication Interface:** Connects to the host CPU over a USB-to-Serial converter mapped to `/dev/ttyUSBStm32` running at $115200\text{ bps}$ baudrate.
