# Multi Lidar Filter Node (`multi_lidar_filter`)

## Verification Status
| Status | Items |
| :--- | :--- |
| **✅ Verified** | Running nodes `/multi_lidar_filter` and `/multi_lidar_filter_for_planner`. Subscriptions to `/scan_front_orig`, `/scan_back_orig`, `/tf`. Publications on `/scan_orig`, `/scan`, `/planner_scan` at $28\text{ Hz}$. Config load from YAML parameters. |
| **🟡 Inferred** | Exact geometric cluster separation algorithms (derived from configuration thresholds `search_th` and `th_thre` but not reverse-engineered from source binaries). |
| **🔴 Unknown** | Exact scan matching/alignment math used internally inside the filter executable. |

## Purpose
The `multi_lidar_filter` node fuses two physical $180^\circ$ lidars (front and rear SDKeli scanners) into a single $360^\circ$ representation, removes self-reflections caused by the robot chassis footprint, and outputs clean laser scan streams for obstacle avoidance, global planning, and localization.

---

## Executable
* **Binary Path:** `/opt/ros/indigo/lib/lidar_filter/multi_lidar_filter`
* **Package Name:** `lidar_filter`
* **Node Names:** 
  * `/multi_lidar_filter` (Fuses scans for obstacle avoidance and local costmaps)
  * `/multi_lidar_filter_for_planner` (Fuses scans with wider thresholds for the global planner)

---

## Launch File
* **Path:** `OpenT2/launch/include/lidar_filter_2.launch`
* **Parameter Files Loaded:** 
  * `OpenT2/parameters/T2/lidar_filter.yaml` (Loaded by `/multi_lidar_filter`)
  * `OpenT2/parameters/T2/lidar_filter_for_planner.yaml` (Loaded by `/multi_lidar_filter_for_planner`)

```xml
<?xml version="1.0"?>
<launch>
    <arg name="OUTPUT_METHOD" default="screen"/>
    <arg name="RESPAWN" default="false"/>
    <arg name="ROBOT_TYPE" default="peanut"/>

    <node pkg="lidar_filter" type="multi_lidar_filter" name="multi_lidar_filter" respawn="$(arg RESPAWN)" output="$(arg OUTPUT_METHOD)">
        <rosparam file="$(find robot_settings)/cfg/yaml/$(arg ROBOT_TYPE)/lidar_filter.yaml" command="load" />
    </node>

    <node pkg="lidar_filter" type="multi_lidar_filter" name="multi_lidar_filter_for_planner" respawn="$(arg RESPAWN)" output="$(arg OUTPUT_METHOD)">
        <rosparam file="$(find robot_settings)/cfg/yaml/$(arg ROBOT_TYPE)/lidar_filter_for_planner.yaml" command="load" />
        <remap from="scan" to="planner_scan"/>
    </node>
</launch>
```

---

## Parameters

| Parameter | Type | `lidar_filter.yaml` | `lidar_filter_for_planner.yaml` | Description |
| :--- | :--- | :--- | :--- | :--- |
| `global_filter` | Boolean | `true` | `true` | Enables global coordinate-based filtering. |
| `enabled` | Boolean | `true` | `true` | Enables/disables the node processing loop. |
| `search_dist` | Double | `0.4` | `10.0` | Scan radius threshold ($m$) to process. |
| `search_th` | Double | `0.1` | `0.1` | Threshold parameter for cluster separation. |
| `search_intensity`| Double | `180.0` | `180.0` | Intensity filter threshold. |
| `dist_thre` | Double | `0.03` | `0.03` | Point distance threshold ($m$) for filtering. |
| `th_thre` | Double | `0.45` | `1.5` | Angular threshold (radians) for scan matching/alignment. |

---

## Subscribed Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/scan_front_orig` | `sensor_msgs/LaserScan` | Raw laser scans from the front SDKeli Lidar ($28\text{ Hz}$). |
| `/scan_back_orig` | `sensor_msgs/LaserScan` | Raw laser scans from the rear SDKeli Lidar ($28\text{ Hz}$). |
| `/tf` & `/tf_static` | `tf2_msgs/TFMessage` | Frame transforms. |

---

## Published Topics

| Topic | Type | Description |
| :--- | :--- | :--- |
| `/scan_orig` | `sensor_msgs/LaserScan` | Merged raw scan before any obstacle or footprint filtering. Used by localization. |
| `/scan` | `sensor_msgs/LaserScan` | Merged and filtered scan (published by `/multi_lidar_filter`). Used for obstacle avoidance. |
| `/planner_scan` | `sensor_msgs/LaserScan` | Merged and wider-filtered scan (published by `/multi_lidar_filter_for_planner`). Used for global costmaps. |

---

## Services

* `/multi_lidar_filter/get_loggers`
* `/multi_lidar_filter/set_logger_level`
* `/multi_lidar_filter_for_planner/get_loggers`
* `/multi_lidar_filter_for_planner/set_logger_level`

---

## TF
* **Listener:** Uses the static transforms from `base_link` to `laser_front_link` and `laser_back_link` to project lidar points into the robot center before merging.
  * Front Lidar: $x = 0.193\text{ m}, y = 0.0\text{ m}, z = 0.225\text{ m}$, Yaw = $0.0\text{ rad}$.
  * Rear Lidar: $x = -0.193\text{ m}, y = 0.0\text{ m}, z = 0.225\text{ m}$, Yaw = $3.14159\text{ rad}$.

---

## Dependencies
* **Nodes:**
  * `/sdkeli_front` & `/sdkeli_back` (Lidar driver nodes).

---

## Known Issues
1. **Overlap Ghosting:** If the relative mounting positions in the static transform configuration (`tf_static` / URDF) are misaligned by millimeters, targets at the lidar overlap boundaries will appear twice ("ghosting"), causing path planning blockages.
2. **Frequency Jitter:** Requires both lidars to publish at similar rates ($\approx 28\text{ Hz}$) to prevent lag in the merged output.

---

## Reverse Engineered Notes
* Spawns two distinct instances of the filter binary to isolate CPU tasks.
* Outputs the raw merged stream on `/scan_orig`. This raw topic is critical for localization (`peanut_localization_node`) since static structural details (such as pillars) should not be filtered out.
* The `/scan` topic filters out short-range points corresponding to the robot's own chassis footprint and filters out high-intensity reflections.
