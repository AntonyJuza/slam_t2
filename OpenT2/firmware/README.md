# Task 7: STM32 Microcontroller Interface & Flashing

This document details the interface protocol, packet formatting, active firmware version, and the update procedure for the STM32-based motion control board onboard the Keenon T2.

---

## 1. Connection & Protocol Specifications

* **Physical Interface:** USB-to-Serial converter internally connected to STM32 USART, mapped on the CPU via udev rules to:
  `/dev/ttyUSBStm32` (or `/dev/ttyUSB2` directly)
* **Baudrate:** `115200` bps
* **Data Settings:** 8 Data Bits, 1 Stop Bit, No Parity
* **Control:** Bidirectional serial streaming

---

## 2. Serial Packet Frame Format

The serial messages stream continuously from the STM32 to the host CPU, packed within distinct frame headers and tails.

### Packet Structure
```
+--------------------+---------------------+------------------+-------------------+
|  Header (4 bytes)  |  Payload (Variable) |  CRC / Checksum  |   Tail (2 bytes)  |
|  AA AA 00 E0       |  [Command] [Data]   |  (Optional)      |   55 55           |
+--------------------+---------------------+------------------+-------------------+
```

* **Header:** 4 bytes `AA AA 00 E0` (`\xaa\xaa\x00\xe0`)
* **Tail:** 2 bytes `55 55` (`\x55\x55`)
* **Payload Structure:** 
  * The first 2 bytes of the payload represent the **Message Type / Command ID**.
  * The remaining payload bytes contain structured binary data fields.

---

## 3. Message Type Definitions (STM32 -> CPU)

### A. Encoder Raw Ticks (Command: `2D 00`)
Contains raw encoder counts used by `/chassis` to compute odometry.
* **Command ID:** `0x002D`
* **Format:** `<ii` (two signed 32-bit little-endian integers)
* **Payload Offset:** bytes 4 to 12 of the stripped payload
* **Data Fields:**
  1. `left_wheel_ticks` (int32)
  2. `right_wheel_ticks` (int32)

### B. Motor Status / Counters (Command: `2F 00`)
Feedback regarding motor driver control loops.
* **Command ID:** `0x002F`
* **Format:** `<ii` (two signed 32-bit little-endian integers)
* **Payload Offset:** bytes 6 to 14 of the stripped payload
* **Data Fields:**
  1. `motor_1_speed_counter` (int32)
  2. `motor_2_speed_counter` (int32)

### C. Onboard IMU Data (Command: `32 01`)
> [!IMPORTANT]
> **Hardware Note:** The physical motion controller board does not contain a populated IMU sensor chip. The firmware still outputs this message type, but the values are uninitialized/dummy floats. In the robot's configuration (`chassis_params.yaml`), `use_imu` is set to `false` and these readings are ignored.
* **Command ID:** `0x0132`
* **Format:** `<fff` (three 32-bit little-endian floats)
* **Payload Offset:** bytes 4 to 16 of the stripped payload
* **Data Fields:**
  1. `roll` (float, dummy/uninitialized)
  2. `pitch` (float, dummy/uninitialized)
  3. `yaw` (float, dummy/uninitialized)


---

## 4. Current Firmware Version

* **Active Version:** `v2.1.2`
* **Binary Filename:** `stm32_robot_APP_v2.1.2-0-g83926df.bin`
* **Storage Location:** `/home/peanut/`

---

## 5. Firmware Flashing (Update) Process

The STM32 microcontroller utilizes In-Application Programming (IAP) over the serial interface. A dedicated binary utility (`iap`) executes the bootloader synchronization and flash sequence.

### Flashing Procedure
The update process is managed via the shell script `/home/peanut/update_Stm32.sh`.

```bash
# 1. Stop the active ROS chassis driver and background nodes to free the serial port
sudo stop keenonrobot

# 2. Execute the IAP tool to upload the firmware binary
# Parameters:
#   -p: Serial port (/dev/ttyUSBStm32)
#   -b: Baudrate (115200)
#   -f: Path to the firmware binary
/home/peanut/iap -p /dev/ttyUSBStm32 -b 115200 -f /home/peanut/stm32_robot_APP_v2.1.2-0-g83926df.bin

# 3. Restart the ROS background nodes to restore normal operations
sudo start keenonrobot
```
