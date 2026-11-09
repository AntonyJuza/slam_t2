#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OpenT2 Deterministic Map Compiler
Combines immutable base occupancy grid with vector feature layers (erasers, keepouts)
to deterministically generate:
- map_amcl.pgm / map_amcl.yaml (Localization-safe: erasers only, no fake walls)
- map.pgm / map.yaml (Planning-safe: erasers + lethal keepout walls)
- thumbnail.png (Downscaled preview for Android UI)
- manifest.json & sha256.json (Integrity validation)
Compatible with Python 2.7 (Indigo) and Python 3.x.
"""

from __future__ import print_function, division, absolute_import
import os
import sys
import json
import hashlib
import numpy as np
import cv2

# Color encoding in standard ROS OccupancyGrid (8-bit grayscale PGM)
# In standard ROS PGM:
# 254 / 255 = Free space (Occupancy cost 0)
# 0         = Occupied space / Obstacle (Occupancy cost 100)
# 205       = Unknown space (Occupancy cost -1)
FREE_VAL = 254
OCCUPIED_VAL = 0
UNKNOWN_VAL = 205


def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def read_yaml(yaml_path):
    res = 0.05
    origin = [0.0, 0.0, 0.0]
    negate = 0
    occ_thresh = 0.65
    free_thresh = 0.196
    image = ""

    with open(yaml_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("image:"):
                image = line.split(":", 1)[1].strip()
            elif line.startswith("resolution:"):
                res = float(line.split(":", 1)[1].strip())
            elif line.startswith("negate:"):
                negate = int(line.split(":", 1)[1].strip())
            elif line.startswith("occupied_thresh:"):
                occ_thresh = float(line.split(":", 1)[1].strip())
            elif line.startswith("free_thresh:"):
                free_thresh = float(line.split(":", 1)[1].strip())
            elif line.startswith("origin:"):
                val_str = line.split(":", 1)[1].strip().strip("[]")
                origin = [float(x.strip()) for x in val_str.split(",") if x.strip()]

    return {
        "image": image,
        "resolution": res,
        "origin": origin,
        "negate": negate,
        "occupied_thresh": occ_thresh,
        "free_thresh": free_thresh
    }


def read_pgm(pgm_path):
    with open(pgm_path, "rb") as f:
        lines = []
        while len(lines) < 3:
            l = f.readline().strip()
            if not l or l.startswith(b"#"):
                continue
            lines.append(l)
        magic = lines[0]
        if magic != b"P5":
            raise ValueError("Only binary P5 PGM format is supported, got: " + str(magic))
        w, h = map(int, lines[1].split())
        maxval = int(lines[2])
        data = f.read()

    arr = np.frombuffer(data, dtype=np.uint8).reshape((h, w))
    return arr, w, h, maxval


def write_pgm(pgm_path, arr):
    h, w = arr.shape
    header = "P5\n# CREATOR: OpenT2 Deterministic Map Compiler\n{} {}\n255\n".format(w, h)
    # Binary write
    with open(pgm_path, "wb") as f:
        if sys.version_info[0] >= 3:
            f.write(header.encode("ascii"))
            f.write(arr.tobytes())
        else:
            f.write(header)
            f.write(arr.tostring())


def write_yaml(yaml_path, image_filename, resolution, origin):
    content = """image: {}
