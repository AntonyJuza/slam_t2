#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OpenT2 Map Manager Node
Authoritative map database manager, compiler runner, and map publisher for OpenT2.
- Serves latched /map (for move_base) and /map_amcl (for AMCL).
- Manages SQLite catalog at /home/peanut/opent2/db/opent2.db.
- Exposes ROS services for map listing, feature editing, compiling, and atomic activation.
- Supervizes SLAM Mapping Lifecycle (Cartographer start/stop/save and AMCL coordination).
- Compatible with ROS Indigo (Python 2.7) and modern ROS/Python 3.
"""

from __future__ import print_function, division, absolute_import
import os
import sys
import json
import time
import shutil
import signal
import subprocess
import numpy as np

import rospy
from nav_msgs.msg import OccupancyGrid, MapMetaData
from geometry_msgs.msg import Pose, Point, Quaternion
from std_msgs.msg import String, Header, UInt8, Bool, Empty
from std_srvs.srv import Trigger, TriggerResponse

# Support both relative import and installed path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

from opent2_db import OpenT2Database
from opent2_compiler import (
    OpenT2Compiler, read_yaml, read_pgm, write_pgm, write_yaml,
    FREE_VAL, OCCUPIED_VAL, UNKNOWN_VAL
)


def pgm_to_occupancy_grid(pgm_path, yaml_path, frame_id="map"):
    meta = read_yaml(yaml_path)
    arr, w, h, _ = read_pgm(pgm_path)
    res = meta["resolution"]
    origin = meta["origin"]

    grid = OccupancyGrid()
    grid.header.stamp = rospy.Time.now()
    grid.header.frame_id = frame_id

    grid.info.map_load_time = rospy.Time.now()
    grid.info.resolution = res
    grid.info.width = w
    grid.info.height = h

    grid.info.origin.position.x = origin[0]
    grid.info.origin.position.y = origin[1]
    grid.info.origin.position.z = origin[2] if len(origin) > 2 else 0.0
    grid.info.origin.orientation.x = 0.0
    grid.info.origin.orientation.y = 0.0
    grid.info.origin.orientation.z = 0.0
    grid.info.origin.orientation.w = 1.0

    # In ROS OccupancyGrid data array:
    # row 0 is bottom row (y = origin_y), row h-1 is top row
    # In PGM file, row 0 is TOP row (y = origin_y + h*res)
    # So we must invert vertically (flip upside down)
    flipped = np.flipud(arr)

    # Convert PGM values (254=free, 0=occupied, 205=unknown) to OccupancyGrid (0=free, 100=occupied, -1=unknown)
    cost_grid = np.full(flipped.shape, -1, dtype=np.int8)
    cost_grid[flipped == FREE_VAL] = 0
    cost_grid[flipped == OCCUPIED_VAL] = 100
    mask_other = (flipped != FREE_VAL) & (flipped != OCCUPIED_VAL) & (flipped != UNKNOWN_VAL)
    if np.any(mask_other):
        cost_grid[mask_other] = np.int8((255 - flipped[mask_other]) * 100 // 255)

    grid.data = cost_grid.flatten().tolist()
    return grid


def occupancy_grid_to_pgm_yaml(grid, pgm_path, yaml_path):
    w = grid.info.width
    h = grid.info.height
    res = grid.info.resolution
    origin = [
        grid.info.origin.position.x,
        grid.info.origin.position.y,
        0.0
    ]

    arr = np.array(grid.data, dtype=np.int8).reshape((h, w))
    # ROS grid row 0 is bottom row; PGM row 0 is top row -> vertical flip
    flipped = np.flipud(arr)

    # Auto-crop bounding box of known cells (cell != -1) with 15 cells padding
    known_mask = (flipped != -1)
    if np.any(known_mask):
        rows = np.any(known_mask, axis=1)
        cols = np.any(known_mask, axis=0)
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        pad = 15
        rmin = max(0, rmin - pad)
        rmax = min(h - 1, rmax + pad)
        cmin = max(0, cmin - pad)
        cmax = min(w - 1, cmax + pad)

        flipped = flipped[rmin:rmax+1, cmin:cmax+1]
        origin[0] = origin[0] + cmin * res
        origin[1] = origin[1] + (h - 1 - rmax) * res

    pgm_arr = np.full(flipped.shape, UNKNOWN_VAL, dtype=np.uint8)
    pgm_arr[flipped == 0] = FREE_VAL
    pgm_arr[flipped >= 50] = OCCUPIED_VAL
    # Intermediate cells
    mask_other = (flipped > 0) & (flipped < 50)
    if np.any(mask_other):
        pgm_arr[mask_other] = np.uint8((100 - flipped[mask_other]) * 254 // 100)

    write_pgm(pgm_path, pgm_arr)
    write_yaml(yaml_path, os.path.basename(pgm_path), res, origin)


class OpenT2MapManagerNode(object):
    def __init__(self):
        if not rospy.core.is_initialized():
            rospy.init_node("opent2_map_manager", anonymous=False)

        # Parameters
        self.maps_root = rospy.get_param("~maps_root", "/home/peanut/opent2_maps")
        self.db_path = rospy.get_param("~db_path", os.path.join(self.maps_root, "opent2.db"))
        self.default_map_id = rospy.get_param("~default_map_id", "default_floor")

        if not os.path.exists(self.maps_root):
            os.makedirs(self.maps_root)

        # Initialize DB and Compiler
        self.db = OpenT2Database(self.db_path)
        self.compiler = OpenT2Compiler()

        # State tracking for mapping lifecycle
        self.is_mapping = False
        self.cartographer_proc = None

        # Latched ROS Publishers
        self.pub_map = rospy.Publisher("/map", OccupancyGrid, queue_size=1, latch=True)
        self.pub_map_amcl = rospy.Publisher("/map_amcl", OccupancyGrid, queue_size=1, latch=True)
        self.pub_status = rospy.Publisher("/opent2/active_map_status", String, queue_size=1, latch=True)
        self.pub_mapping_status = rospy.Publisher("/mapping_status", UInt8, queue_size=1, latch=True)
        self.pub_mapping_info = rospy.Publisher("/opent2/mapping/status", String, queue_size=1, latch=True)

        # ROS Services
        rospy.Service("/opent2/map/list_maps", Trigger, self.handle_list_maps)
        rospy.Service("/opent2/map/activate_revision", Trigger, self.handle_activate_revision)
        rospy.Service("/opent2/map/publish_revision", Trigger, self.handle_publish_revision)
        rospy.Service("/opent2/map/reload_active", Trigger, self.handle_reload_active)
        rospy.Service("/opent2/mapping/start", Trigger, self.handle_service_start_mapping)
        rospy.Service("/opent2/mapping/stop", Trigger, self.handle_service_stop_mapping)
        rospy.Service("/opent2/mapping/save", Trigger, self.handle_service_save_mapping)

        # Command Subscribers
        self.sub_activate = rospy.Subscriber("/opent2/map/command_activate", String, self.handle_command_activate)
        self.sub_save_features = rospy.Subscriber("/opent2/map/save_features", String, self.handle_save_features)
        self.sub_run_mapping = rospy.Subscriber("/run_mapping", UInt8, self.handle_run_mapping)
        self.sub_run_mapping_str = rospy.Subscriber("/run_mapping_cmd", String, self.handle_run_mapping_str)
        self.sub_save_new_map_bool = rospy.Subscriber("/save_new_map", Bool, self.handle_save_new_map_bool)
        self.sub_save_new_map_empty = rospy.Subscriber("/save_new_map_trigger", Empty, self.handle_save_new_map_empty)

        # Publish initial mapping status (0 = IDLE)
        self.pub_mapping_status.publish(UInt8(data=0))
        self.pub_mapping_info.publish(String(data=json.dumps({"is_mapping": False, "status": "IDLE"})))

        # Ensure baseline map is registered and active
        self._ensure_baseline_map()

        # Publish initial active map
        self.publish_active_map()

        rospy.loginfo("OpenT2 Map Manager Node initialized successfully.")

    def _ensure_baseline_map(self):
        active = self.db.get_active_map()
        if active:
            return

        # Check for existing map files on the robot
        candidate_paths = [
            ("/home/peanut/maps/my_new_map_cropped.pgm", "/home/peanut/maps/my_new_map_cropped.yaml"),
            ("/home/peanut/maps/new_map_cropped.pgm", "/home/peanut/maps/new_map_cropped.yaml"),
            (os.path.join(script_dir, "../maps/map.pgm"), os.path.join(script_dir, "../maps/map.yaml")),
        ]

        found_pgm, found_yaml = None, None
        for p, y in candidate_paths:
            if os.path.exists(p) and os.path.exists(y):
                found_pgm, found_yaml = p, y
                break

        if not found_pgm:
            rospy.logwarn("No baseline map found to initialize OpenT2 Map Manager.")
            return

        rospy.loginfo("Bootstrapping baseline map from %s", found_pgm)
        map_id = self.default_map_id
        map_dir = os.path.join(self.maps_root, "maps", map_id)
        base_dir = os.path.join(map_dir, "base")
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        dst_pgm = os.path.join(base_dir, "base.pgm")
        dst_yaml = os.path.join(base_dir, "base.yaml")
        shutil.copyfile(found_pgm, dst_pgm)
        shutil.copyfile(found_yaml, dst_yaml)

        from opent2_compiler import compute_sha256
        sha = compute_sha256(dst_pgm)
        meta = read_yaml(dst_yaml)
        arr, w, h, _ = read_pgm(dst_pgm)

        self.db.create_or_update_map(
            map_id=map_id,
            name="Main Floor (Baseline)",
            floor_level=1,
            resolution=meta["resolution"],
            width=w,
            height=h,
            origin_x=meta["origin"][0],
            origin_y=meta["origin"][1],
            origin_yaw=meta["origin"][2] if len(meta["origin"]) > 2 else 0.0,
            base_pbstream_rel="base/base.pbstream",
            base_yaml_rel="base/base.yaml",
            base_pgm_rel="base/base.pgm",
            base_sha256=sha
        )

        # Compile initial Revision 1 (clean base with 0 features)
        rev1_dir = os.path.join(map_dir, "revisions", "rev_1")
        manifest = self.compiler.compile(
            base_pgm_path=dst_pgm,
            base_yaml_path=dst_yaml,
            output_dir=rev1_dir,
            features=[],
            revision_number=1,
            map_id=map_id
        )

        self.db.publish_revision(
            map_id=map_id,
            revision_number=1,
            bundle_relpath="revisions/rev_1",
            bundle_sha256=manifest["bundle_sha256"],
            features_snapshot=[],
            map_yaml_rel="revisions/rev_1/map.yaml",
            map_pgm_rel="revisions/rev_1/map.pgm",
            map_amcl_yaml_rel="revisions/rev_1/map_amcl.yaml",
            map_amcl_pgm_rel="revisions/rev_1/map_amcl.pgm",
            thumbnail_rel="revisions/rev_1/thumbnail.png",
            published_by="system_init",
            notes="Initial baseline revision"
        )

        self.db.set_active_map(map_id, 1, activated_by="system_init")
        rospy.loginfo("Baseline revision 1 successfully created and activated.")

    def publish_active_map(self):
        active = self.db.get_active_map()
        if not active:
            rospy.logwarn("No active map set in database.")
            return False

        map_id = active["map_id"]
        map_dir = os.path.join(self.maps_root, "maps", map_id)
        map_pgm = os.path.join(map_dir, active["map_pgm_relpath"])
        map_yaml = os.path.join(map_dir, active["map_yaml_relpath"])
        amcl_pgm = os.path.join(map_dir, active["map_amcl_pgm_relpath"])
        amcl_yaml = os.path.join(map_dir, active["map_amcl_yaml_relpath"])

        if not os.path.exists(map_pgm) or not os.path.exists(amcl_pgm):
            rospy.logerr("Active map files missing: %s or %s", map_pgm, amcl_pgm)
            return False

        rospy.loginfo("Publishing active map: %s (rev %d)", map_id, active["active_revision"])

        grid_nav = pgm_to_occupancy_grid(map_pgm, map_yaml, frame_id="map")
        grid_amcl = pgm_to_occupancy_grid(amcl_pgm, amcl_yaml, frame_id="map")

        self.pub_map.publish(grid_nav)
        self.pub_map_amcl.publish(grid_amcl)

        status_msg = json.dumps({
            "map_id": map_id,
            "revision": active["active_revision"],
            "name": active["name"],
            "resolution": active["resolution"],
            "width": active["width"],
            "height": active["height"],
            "activated_at": active["activated_at"],
            "sha256": active["bundle_sha256"],
            "status": "ACTIVE_MAP_PUBLISHED",
            "success": True
        })
        self.pub_status.publish(String(data=status_msg))
        return True

    # --- MAPPING LIFECYCLE MANAGEMENT ---

    def _set_amcl_tf_broadcast(self, enable):
        try:
            import dynamic_reconfigure.client
            client = dynamic_reconfigure.client.Client("/amcl", timeout=1.5)
            client.update_configuration({"tf_broadcast": bool(enable)})
            rospy.loginfo("Set AMCL tf_broadcast to %s", str(enable))
            return True
        except Exception as e:
            rospy.logwarn("Failed to set AMCL tf_broadcast: %s", str(e))
            return False

    def start_mapping(self):
        if self.is_mapping:
            rospy.loginfo("Mapping is already active.")
            self.pub_mapping_status.publish(UInt8(data=2))
            return True

        rospy.loginfo("Starting OpenT2 Cartographer SLAM session...")

        # 1. Disable AMCL TF broadcast to avoid conflict with Cartographer map->odom
        self._set_amcl_tf_broadcast(False)

        # 2. Launch Cartographer
        try:
            launch_cmd = [
                "roslaunch", "open_t2_mapping", "cartographer_slam.launch"
            ]
            self.cartographer_proc = subprocess.Popen(
                launch_cmd,
                preexec_fn=os.setsid,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.is_mapping = True
            self.pub_mapping_status.publish(UInt8(data=2))
            self.pub_mapping_info.publish(String(data=json.dumps({
                "is_mapping": True,
                "status": "ACTIVE",
                "message": "Cartographer SLAM running"
            })))
            rospy.loginfo("Cartographer SLAM started with PID %d", self.cartographer_proc.pid)
            return True
        except Exception as e:
            rospy.logerr("Failed to launch Cartographer SLAM: %s", str(e))
            self._set_amcl_tf_broadcast(True)
            return False

    def stop_mapping(self):
        if not self.is_mapping:
            rospy.loginfo("Mapping is already stopped / idle.")
            self.pub_mapping_status.publish(UInt8(data=0))
            return True

        rospy.loginfo("Stopping OpenT2 Cartographer SLAM session...")

        # 1. Gracefully terminate Cartographer process
        if self.cartographer_proc:
            try:
                os.killpg(os.getpgid(self.cartographer_proc.pid), signal.SIGINT)
                for _ in range(25):
                    if self.cartographer_proc.poll() is not None:
                        break
                    time.sleep(0.1)
                if self.cartographer_proc.poll() is None:
                    os.killpg(os.getpgid(self.cartographer_proc.pid), signal.SIGKILL)
            except Exception as e:
                rospy.logwarn("Exception stopping cartographer process: %s", str(e))
            self.cartographer_proc = None

        self.is_mapping = False
        self.pub_mapping_status.publish(UInt8(data=0))
        self.pub_mapping_info.publish(String(data=json.dumps({
            "is_mapping": False,
            "status": "IDLE",
            "message": "Cartographer SLAM stopped"
        })))

        # 2. Re-enable AMCL TF broadcast
        self._set_amcl_tf_broadcast(True)

        # 3. Republish active map from database
        self.publish_active_map()
        rospy.loginfo("Cartographer SLAM stopped; active map republished.")
        return True

    def save_new_map_from_scan(self, map_id=None, map_name=None):
        grid = None
        try:
            grid = rospy.wait_for_message("/map", OccupancyGrid, timeout=3.0)
        except Exception as e:
            rospy.logwarn("Failed to capture live /map: %s", str(e))

        if not grid:
            rospy.logwarn("No occupancy grid available to save new map.")
            return False, "No occupancy grid available to save"
        target_map_id = map_id or self.default_map_id
        target_name = map_name or ("Scanned Map %s" % time.strftime("%Y-%m-%d %H:%M"))

        map_dir = os.path.join(self.maps_root, "maps", target_map_id)
        base_dir = os.path.join(map_dir, "base")
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        base_pgm = os.path.join(base_dir, "base.pgm")
        base_yaml = os.path.join(base_dir, "base.yaml")

        try:
            occupancy_grid_to_pgm_yaml(grid, base_pgm, base_yaml)
            from opent2_compiler import compute_sha256
            sha = compute_sha256(base_pgm)

            w = grid.info.width
            h = grid.info.height
            res = grid.info.resolution
            ox = grid.info.origin.position.x
            oy = grid.info.origin.position.y

            self.db.create_or_update_map(
                map_id=target_map_id,
                name=target_name,
                floor_level=1,
                resolution=res,
                width=w,
                height=h,
                origin_x=ox,
                origin_y=oy,
                origin_yaw=0.0,
                base_pbstream_rel="base/base.pbstream",
                base_yaml_rel="base/base.yaml",
                base_pgm_rel="base/base.pgm",
                base_sha256=sha
            )

            # Compile clean Revision 1
            rev1_dir = os.path.join(map_dir, "revisions", "rev_1")
            manifest = self.compiler.compile(
                base_pgm_path=base_pgm,
                base_yaml_path=base_yaml,
                output_dir=rev1_dir,
                features=[],
                revision_number=1,
                map_id=target_map_id
            )

            self.db.publish_revision(
                map_id=target_map_id,
                revision_number=1,
                bundle_relpath="revisions/rev_1",
                bundle_sha256=manifest["bundle_sha256"],
                features_snapshot=[],
                map_yaml_rel="revisions/rev_1/map.yaml",
                map_pgm_rel="revisions/rev_1/map.pgm",
                map_amcl_yaml_rel="revisions/rev_1/map_amcl.yaml",
                map_amcl_pgm_rel="revisions/rev_1/map_amcl.pgm",
                thumbnail_rel="revisions/rev_1/thumbnail.png",
                published_by="slam_scan",
                notes="Initial scan baseline"
            )

            # Activate Revision 1
            self.db.set_active_map(target_map_id, 1, activated_by="save_new_map")
            if self.is_mapping:
                self.stop_mapping()
            else:
                self.publish_active_map()

            rospy.loginfo("New map %s successfully saved and activated as Rev 1", target_map_id)
            return True, "Map %s saved as Rev 1 (sha: %s)" % (target_map_id, sha[:8])
        except Exception as e:
            rospy.logerr("Failed to save new map: %s", str(e))
            return False, str(e)

    # --- TOPIC HANDLERS ---

    def handle_run_mapping(self, msg):
        val = msg.data
        rospy.loginfo("Received /run_mapping command: %d", val)
        if val == 2:
            self.start_mapping()
        elif val == 0:
            self.stop_mapping()

    def handle_run_mapping_str(self, msg):
        cmd = msg.data.strip().lower()
        rospy.loginfo("Received /run_mapping_cmd: %s", cmd)
        if cmd in ("start", "2", "true"):
            self.start_mapping()
        elif cmd in ("stop", "0", "false"):
            self.stop_mapping()

    def handle_save_new_map_bool(self, msg):
        if msg.data:
            self.save_new_map_from_scan()

    def handle_save_new_map_empty(self, msg):
        self.save_new_map_from_scan()

    def handle_command_activate(self, msg):
        try:
            data = json.loads(msg.data)
            map_id = data.get("map_id", self.default_map_id)
            rev_num = int(data.get("revision", 1))
            rospy.loginfo("Received command to activate map: %s (rev %d)", map_id, rev_num)
            rospy.set_param("~target_revision", rev_num)
            rospy.set_param("~target_map_id", map_id)
            self.db.set_active_map(map_id, rev_num, activated_by="command_topic")
            self.publish_active_map()
        except Exception as e:
            rospy.logerr("Failed to activate map from topic: %s", str(e))

    def handle_save_features(self, msg):
        try:
            data = json.loads(msg.data)
            map_id = data.get("map_id", self.default_map_id)
            notes = data.get("notes", "Published from T2 Tera App")
            published_by = data.get("published_by", "t2_tera_app")
            features = data.get("features", [])

            rospy.loginfo("Received %d features to save for map: %s", len(features), map_id)

            m = self.db.get_map(map_id)
            if not m:
                rospy.logerr("Map not found: %s", map_id)
                return

            # Insert or replace features
            for f in features:
                kind = f.get("kind", "waypoint")
                name = f.get("name", "Feature")
                geom = f.get("geometry", [])
                props = f.get("properties", {})
                feat_id = f.get("feature_id")
                if feat_id:
                    self.db.delete_feature(feat_id, soft_delete=False)
                self.db.add_feature(
                    map_id=map_id,
                    kind=kind,
                    name=name,
                    geometry=geom,
                    properties=props,
                    feature_id=feat_id
                )

            # Compile next revision
            all_features = self.db.get_features(map_id, include_deleted=False)
            latest_rev = self.db.get_latest_revision_number(map_id)
            next_rev = latest_rev + 1

            map_dir = os.path.join(self.maps_root, "maps", map_id)
            base_pgm = os.path.join(map_dir, m["base_pgm_relpath"])
            base_yaml = os.path.join(map_dir, m["base_yaml_relpath"])
            rev_dir = os.path.join(map_dir, "revisions", "rev_%d" % next_rev)

            manifest = self.compiler.compile(
                base_pgm_path=base_pgm,
                base_yaml_path=base_yaml,
                features=all_features,
                output_dir=rev_dir,
                revision_number=next_rev,
                map_id=map_id
            )

            bundle_rel = "revisions/rev_%d" % next_rev
            self.db.publish_revision(
                map_id=map_id,
                revision_number=next_rev,
                bundle_relpath=bundle_rel,
                bundle_sha256=manifest["bundle_sha256"],
                features_snapshot=all_features,
                map_yaml_rel=bundle_rel + "/map.yaml",
                map_pgm_rel=bundle_rel + "/map.pgm",
                map_amcl_yaml_rel=bundle_rel + "/map_amcl.yaml",
                map_amcl_pgm_rel=bundle_rel + "/map_amcl.pgm",
                thumbnail_rel=bundle_rel + "/thumbnail.png",
                published_by=published_by,
                notes=notes
            )

            # Auto-activate newly published revision
            self.db.set_active_map(map_id, next_rev, activated_by="publish_save_features")
            self.publish_active_map()
            rospy.loginfo("Successfully compiled and activated revision %d for map %s", next_rev, map_id)
        except Exception as e:
            rospy.logerr("Failed to save features: %s", str(e))

    # --- SERVICE HANDLERS ---

    def handle_reload_active(self, req):
        success = self.publish_active_map()
        return TriggerResponse(success=success, message="Active map reloaded and published")

    def handle_service_start_mapping(self, req):
        success = self.start_mapping()
        return TriggerResponse(success=success, message="Cartographer SLAM started" if success else "Failed to start mapping")

    def handle_service_stop_mapping(self, req):
        success = self.stop_mapping()
        return TriggerResponse(success=success, message="Cartographer SLAM stopped" if success else "Failed to stop mapping")

    def handle_service_save_mapping(self, req):
        success, msg = self.save_new_map_from_scan()
        return TriggerResponse(success=success, message=msg)

    def handle_list_maps(self, req):
        try:
            maps = self.db.list_maps()
            for m in maps:
                m["revisions"] = self.db.get_revisions(m["map_id"])
            active = self.db.get_active_map()
            payload = {
                "maps": maps,
                "active_map": active
            }
            return TriggerResponse(success=True, message=json.dumps(payload))
        except Exception as e:
            return TriggerResponse(success=False, message=str(e))

    def handle_activate_revision(self, req):
        try:
            map_id = rospy.get_param("~target_map_id", self.default_map_id)
            if rospy.has_param("~target_revision"):
                rev_num = int(rospy.get_param("~target_revision"))
            else:
                active = self.db.get_active_map()
                rev_num = active["active_revision"] if active else 1
            self.db.set_active_map(map_id, rev_num, activated_by="service_call")
            success = self.publish_active_map()
            return TriggerResponse(success=success, message="Map activated: %s rev %d" % (map_id, rev_num))
        except Exception as e:
            return TriggerResponse(success=False, message=str(e))

    def handle_publish_revision(self, req):
        try:
            map_id = rospy.get_param("~target_map_id", self.default_map_id)
            m = self.db.get_map(map_id)
            if not m:
                return TriggerResponse(success=False, message="Map not found: " + map_id)

            features = self.db.get_features(map_id, include_deleted=False)
            latest_rev = self.db.get_latest_revision_number(map_id)
            next_rev = latest_rev + 1

            map_dir = os.path.join(self.maps_root, "maps", map_id)
            base_pgm = os.path.join(map_dir, m["base_pgm_relpath"])
            base_yaml = os.path.join(map_dir, m["base_yaml_relpath"])
            rev_dir = os.path.join(map_dir, "revisions", "rev_%d" % next_rev)

            manifest = self.compiler.compile(
                base_pgm_path=base_pgm,
                base_yaml_path=base_yaml,
                output_dir=rev_dir,
                features=features,
                revision_number=next_rev,
                map_id=map_id
            )

            bundle_rel = "revisions/rev_%d" % next_rev
            self.db.publish_revision(
                map_id=map_id,
                revision_number=next_rev,
                bundle_relpath=bundle_rel,
                bundle_sha256=manifest["bundle_sha256"],
                features_snapshot=features,
                map_yaml_rel=bundle_rel + "/map.yaml",
                map_pgm_rel=bundle_rel + "/map.pgm",
                map_amcl_yaml_rel=bundle_rel + "/map_amcl.yaml",
                map_amcl_pgm_rel=bundle_rel + "/map_amcl.pgm",
                thumbnail_rel=bundle_rel + "/thumbnail.png",
                published_by="operator",
                notes="Published via ROS service"
            )

            self.db.set_active_map(map_id, next_rev, activated_by="publish_auto")
            self.publish_active_map()

            return TriggerResponse(success=True, message="Published and activated revision %d" % next_rev)
        except Exception as e:
            return TriggerResponse(success=False, message=str(e))


if __name__ == "__main__":
    try:
        node = OpenT2MapManagerNode()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
