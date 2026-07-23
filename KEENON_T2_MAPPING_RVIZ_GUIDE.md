# OpenT2 - SLAM Mapping Guide & Conflict Resolution

## ⚠️ CRITICAL WARNING: Active ROS Node Conflicts

By default, the robot automatically starts Keenon's proprietary background stack on boot:
```bash
/usr/bin/python /opt/ros/indigo/bin/roslaunch /opt/ros/indigo/share/robot_settings/launch/keenon_robot.launch
```

### Why is this a problem?
If `keenon_robot.launch` is running in the background and you launch `open_t2_mapping mapping.launch`:
1. **TF Tree Corruption**: Both stacks fight to publish the `map -> odom_combined` transform, causing RViz rendering jitter and pose jumps.
2. **Topic Contention**: Multiple nodes publish conflicting map data to `/map` and `/submap_list`.
3. **High CPU Overload**: Running 2 SLAM engines simultaneously exhausts onboard CPU resources.

---

## 🛠️ Solution: Choose ONE of the Two Workflow Paths

---

### PATH 1: Use OpenT2 Clean Stack (Recommended for Development)

Before starting `open_t2_mapping`, **you MUST stop the background Keenon stack**:

#### Step 1: Stop Background Keenon Stack
```bash
ssh peanut@192.168.64.20 "echo root | sudo -S killall -9 roslaunch cartographer_node slam_gmapping"
```

#### Step 2: Launch OpenT2 Clean Mapping
```bash
ssh peanut@192.168.64.20 "source /opt/ros/indigo/setup.bash && source /home/peanut/open_t2_ws/devel/setup.bash && roslaunch open_t2_mapping mapping.launch"
```

#### Step 3: Launch Teleoperation (Separate Terminal)
```bash
ssh peanut@192.168.64.20 "source /opt/ros/indigo/setup.bash && rosrun teleop_twist_keyboard teleop_twist_keyboard.py"
```

#### Step 4: Launch RViz on Workstation
```bash
xhost +local:root

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
*In RViz: Set **Fixed Frame** to `map`, add **Map** set to `/map`, and add **LaserScan** set to `/scan`.*

---

### PATH 2: Use Already-Running Keenon Stack (Zero Setup)

If you leave `keenon_robot.launch` running, **DO NOT run `roslaunch open_t2_mapping`**. The robot is already mapping!

#### Step 1: Directly Connect Workstation RViz
```bash
xhost +local:root

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

#### Step 2: RViz Display Settings for Keenon Stack
- **Fixed Frame**: Set to `map`
- **Map Display**: Set Topic to `/gmapping_map` (or `/map`)
- **LaserScan Display**: Set Topic to `/scan_front_orig` and `/scan_back_orig`
- **TF Display**: Enabled

#### Step 3: Teleoperate Robot (Separate Terminal)
```bash
ssh peanut@192.168.64.20 "source /opt/ros/indigo/setup.bash && rosrun teleop_twist_keyboard teleop_twist_keyboard.py"
```

---

## 💾 Saving the Map

When finished mapping (using either Path 1 or Path 2):

```bash
ssh peanut@192.168.64.20 "source /opt/ros/indigo/setup.bash && mkdir -p /home/peanut/maps && rosrun map_server map_saver -f /home/peanut/maps/my_building_map"
```