resolution: {:.6f}
origin: [{:.6f}, {:.6f}, {:.6f}]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.196
""".format(image_filename, resolution, origin[0], origin[1], origin[2] if len(origin) > 2 else 0.0)
    with open(yaml_path, "w") as f:
        f.write(content)


def world_to_pixel(x, y, origin_x, origin_y, resolution, height):
    """
    Transforms world coordinates in meters (map frame) to image pixel coordinates (col, row).
    In ROS map convention:
    Origin is the world coordinate of the bottom-left pixel (row = height - 1).
    x moves right (col increases: 0 -> width-1)
    y moves up (row decreases: height-1 -> 0)
    """
    col = int(round((x - origin_x) / resolution))
    row = int(round(height - 1 - ((y - origin_y) / resolution)))
    return col, row


def pixel_to_world(col, row, origin_x, origin_y, resolution, height):
    x = col * resolution + origin_x
    y = (height - 1 - row) * resolution + origin_y
    return x, y


class OpenT2Compiler(object):
    def __init__(self):
        pass

    def compile(self, base_pgm_path, base_yaml_path, output_dir, features,
                revision_number=1, map_id="default"):
        """
        Compiles base map and vector features into a versioned bundle inside output_dir.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 1. Read base map
        meta = read_yaml(base_yaml_path)
        base_arr, w, h, _ = read_pgm(base_pgm_path)
        res = meta["resolution"]
        origin = meta["origin"]
        orig_x, orig_y = origin[0], origin[1]

        # Clone base grid for AMCL and navigation
        arr_amcl = np.copy(base_arr)
        arr_nav = np.copy(base_arr)

        erasers = [f for f in features if f.get("kind") == "free_space_override" and f.get("is_enabled", 1)]
        keepouts = [f for f in features if f.get("kind") == "keepout" and f.get("is_enabled", 1)]
        waypoints = [f for f in features if f.get("kind") in ("waypoint", "charging_dock", "origin_point", "destination_point") and f.get("is_enabled", 1)]
        charging_stations = [f for f in features if f.get("kind") == "charging_dock" and f.get("is_enabled", 1)]
        origin_points = [f for f in features if f.get("kind") == "origin_point" and f.get("is_enabled", 1)]
        destination_points = [f for f in features if f.get("kind") == "destination_point" and f.get("is_enabled", 1)]

        # 2. Rasterize Ghost Erasers (applied to BOTH AMCL and Navigation)
        for f in erasers:
            geom = f.get("geometry")
            if not geom or not isinstance(geom, list):
                continue
            pts = []
            for pt in geom:
                c, r = world_to_pixel(pt[0], pt[1], orig_x, orig_y, res, h)
                pts.append([c, r])
            if len(pts) >= 3:
                cv2_pts = np.array([pts], dtype=np.int32)
                cv2.fillPoly(arr_amcl, cv2_pts, FREE_VAL)
                cv2.fillPoly(arr_nav, cv2_pts, FREE_VAL)

        # 3. Rasterize Keepouts (applied to Navigation ONLY)
        for f in keepouts:
            geom = f.get("geometry")
            if not geom or not isinstance(geom, list):
                continue
            pts = []
            for pt in geom:
                c, r = world_to_pixel(pt[0], pt[1], orig_x, orig_y, res, h)
                pts.append([c, r])
            if len(pts) >= 3:
                cv2_pts = np.array([pts], dtype=np.int32)
                cv2.fillPoly(arr_nav, cv2_pts, OCCUPIED_VAL)
            elif len(pts) == 2:
                # Line segment wall: draw with width of at least 3 cells (~15cm)
                thickness = 3
                cv2.line(arr_nav, (pts[0][0], pts[0][1]), (pts[1][0], pts[1][1]), OCCUPIED_VAL, thickness)

        # 4. Save compiled PGMs and YAMLs
        map_pgm_name = "map.pgm"
        map_yaml_name = "map.yaml"
        amcl_pgm_name = "map_amcl.pgm"
        amcl_yaml_name = "map_amcl.yaml"

        map_pgm_path = os.path.join(output_dir, map_pgm_name)
        map_yaml_path = os.path.join(output_dir, map_yaml_name)
        amcl_pgm_path = os.path.join(output_dir, amcl_pgm_name)
        amcl_yaml_path = os.path.join(output_dir, amcl_yaml_name)

        write_pgm(map_pgm_path, arr_nav)
        write_yaml(map_yaml_path, map_pgm_name, res, origin)

        write_pgm(amcl_pgm_path, arr_amcl)
        write_yaml(amcl_yaml_path, amcl_pgm_name, res, origin)

        # 5. Generate Thumbnail (downscaled 512x512 preview PNG for UI)
        thumb_name = "thumbnail.png"
        thumb_path = os.path.join(output_dir, thumb_name)
        thumb_size = 512
        scale = min(float(thumb_size) / w, float(thumb_size) / h)
        tw = int(w * scale)
        th = int(h * scale)
        resized = cv2.resize(arr_nav, (tw, th), interpolation=cv2.INTER_NEAREST)
        # Pad to exactly 512x512 with dark background
        thumb_canvas = np.full((thumb_size, thumb_size), 26, dtype=np.uint8)  # #1A1A1A
        ox = (thumb_size - tw) // 2
        oy = (thumb_size - th) // 2
        thumb_canvas[oy:oy+th, ox:ox+tw] = resized
        cv2.imwrite(thumb_path, thumb_canvas)

        # 6. Save Features Snapshot
        features_path = os.path.join(output_dir, "features.json")
        with open(features_path, "w") as f:
            json.dump(features, f, indent=2)

        # 7. Preflight Validations
        total_cells = w * h
        mapped_cells = int(np.sum(arr_nav != UNKNOWN_VAL))
        free_cells = int(np.sum(arr_nav == FREE_VAL))
        if mapped_cells == 0 or free_cells < 50:
            raise ValueError("Preflight Check FAILED: No mapped free space found (free_cells={}). Map may be empty.".format(free_cells))
        free_ratio_mapped = float(free_cells) / float(mapped_cells)
        if free_ratio_mapped < 0.05:
            raise ValueError("Preflight Check FAILED: Navigable free space ratio is too low ({:.2f}% of mapped space). Map may be corrupted or blocked.".format(free_ratio_mapped * 100))

        # Check waypoints reachability
        unreachable = []
        for wp in waypoints:
            geom = wp.get("geometry")
            if geom and len(geom) >= 2:
                wx, wy = geom[0], geom[1]
                c, r = world_to_pixel(wx, wy, orig_x, orig_y, res, h)
                if c < 0 or c >= w or r < 0 or r >= h:
                    unreachable.append(wp.get("name", "unnamed") + " (out of bounds)")
                elif arr_nav[r, c] == OCCUPIED_VAL:
                    unreachable.append(wp.get("name", "unnamed") + " (inside obstacle/keepout)")

        if unreachable:
            raise ValueError("Preflight Check FAILED: Waypoints unreachable: " + ", ".join(unreachable))

        # 8. Compute Checksums & Write Manifest
        files_to_hash = [map_pgm_name, map_yaml_name, amcl_pgm_name, amcl_yaml_name, thumb_name, "features.json"]
        sha_manifest = {}
        for fn in files_to_hash:
            fp = os.path.join(output_dir, fn)
            sha_manifest[fn] = compute_sha256(fp)

        sha_path = os.path.join(output_dir, "sha256.json")
        with open(sha_path, "w") as f:
            json.dump(sha_manifest, f, indent=2)

        manifest = {
            "map_id": map_id,
            "revision": revision_number,
            "width": w,
            "height": h,
            "resolution": res,
            "origin": origin,
            "free_space_ratio": free_ratio_mapped,
            "mapped_cells": mapped_cells,
            "free_cells": free_cells,
            "features_count": len(features),
            "charging_stations_count": len(charging_stations),
            "origin_points_count": len(origin_points),
            "destinations_count": len(destination_points),
            "keepouts_count": len(keepouts),
            "erasers_count": len(erasers),
            "files": sha_manifest,
            "bundle_sha256": sha_manifest[map_pgm_name]
        }
        manifest_path = os.path.join(output_dir, "manifest.json")
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)

        return manifest
