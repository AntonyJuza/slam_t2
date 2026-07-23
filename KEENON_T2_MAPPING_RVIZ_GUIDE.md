# Keenon T2 - Complete Guide: SLAM Mapping, Services & RViz Visualization

This guide provides step-by-step instructions and terminal commands to start mapping on the **Keenon T2 delivery robot**, interact with ROS services, and run **RViz** on your local workstation.

---

## 1. Network & Prerequisites

- **Robot IP**: `192.168.64.20`
- **Wi-Fi AP SSID**: `Keenon_robot_E60643` (Password: `keenonrobot`)
- **SSH User**: `peanut@192.168.64.20`
- **Sudo Password (`peanut`)**: `root`

### Connect Computer to Robot Wi-Fi (if not using ethernet):
```bash
nmcli dev wifi connect Keenon_robot_E60643 password keenonrobot
```

### Test SSH Connection:
```bash
ssh peanut@192.168.64.20
```

---

## 2. Starting Mapping on the Robot

You can start mapping using either **OpenT2 SLAM** or **Keenon Proprietary Services**.

### Option A: OpenT2 Cartographer Mapping (Recommended)

1. SSH into the robot and source both ROS Indigo and `open_t2_ws`:
   ```bash
   ssh peanut@192.168.64.20 "source /opt/ros/indigo/setup.bash && source /home/peanut/open_t2_ws/devel/setup.bash && roslaunch open_t2_mapping mapping.launch"
   ```

### Option B: Proprietary Keenon SLAM / Services

1. Check active ROS mapping topics and nodes:
   ```bash
   ssh peanut@192.168.64.20 "source /opt/ros/indigo/setup.bash && rostopic list | grep map"
   ```
2. Trigger mapping mode via ROS topics/services:
   ```bash
   ssh peanut@192.168.64.20 "source /opt/ros/indigo/setup.bash && rostopic pub -1 /run_mapping std_msgs/Bool 'data: true'"
   ```

---

## 3. Starting Teleoperation (Driving the Robot)

Open a new terminal to drive the robot manually with keyboard controls during mapping:

```bash
ssh peanut@192.168.64.20 "source /opt/ros/indigo/setup.bash && rosrun teleop_twist_keyboard teleop_twist_keyboard.py"
```

**Controls:**
- `i`: Move forward
- `,`: Move backward
- `j`: Turn left in place
- `l`: Turn right in place
- `k`: Stop
- `q`/`z`: Increase / decrease speeds

---

## 4. Launching RViz on Your Local Workstation

Run ROS Noetic RViz inside Docker on your host PC pointing to `ROS_MASTER_URI=http://192.168.64.20:11311`.

### Step 1: Allow X11 Display Access
```bash
xhost +local:root
```

### Step 2: Launch Docker RViz Container
```bash
docker run -it --rm \
  --net=host \
  -e DISPLAY=$DISPLAY \
  -e QT_X11_NO_MITSHM=1 \
  -e ROS_MASTER_URI=http://192.168.64.20:11311 \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /home/juza/slam_t2:/workspace \
  osrf/ros:noetic-desktop-full \
  rviz
```

---

## 5. RViz Display Configuration (Fixing "Map Not Seeing")

Standard RViz does not ship with Cartographer's custom `Submaps` display plugin (which causes `PluginlibFactory: The plugin for class 'Submaps' failed to load`). Use standard ROS displays instead:

1. **Fixed Frame**: Set `Global Options` $\rightarrow$ `Fixed Frame` to `map` (or `odom_combined`).
2. **Add Occupancy Grid Map Display**:
   - Click **Add** (bottom left) $\rightarrow$ select **Map**.
   - Expand the new Map entry $\rightarrow$ set **Topic** to `/gmapping_map` (or `/map`).
3. **Add Laser Scans Display**:
   - Click **Add** $\rightarrow$ select **LaserScan**.
   - Set **Topic** to `/scan` (or `/scan_front_orig` and `/scan_back_orig`).
   - Set **Size (m)** to `0.05` and **Color Transformer** to `FlatColor` (Red/Green).
4. **Add TF / Robot Model Display**:
   - Click **Add** $\rightarrow$ select **TF** (shows frame tree: `map` $\rightarrow$ `odom_combined` $\rightarrow$ `base_link`).
   - Click **Add** $\rightarrow$ select **RobotModel** (if URDF parameter `/robot_description` is present).

---

## 6. Keenon Database & Map Services Reference

| Action | Service / Command | Description |
| :--- | :--- | :--- |
| **Switch Map** | `rosservice call /switch_map "{map_name: 'floor1'}"` | Dynamically loads a saved map layer from SQLite DB |
| **Save Current Pose** | `rosservice call /save_current_pose "{}"` | Saves active pose estimate to SQLite DB |
| **Save Initial Pose** | `rosservice call /save_current_init_pose "{}"` | Sets starting pose hypothesis |
| **Map Trans Config** | `/config_maptrans` | Configures floor transition transforms |

---

## 7. Saving the Completed Map

When mapping is complete, save the map files (`.yaml` and `.pgm`):

```bash
ssh peanut@192.168.64.20 "source /opt/ros/indigo/setup.bash && mkdir -p /home/peanut/maps && rosrun map_server map_saver -f /home/peanut/maps/my_building_map"
```
