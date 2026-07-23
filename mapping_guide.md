# Keenon T2 SLAM & Mapping Guide
### Custom Cartographer & RViz Integration Pipeline

This document outlines the step-by-step procedure to run our custom mapping stack on the Keenon T2 robot, bridge it to a modern RViz instance running on a host machine, drive the robot using teleoperation, and save the completed map.

---

## 1. Automatic Proprietary Stack Behavior

When the Keenon T2 robot is powered on, it automatically launches the proprietary Keenon navigation and mapping stack.

* **Upstart Service:** Controlled by `/etc/init/keenonrobot.conf`.
* **Execution Script:** It sources `/opt/ros/indigo/setup.sh` and runs `roslaunch /opt/ros/indigo/share/robot_settings/launch/keenon_robot.launch`.
* **Auto-Restart:** The Upstart service is configured to `respawn` automatically. If any core proprietary nodes are terminated individually, they will be restarted, causing resource conflicts (e.g., port and hardware socket locks for the LiDARs and STM32 chassis).

> [!WARNING]
> Before launching our custom Cartographer mapping stack, you **MUST** stop the proprietary `keenonrobot` service and clean up all leftover ROS/Python processes. Failing to do so will result in laser sensor publication conflicts and master-node registration failures.

---

## 2. Step 1: Deactivating the Proprietary Stack

To stop the proprietary stack and ensure a clean environment, execute the following commands on the robot.

1. **Stop the Upstart Service:**
   ```bash
   ssh peanut@192.168.64.20 "echo 'root' | sudo -S service keenonrobot stop"
   ```
   *Note: The sudo password for the user `peanut` is `root`.*

2. **Force-Kill Leftover Processes:**
   Since Upstart may fail to clean up every background node, run this command to terminate all remaining ROS and Python nodes:
   ```bash
   ssh peanut@192.168.64.20 "pkill -u peanut -9 -f ros ; pkill -u peanut -9 -f python"
   ```

3. **Clear Stale Screens:**
   ```bash
   ssh peanut@192.168.64.20 "screen -wipe"
   ```

---

## 3. Step 2: Launching the Custom Mapping Stack

Our custom stack consists of three separate components running inside `screen` sessions on the robot:

### A. The Mapping launch stack (ROS Master + Hardware Nodes + Cartographer)
This starts the chassis driver, front-end location estimators, SDKELI LiDAR nodes, LiDAR filter nodes, Cartographer, and the occupancy grid builder.
```bash
ssh peanut@192.168.64.20 "screen -S mapping -d -m bash -c 'source /opt/ros/indigo/setup.bash && source /home/peanut/open_t2_ws/devel/setup.bash && export ROS_IP=192.168.64.20 && export ROS_MASTER_URI=http://192.168.64.20:11311 && roslaunch open_t2_mapping mapping.launch >/home/peanut/mapping.log 2>&1'"
```

### B. The TF Cleaner Node
Because the robot runs **ROS Indigo** (which uses leading slashes in TF frame IDs like `/base_link`) and the host runs **ROS Noetic** (which strictly forbids leading slashes in TF frame IDs), we must clean the transforms on the fly.
```bash
ssh peanut@192.168.64.20 "screen -S tf_cleaner -d -m bash -c 'source /opt/ros/indigo/setup.bash && export ROS_IP=192.168.64.20 && export ROS_MASTER_URI=http://192.168.64.20:11311 && python -u /home/peanut/tf_cleaner.py >/home/peanut/tf_cleaner.log 2>&1'"
```

### C. The Scan Filter Node
Filters out laser scan reflections/spikes close to the robot's base or wheels to prevent false obstacles:
```bash
ssh peanut@192.168.64.20 "screen -S scan_filter -d -m bash -c 'source /opt/ros/indigo/setup.bash && export ROS_IP=192.168.64.20 && export ROS_MASTER_URI=http://192.168.64.20:11311 && python -u /home/peanut/scan_filter.py >/home/peanut/scan_filter.log 2>&1'"
```


---

## 4. Step 3: Activating Cartographer SLAM

By default, the Cartographer node launches in an idle state. It will not subscribe to the LiDAR scanners or construct submaps until it is triggered via the `/run_mapping` topic.

