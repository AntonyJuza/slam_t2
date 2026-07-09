# Schedule Map Builder Node (`schedule_map_builder`)

## Verification Status
| Status | Items |
| :--- | :--- |
| **✅ Verified** | Running node `/schedule_map_builder` (PID 3679). Subscriptions to `/tf`, `/tf_static`, and `/robot_current_floor` (published by `/switch_map`), and publications on `/virtual_wall_1`, `/schedule_state`, `/virtual_wall_updates`, and `/click_map_pub_` confirmed via `rosnode info`. |
| **🟡 Inferred** | Multi-robot dynamic blocking zone and hallway lock mechanics (inferred from node connections and `/virtual_wall_updates` topic, but not validated with multiple active robots). |
| **🔴 Unknown** | Exact network synchronization API and server-side scheduler dispatch communication parameters. |

## Purpose
The `schedule_map_builder` node handles multi-robot coordination and scheduling. It communicates with the scheduling server, coordinates virtual wall blockages, publishes scheduling state, and updates costmaps dynamically to prevent the robot from planning routes through restricted or busy hallways.

---

## Executable
* **Binary Path:** `/opt/ros/indigo/lib/schedule_map_builder/schedule_map_builder_node`
* **Package Name:** `schedule_map_builder`
* **Node Name:** `/schedule_map_builder`

---

## Launch File
* **Path:** `OpenT2/launch/include/schedule_map_builder.launch`

```xml
<?xml version="1.0"?>
<launch>
    <arg name="OUTPUT_METHOD" default="screen"/>
    <arg name="RESPAWN" default="false"/>
    <arg name="ROBOT_TYPE" default="peanut"/>

    <node pkg="schedule_map_builder" type="schedule_map_builder_node" name="schedule_map_builder" respawn="$(arg RESPAWN)" output="$(arg OUTPUT_METHOD)" />
</launch>
```

---

## Parameters
Uses default compile-time parameters.

---

## Subscribed Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/robot_current_floor` | `std_msgs/Int16` | Active floor index from `/switch_map`. |
| `/schedule_path` / `/schedule_path_test`| Custom | Coordinates representing paths assigned by the scheduling server. |
| `/robot_pose` | `geometry_msgs/PoseStamped` | Current estimated robot coordinates. |
| `/clicked_point` | `geometry_msgs/PointStamped` | Manual checkpoint coordinate from Rviz. |
| `/tf` & `/tf_static` | `tf2_msgs/TFMessage` | Frame transforms. |

---

## Published Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/virtual_wall_1` | `nav_msgs/OccupancyGrid` | Grid containing scheduler-defined temporary virtual walls. |
| `/virtual_wall_updates`| `map_msgs/OccupancyGridUpdate`| Real-time changes to the active virtual wall grid. |
| `/schedule_state` | `std_msgs/Bool` | Indicates if the robot is currently controlled by the scheduling system (`true`) or free to navigate independently. |
| `/click_map_pub_` | `nav_msgs/OccupancyGrid` | Interactive path visualization. |

---

## Services

* `/schedule_map_builder/get_loggers`
* `/schedule_map_builder/set_logger_level`

---

## TF
* **Listener:** Subscribes to `/tf` to track active planning frame coordinates.

---

## Dependencies
* **Nodes:**
  * `/switch_map` (Provides floor index).
  * `/move_base` (Consumes `/virtual_wall_updates` in the costmap obstacle layer).

---

## Known Issues
1. **Network Disconnection:** If the Wi-Fi connection to the scheduling server drops, the node may fail to clear temporary virtual walls, leaving the robot stuck in front of phantom obstacles.

---

## Reverse Engineered Notes
* **Dynamic Costmap Injection:** Rather than reloading the map when scheduling changes occur, `schedule_map_builder` publishes `map_msgs/OccupancyGridUpdate` messages directly to `/virtual_wall_updates`. The costmap obstacle layer in `move_base` intercepts these updates to block off congested corridors on the fly.
* **Topological Lockouts:** Works in tandem with the scheduling server to lock out intersections, elevators, and charging bays in multi-robot deployments.
