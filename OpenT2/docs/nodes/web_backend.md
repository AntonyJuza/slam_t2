# Web Backend Node (`web_backend_node`)

## Purpose
The `web_backend_node` acts as a communication bridge between the ROS environment and external user interfaces (such as the Android tablet app and cloud services). It monitors robot telemetry and compresses high-bandwidth grid maps and costmaps into compressed image streams to save wireless bandwidth.

---

## Executable
* **Binary Path:** `/opt/ros/indigo/lib/web_backend/web_backend_node`
* **Package Name:** `web_backend`
* **Node Name:** `/web_backend_node`

---

## Launch File
* **Path:** `OpenT2/launch/include/web_backend.launch`

```xml
<?xml version="1.0"?>
<launch>
    <arg name="OUTPUT_METHOD" default="screen"/>
    <arg name="RESPAWN" default="false"/>
    <arg name="ROBOT_TYPE" default="peanut"/>

    <node name="web_backend_node" pkg="web_backend" type="web_backend_node" respawn="$(arg RESPAWN)" output="$(arg OUTPUT_METHOD)">
        <param name="maps_layer_path" value="/etc/ros/runtime/maps/"/>
    </node>
</launch>
```

---

## Parameters

| Parameter | Type | Value | Description |
| :--- | :--- | :--- | :--- |
| `maps_layer_path` | String | `/etc/ros/runtime/maps/` | Local cache directory used for exporting map assets. |

---

## Subscribed Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/map` | `nav_msgs/OccupancyGrid` | The current floor occupancy grid map. |
| `/virtual_wall` | `nav_msgs/OccupancyGrid` | Active virtual walls. |
| `/gate_map` | `nav_msgs/OccupancyGrid` | Active automatic gates. |
| `/move_base/local_costmap/costmap` | `nav_msgs/OccupancyGrid` | Local costmap representation. |
| `/move_base/global_costmap/costmap`| `nav_msgs/OccupancyGrid` | Global costmap representation. |
| `/scan` | `sensor_msgs/LaserScan` | Filtered laser scan points. |
| `/mapping_status` | `std_msgs/UInt8` | Current SLAM mapping progress status. |
| `/tf` & `/tf_static` | `tf2_msgs/TFMessage` | Frame transforms. |

---

## Published Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/map/to_web/compressed` | `sensor_msgs/CompressedImage` | Map occupancy grid compressed as an image stream. |
| `/virtual_wall/to_web/compressed` | `sensor_msgs/CompressedImage` | Virtual wall grid compressed as an image. |
| `/gate_map/to_web/compressed` | `sensor_msgs/CompressedImage` | Gate grid compressed as an image. |
| `/move_base/local_costmap/costmap/to_web/compressed` | `sensor_msgs/CompressedImage` | Local planning costmap compressed as an image. |
| `/move_base/global_costmap/costmap/to_web/compressed` | `sensor_msgs/CompressedImage` | Global planning costmap compressed as an image. |
| `/robot_state` | `web_backend/robot_state` | Fused telemetry packet (battery, coordinates, speed, errors) sent to the UI. |
| `/run_mapping` | `std_msgs/UInt8` | Starts or stops the mapping process based on user commands. |
| `/scan_base_map` | `web_backend/PointArray` | Projected lidar scan coordinates aligned with the map. |

---

## Services

* `/web_command` (Custom service to receive structured JSON/RPC commands from the tablet interface).
* `/web_backend_node/get_loggers` / `/web_backend_node/set_logger_level`

---

## TF
* **Listener:** Tracks the `map` -> `base_link` coordinates to project the robot's real-time position onto the compressed map image.

---

## Dependencies
* **Nodes:**
  * `rosbridge_websocket` (Translates ROS topics and services to WebSocket connections).

---

## Known Issues
1. **Network Compression Overhead:** High CPU usage when compressing large grid maps if the Wi-Fi signal drops and retransmissions occur.
2. **WebSocket Buffer Overflow:** If the tablet UI disconnects abruptly, the unsent compressed images can pile up in the rosbridge queue, causing memory leaks.

---

## Reverse Engineered Notes
* **Bandwidth Optimization:** Instead of sending raw occupancy grids (which consume megabytes of data), `web_backend_node` renders the grid arrays onto a color-coded image buffer, applies JPEG/PNG compression, and publishes it on the `*/to_web/compressed` topics.
* **Web Command Hub:** The `/web_command` service is the entry point for starting deliveries, switching maps, declaring manual e-stops, locking/unlocking motors, and controlling chargers.
