# Switch Map Node (`switch_map`)

## Verification Status
| Status | Items |
| :--- | :--- |
| **✅ Verified** | Running node `/switch_map` (PID 3624). Subscriptions to `/tf` and `/tf_static` and publications on `/map`, `/virtual_wall`, `/gate_map`, `/elevator_map`, `/vel_map`, `/map_metadata`, `/robot_current_floor`, and `/label_map` confirmed via `rosnode info`. SQLite map BLOB and waypoint retrieval from `peanut.db` verified. |
| **🟡 Inferred** | Dynamic coordination rules during elevator docking and floor map coordinate transformation offsets (inferred from `/switch_dest_floor_map` service call sequence). |
| **🔴 Unknown** | Exact validation check steps executed when writing updated layout layers back to the SQLite file. |

## Purpose
The `switch_map` node manages multi-floor operations and map layer distribution. It queries the local SQLite database (`peanut.db`), extracts the correct map and layer data (such as occupancy grids, virtual walls, elevator zones, speed limit zones, and automatic gate locations) for the requested floor, and publishes them to the respective ROS topics.

---

## Executable
* **Binary Path:** `/opt/ros/indigo/lib/switch_map/switch_map`
* **Package Name:** `switch_map`
* **Node Name:** `/switch_map`

---

## Launch File
* **Path:** `OpenT2/launch/include/switch_map.launch`

```xml
<?xml version="1.0"?>
<launch>
    <arg name="OUTPUT_METHOD" default="screen"/>
    <arg name="RESPAWN" default="false"/>
    <arg name="ROBOT_TYPE" default="peanut"/>

    <node name="switch_map" pkg="switch_map" type="switch_map" respawn="$(arg RESPAWN)" output="$(arg OUTPUT_METHOD)"/>
</launch>
```

---

## Parameters
* **Database File Path:** `/etc/ros/runtime/database/peanut.db` (Default path containing the system configuration and map layers).

---

## Subscribed Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/load_label` | Custom | Trigger to reload waypoint labels. |
| `/tf` & `/tf_static` | `tf2_msgs/TFMessage` | Frame transforms. |

---

## Published Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/map` | `nav_msgs/OccupancyGrid` | The current floor occupancy grid map used for localization and navigation. |
| `/virtual_wall` | `nav_msgs/OccupancyGrid` | Grid containing virtual walls for the current floor. |
| `/gate_map` | `nav_msgs/OccupancyGrid` | Grid containing automatic gate interaction regions. |
| `/elevator_map` | `nav_msgs/OccupancyGrid` | Grid defining elevator cabin regions and docking zones. |
| `/vel_map` | `nav_msgs/OccupancyGrid` | Grid representing restricted speed zones. |
| `/map_metadata` | `nav_msgs/MapMetaData` | Size, resolution, and origin details of the current map. |
| `/robot_current_floor`| `std_msgs/Int16` | The active floor index. |
| `/label_map` | `keenon_label_msgs/gmapping_label_array` | Array of labeled waypoint coordinates (delivery points, charger, elevator docking). |

---

## Services

| Service | Type | Description |
| :--- | :--- | :--- |
| `/static_map` | `nav_msgs/GetMap` | Standard ROS map server service returning the current occupancy grid. |
| `/switch_dest_floor_map` | Custom | Request map switch to a target floor. |
| `/config_map_trans` | Custom | Updates coordinate transforms between floors. |

---

## TF
* **Listener:** Tracks transforms to apply alignment offsets when transitioning between floor coordinates.

---

## Dependencies
* **Libraries:** `sqlite3`, `nav_msgs`, `std_msgs`.
* **Database:** SQLite database located at `/etc/ros/runtime/database/peanut.db`.

---

## Known Issues
1. **Database Lockups:** SQLite can lock up if multiple nodes attempt to write to `peanut.db` at the same time. The database is opened in read-only mode by `switch_map` to prevent locking.

---

## Reverse Engineered Notes
* **Database Structure:** Maps are stored as binary BLOBs in the `map` table of `peanut.db`:
  * `carto_map` (Occupancy grid created by SLAM).
  * `virtual_wall` (Occupancy grid containing user-defined virtual walls).
* **Multi-Floor Transition:** When the robot enters an elevator, the Android tablet triggers the `/switch_dest_floor_map` service. `switch_map` queries the database for the new floor, publishes the new occupancy grid `/map`, updates `/virtual_wall` and other costmap grids, and broadcasts the updated floor index on `/robot_current_floor`.
