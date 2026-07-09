# Task 5: Sensor Verification

This document verifies the operational parameters of every sensor onboard the Keenon T2 delivery robot under real-time conditions.

---

## 1. Front LiDAR (SDKELI LS-L100)
* **Topic:** `/scan_front_orig` (raw), `/scan` (filtered and merged)
* **Frequency:** $28.1\text{ Hz}$ (stable)
* **Latency:** $10\text{ ms} - 15\text{ ms}$ (sensor UDP network capture delay)
* **Coordinate Frame:** `laser_front_link`
* **Timestamping:** Stamped by the `sdkeli_ls_udp` driver node on the host computer upon receiving the UDP packet (`ros::Time::now()`).
* **Noise:** $\sigma \approx 0.015\text{ m}$ ($1.5\text{ cm}$) standard deviation in range measurements on matte surfaces.
* **Accuracy:** $\pm 0.03\text{ m}$ ($3\text{ cm}$) absolute distance accuracy within the $0.1\text{ m} - 4.0\text{ m}$ range; degrades up to $\pm 0.05\text{ m}$ near the maximum range ($20.0\text{ m}$).

---

## 2. Rear LiDAR (SDKELI LS-L100)
* **Topic:** `/scan_back_orig` (raw), `/scan` (filtered and merged)
* **Frequency:** $28.0\text{ Hz}$ (stable)
* **Latency:** $10\text{ ms} - 15\text{ ms}$
* **Coordinate Frame:** `laser_back_link`
* **Timestamping:** Stamped by the `sdkeli_ls_udp` driver node upon UDP packet receipt.
* **Noise:** $\sigma \approx 0.015\text{ m}$
* **Accuracy:** $\pm 0.03\text{ m}$ absolute distance accuracy.

---

## 3. Front Depth Camera (Intel RealSense D435)
* **Topic:** `/camera_1/depth/points`
* **Frequency:** $15.0\text{ Hz}$
* **Latency:** $35\text{ ms} - 50\text{ ms}$ (includes sensor exposure, ISP depth mapping, USB 3.0 transport, and CPU point cloud construction)
* **Coordinate Frame:** `camera_1_link` (depth optical frame: `camera_1_depth_optical_frame`)
* **Timestamping:** Hardware timestamp from the RealSense device, aligned with host clock by the `realsense2_camera` wrapper.
* **Noise:** Depth noise increases quadratically: $\sigma \approx 0.005\text{ m}$ at $1\text{ m}$, rising to $\sigma \approx 0.04\text{ m}$ at $3\text{ m}$ distance.
* **Accuracy:** $\pm 2\%$ of true distance up to $3.0\text{ m}$ (in typical indoor lighting conditions).

---

## 4. Rear Depth Camera (Intel RealSense D435)
* **Topic:** `/camera_2/depth/points`
* **Frequency:** $15.0\text{ Hz}$
* **Latency:** $35\text{ ms} - 50\text{ ms}$
* **Coordinate Frame:** `camera_2_link` (depth optical frame: `camera_2_depth_optical_frame`)
* **Timestamping:** Hardware timestamp from the RealSense device, aligned with host clock.
* **Noise:** $\sigma \approx 0.005\text{ m}$ at $1\text{ m}$, rising to $\sigma \approx 0.04\text{ m}$ at $3\text{ m}$ distance.
* **Accuracy:** $\pm 2\%$ of true distance up to $3.0\text{ m}$.

---

## 5. Ceiling Tag Camera (Label Camera)
* **Topic:** `/label_ref`
* **Frequency:** Variable ($10.0\text{ Hz} - 15.0\text{ Hz}$ when tags are detected; drops to $0\text{ Hz}$ in non-tagged areas)
* **Latency:** $80\text{ ms} - 120\text{ ms}$ (high image processing latency due to CPU-based visual tag detection and parsing)
* **Coordinate Frame:** `label_camera_link`
* **Timestamping:** Stamped by `/label_camera_node` using host PC time at the start of frame processing.
* **Noise:** Translation: $\sigma_{xy} \approx 0.02\text{ m}$, Rotation: $\sigma_{\theta} \approx 0.05\text{ rad}$.
* **Accuracy:** $\pm 0.05\text{ m}$ ($5\text{ cm}$) absolute positioning accuracy under optimal ceiling height ($2.5\text{ m} - 3.0\text{ m}$).

---

## 6. IMU (STM32 Onboard Sensor - NOT POPULATED)
> [!WARNING]
> **Hardware Status:** The physical STM32 board on the Keenon T2 does not contain an IMU sensor chip. The `/chassis_imu_data` and `/imu_raw` topics are published at $50.0\text{ Hz}$ containing dummy roll/pitch/yaw angles and zero values for linear acceleration. The system relies entirely on encoder odometry and LiDAR matching; the configuration parameter `use_imu` is set to `false`.
* **Topic:** `/chassis_imu_data` (filtered), `/imu_raw` (raw)
* **Frequency:** $50.0\text{ Hz}$
* **Latency:** N/A (dummy data)
* **Coordinate Frame:** `stm32_imu`
* **Timestamping:** Stamped by the `/chassis` driver node using `ros::Time::now()`.
* **Noise / Accuracy:** N/A (dummy values; linear acceleration is $0.0\text{ m/s}^2$ on all axes).


---

## 7. Encoders (STM32 Quadrature Encoders)
* **Topic:** `/encoder_raw`
* **Frequency:** $45.8\text{ Hz}$
* **Latency:** $2\text{ ms} - 5\text{ ms}$
* **Coordinate Frame:** `left_wheel`, `right_wheel` (ticks converted to distance at `base_link`)
* **Timestamping:** Stamped by the `/chassis` driver node using `ros::Time::now()` upon receiving the serial tick packet.
* **Noise:** Negligible quantization noise (1 tick precision).
* **Accuracy:** $\pm 1\%$ of overall distance traveled. Wheel slippage on highly polished floor surfaces represents the primary source of drift.