To activate mapping, publish the state value `2` (CARTOGRAPHER) to the topic:
```bash
ssh peanut@192.168.64.20 "source /opt/ros/indigo/setup.bash && export ROS_IP=192.168.64.20 && export ROS_MASTER_URI=http://192.168.64.20:11311 && rostopic pub -1 /run_mapping std_msgs/UInt8 'data: 2'"
```

---

## 5. Step 4: Launching RViz on the Host Machine

Because of the ROS version difference between the Robot (Indigo, Ubuntu 14.04) and modern systems, RViz is run inside a **ROS Noetic Docker Container** on the host machine.

### A. Environment Configuration
Verify your host IP address (`ROS_IP` on the host side) is reachable by the robot. (You can check it using `ip addr | grep 192.168.64`).
Ensure your firewall allows inbound ROS traffic from the robot:
```bash
sudo ufw allow from 192.168.64.20
```

### B. Run the RViz Docker Container
Launch the container, mapping the cleaned Indigo topics to standard topics expected by Noetic (use your actual host IP, e.g. `192.168.64.208`):
```bash
docker run -it --name rviz_opent2 \
  --net=host \
  --env ROS_MASTER_URI=http://192.168.64.20:11311 \
  --env ROS_IP=192.168.64.208 \
  --env DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /home/juza/slam_t2/OpenT2:/root/OpenT2 \
  osrf/ros:noetic-desktop-full \
  rviz -d /root/OpenT2/mapping/rviz/navigation.rviz \
  /tf:=/tf_clean \
  /tf_static:=/tf_static_clean \
  /bump:=/bump_clean \
  /scan_filtered:=/scan_filtered_clean \
  /map:=/map_clean


```
*Note: If the container is already created, you can simply start or restart it:*
```bash
docker restart rviz_opent2
```

---

## 6. Step 5: Teleoperating & Building the Map

1. **Start the Teleop keyboard node:**
   Open a new terminal on the host machine and SSH into the robot to run teleoperation:
   ```bash
   ssh -t peanut@192.168.64.20 "source /opt/ros/indigo/setup.bash && export ROS_IP=192.168.64.20 && export ROS_MASTER_URI=http://192.168.64.20:11311 && rosrun teleop_twist_keyboard teleop_twist_keyboard.py"
   ```

2. **Mapping Guidelines:**
   * Drive the robot slowly (ideal speed is < 0.2 m/s).
   * Avoid fast rotations. Spin the robot in place slowly to allow Cartographer's scan-matching to align scans.
   * Verify on RViz that the live laser scan aligns with the walls of the map.
   * If drift occurs, back up the robot into a previously mapped, high-feature area (loop closure) to correct the alignment.

---

## 7. Step 6: Saving the Map

Once the environment has been fully mapped and looks correct in RViz, save the map file to the robot's storage:

```bash
ssh peanut@192.168.64.20 "source /opt/ros/indigo/setup.bash && export ROS_IP=192.168.64.20 && export ROS_MASTER_URI=http://192.168.64.20:11311 && rosrun map_server map_saver -f /home/peanut/new_map"
```

This will generate two files in the `/home/peanut/` directory:
1. `new_map.pgm` (the actual occupancy grid image)
2. `new_map.yaml` (metadata details including resolution, origin, and thresholds)

---

## 8. WiFi Hotspot Auto-Off Issue

The robot runs a custom AP daemon (`keenonAP` via Upstart) that configures the wireless interface `wlanAP` into Access Point mode using `hostapd`. Concurrently running **NetworkManager** may attempt to manage this interface, periodically scanning and deactivating it.

> [!IMPORTANT]
> On Ubuntu 14.04, NetworkManager's version does **not** support the `interface-name:wlanAP` syntax in `NetworkManager.conf` and will throw an error (`invalid unmanaged-devices entry`). Use one of the two methods below to properly mark it as unmanaged.

### A. Quick Restart Command
If the WiFi AP goes down, restart the service to re-initialize it:
```bash
ssh peanut@192.168.64.20 "echo 'root' | sudo -S service keenonAP restart"
```

### B. Permanent Resolution (Stop Auto-Off)
Prevent NetworkManager from managing the `wlanAP` interface using one of these methods:

1. **Method 1: Interfaces Configuration (Recommended & Cleanest)**
   Since NetworkManager has `[ifupdown] managed=false` enabled, it will automatically ignore any interface defined in `/etc/network/interfaces`.
   
   Append the following to `/etc/network/interfaces` on the robot:
   ```text
   allow-hotplug wlanAP
   iface wlanAP inet manual
   ```

2. **Method 2: NetworkManager Config (By MAC Address)**
   Alternatively, add `wlanAP` to the unmanaged list in `/etc/NetworkManager/NetworkManager.conf` using its physical MAC address:
   ```ini
   [keyfile]
   unmanaged-devices=mac:00:12:0e:e6:06:43
   ```

3. **Restart the Services to Apply Changes:**
   ```bash
   ssh peanut@192.168.64.20 "echo 'root' | sudo -S service network-manager restart"
   ssh peanut@192.168.64.20 "echo 'root' | sudo -S service keenonAP restart"
   ```

---

## 9. Transitioning to Autonomous Navigation

Once you have successfully built and saved your map, you can use it to run autonomous navigation (AMCL localization + Move Base path planning).

### A. Shutdown the Mapping Stack
1. On the robot, stop the Cartographer mapping node:
   ```bash
   ssh peanut@192.168.64.20 "screen -S mapping -X quit"
   ```

### B. Launch the Navigation Stack
1. Run the navigation launcher on the robot. It will start a new ROS Master, load the saved map from `/home/peanut/new_map.yaml`, and initialize AMCL and Move Base:
   ```bash
   ssh peanut@192.168.64.20 "screen -S navigation -d -m bash -c 'source /opt/ros/indigo/setup.bash && source /home/peanut/open_t2_ws/devel/setup.bash && export ROS_IP=192.168.64.20 && export ROS_MASTER_URI=http://192.168.64.20:11311 && roslaunch open_t2_mapping navigation.launch map_file:=/home/peanut/new_map.yaml >/home/peanut/navigation.log 2>&1'"
   ```


2. **Restart the Helper Nodes (TF Cleaner & Scan Filter):**
   Because launching the navigation launcher starts a new ROS Master, you must restart the `tf_cleaner` and `scan_filter` nodes so they register with the new master:
   ```bash
   ssh peanut@192.168.64.20 "screen -S tf_cleaner -X quit ; screen -S tf_cleaner -d -m bash -c 'source /opt/ros/indigo/setup.bash && export ROS_IP=192.168.64.20 && export ROS_MASTER_URI=http://192.168.64.20:11311 && python -u /home/peanut/tf_cleaner.py >/home/peanut/tf_cleaner.log 2>&1'"
   ssh peanut@192.168.64.20 "screen -S scan_filter -X quit ; screen -S scan_filter -d -m bash -c 'source /opt/ros/indigo/setup.bash && export ROS_IP=192.168.64.20 && export ROS_MASTER_URI=http://192.168.64.20:11311 && python -u /home/peanut/scan_filter.py >/home/peanut/scan_filter.log 2>&1'"
   ```



### C. Visualize and Control in RViz
1. **Localize the Robot:**
   * If the robot is not positioned correctly on the map in RViz, click the **2D Pose Estimate** button at the top of RViz.
   * Click and drag on the map at the robot's physical location to align its orientation.
2. **Send Goals:**
   * Click the **2D Nav Goal** button at the top of RViz.
   * Click and drag anywhere on the map to set a goal pose. The robot will autonomously plan and drive to the target destination.

---

## Troubleshooting Checklist

| Issue | Cause | Solution |
|---|---|---|
| **Unable to register with Master** | Stale master or firewall blocking host. | Check UFW rules: `sudo ufw status`. Verify `ROS_IP` and `ROS_MASTER_URI` on both host and robot. |
| **LiDAR scans do not update** | `/run_mapping` was not triggered or proprietary service is still holding the USB port. | Run `rostopic pub` trigger command (Step 3). Verify `keenonrobot` service is stopped. |
| **No map showing up in RViz** | Noetic RViz is rejecting slash prefixes. | Verify `tf_cleaner.py` screen is active. Inspect output of `rostopic hz /tf_clean`. |
| **Map saver timeout** | `map_server` cannot connect to `/map` topic. | Ensure `cartographer_occupancy_grid_node` is running and publishing to `/map`. |
| **WiFi Hotspot disappears / disconnects** | NetworkManager is managing `wlanAP` and deactivating the hostapd bridge. | Follow the Permanent Resolution steps in Section 8 to mark `wlanAP` as unmanaged. |

