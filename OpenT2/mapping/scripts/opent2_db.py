#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OpenT2 Map Database Module
Provides SQLite persistence for maps, vector feature layers, published revisions,
active state, and audit logs.
Supports Python 2.7 (Indigo) and Python 3.x.
"""

from __future__ import print_function, division, absolute_import
import os
import sys
import json
import sqlite3
import hashlib
import time

CURRENT_SCHEMA_VERSION = 2

SCHEMA_SQL = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;
PRAGMA synchronous = NORMAL;

CREATE TABLE IF NOT EXISTS schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS maps (
    map_id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    floor_level INTEGER DEFAULT 1,
    resolution REAL NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    origin_x REAL NOT NULL,
    origin_y REAL NOT NULL,
    origin_yaw REAL NOT NULL DEFAULT 0.0,
    base_pbstream_relpath TEXT NOT NULL,
    base_yaml_relpath TEXT NOT NULL,
    base_pgm_relpath TEXT NOT NULL,
    base_sha256 TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS map_features (
    feature_id TEXT PRIMARY KEY,
    map_id TEXT NOT NULL REFERENCES maps(map_id) ON DELETE CASCADE,
    kind TEXT NOT NULL CHECK(kind IN (
        'keepout',
        'free_space_override',
        'speed_limit',
        'waypoint',
        'charging_dock',
        'origin_point',
        'destination_point'
    )),
    name TEXT NOT NULL,
    geometry_json TEXT NOT NULL,
    properties_json TEXT,
    is_enabled INTEGER DEFAULT 1 CHECK(is_enabled IN (0, 1)),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS map_revisions (
    revision_id INTEGER PRIMARY KEY AUTOINCREMENT,
    map_id TEXT NOT NULL REFERENCES maps(map_id) ON DELETE CASCADE,
    revision_number INTEGER NOT NULL,
    bundle_relpath TEXT NOT NULL,
    bundle_sha256 TEXT NOT NULL,
    features_snapshot_json TEXT NOT NULL,
    map_yaml_relpath TEXT NOT NULL,
    map_pgm_relpath TEXT NOT NULL,
    map_amcl_yaml_relpath TEXT NOT NULL,
    map_amcl_pgm_relpath TEXT NOT NULL,
    thumbnail_relpath TEXT,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    published_by TEXT DEFAULT 'operator',
    notes TEXT,
    UNIQUE(map_id, revision_number)
);

CREATE TABLE IF NOT EXISTS active_map_state (
    singleton_id INTEGER PRIMARY KEY DEFAULT 1 CHECK(singleton_id = 1),
    map_id TEXT NOT NULL REFERENCES maps(map_id),
    active_revision INTEGER NOT NULL,
    activated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activated_by TEXT DEFAULT 'system',
    FOREIGN KEY(map_id, active_revision) REFERENCES map_revisions(map_id, revision_number)
);

CREATE TABLE IF NOT EXISTS map_audit_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL CHECK(event_type IN (
        'CREATE_MAP', 'UPDATE_MAP', 'ADD_FEATURE', 'EDIT_FEATURE', 'DELETE_FEATURE',
        'COMPILE_REVISION', 'ACTIVATE_REVISION', 'ROLLBACK_REVISION'
    )),
    map_id TEXT,
    revision_number INTEGER,
    actor TEXT DEFAULT 'operator',
    details_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_features_map_kind ON map_features(map_id, kind) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_revisions_map ON map_revisions(map_id, revision_number);
"""


class OpenT2Database(object):
    def __init__(self, db_path):
        self.db_path = os.path.abspath(db_path)
        db_dir = os.path.dirname(self.db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            conn.executescript(SCHEMA_SQL)
            cur = conn.cursor()
            cur.execute("SELECT MAX(version) FROM schema_migrations")
            row = cur.fetchone()
            curr_ver = row[0] if (row and row[0] is not None) else 0

            if curr_ver < 1:
                cur.execute(
                    "INSERT INTO schema_migrations (version, description) VALUES (1, ?)",
                    ("Initial OpenT2 schema with revisions and audit log",)
                )
                curr_ver = 1

            if curr_ver < 2:
                # Migration 2: Add origin_point and destination_point to map_features check constraint
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS map_features_v2 (
                        feature_id TEXT PRIMARY KEY,
                        map_id TEXT NOT NULL REFERENCES maps(map_id) ON DELETE CASCADE,
                        kind TEXT NOT NULL CHECK(kind IN (
                            'keepout',
                            'free_space_override',
                            'speed_limit',
                            'waypoint',
                            'charging_dock',
                            'origin_point',
                            'destination_point'
                        )),
                        name TEXT NOT NULL,
                        geometry_json TEXT NOT NULL,
                        properties_json TEXT,
                        is_enabled INTEGER DEFAULT 1 CHECK(is_enabled IN (0, 1)),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        deleted_at TIMESTAMP DEFAULT NULL
                    );
                """)
                cur.execute("INSERT INTO map_features_v2 SELECT * FROM map_features;")
                cur.execute("DROP TABLE map_features;")
                cur.execute("ALTER TABLE map_features_v2 RENAME TO map_features;")
                cur.execute("CREATE INDEX IF NOT EXISTS idx_features_map_kind ON map_features(map_id, kind) WHERE deleted_at IS NULL;")
                cur.execute(
                    "INSERT INTO schema_migrations (version, description) VALUES (2, ?)",
                    ("Add origin_point and destination_point layer support",)
                )
            conn.commit()

    # --- MAPS ---

    def create_or_update_map(self, map_id, name, floor_level, resolution, width, height,
                             origin_x, origin_y, origin_yaw,
                             base_pbstream_rel, base_yaml_rel, base_pgm_rel, base_sha256):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT map_id FROM maps WHERE map_id = ?", (map_id,))
            exists = cur.fetchone() is not None
            if exists:
                cur.execute("""
                    UPDATE maps SET
                        name = ?, floor_level = ?, resolution = ?, width = ?, height = ?,
                        origin_x = ?, origin_y = ?, origin_yaw = ?,
                        base_pbstream_relpath = ?, base_yaml_relpath = ?, base_pgm_relpath = ?,
                        base_sha256 = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE map_id = ?
                """, (name, floor_level, resolution, width, height,
                      origin_x, origin_y, origin_yaw,
                      base_pbstream_rel, base_yaml_rel, base_pgm_rel, base_sha256, map_id))
                event = "UPDATE_MAP"
            else:
                cur.execute("""
                    INSERT INTO maps (
                        map_id, name, floor_level, resolution, width, height,
                        origin_x, origin_y, origin_yaw,
                        base_pbstream_relpath, base_yaml_relpath, base_pgm_relpath, base_sha256
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (map_id, name, floor_level, resolution, width, height,
                      origin_x, origin_y, origin_yaw,
                      base_pbstream_rel, base_yaml_rel, base_pgm_rel, base_sha256))
                event = "CREATE_MAP"
            self.log_audit(conn, event, map_id=map_id, details={"name": name, "res": resolution})
            conn.commit()

    def get_map(self, map_id):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM maps WHERE map_id = ?", (map_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def list_maps(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM maps ORDER BY created_at DESC")
            return [dict(r) for r in cur.fetchall()]

    # --- FEATURES ---

    def add_feature(self, feature_id, map_id, kind, name, geometry, properties=None, is_enabled=1):
        geom_json = json.dumps(geometry) if not isinstance(geometry, str) else geometry
        props_json = json.dumps(properties) if properties and not isinstance(properties, str) else (properties or "{}")
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO map_features (
                    feature_id, map_id, kind, name, geometry_json, properties_json, is_enabled
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (feature_id, map_id, kind, name, geom_json, props_json, 1 if is_enabled else 0))
            self.log_audit(conn, "ADD_FEATURE", map_id=map_id, details={"feature_id": feature_id, "kind": kind, "name": name})
            conn.commit()

    def update_feature(self, feature_id, name=None, geometry=None, properties=None, is_enabled=None):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM map_features WHERE feature_id = ?", (feature_id,))
            row = cur.fetchone()
            if not row:
                raise ValueError("Feature not found: " + str(feature_id))
            
            new_name = name if name is not None else row["name"]
            new_geom = json.dumps(geometry) if (geometry is not None and not isinstance(geometry, str)) else (geometry or row["geometry_json"])
            new_props = json.dumps(properties) if (properties is not None and not isinstance(properties, str)) else (properties if properties is not None else row["properties_json"])
            new_enabled = (1 if is_enabled else 0) if is_enabled is not None else row["is_enabled"]

            cur.execute("""
                UPDATE map_features SET
                    name = ?, geometry_json = ?, properties_json = ?, is_enabled = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE feature_id = ?
            """, (new_name, new_geom, new_props, new_enabled, feature_id))
            self.log_audit(conn, "EDIT_FEATURE", map_id=row["map_id"], details={"feature_id": feature_id, "name": new_name})
            conn.commit()

    def delete_feature(self, feature_id, soft_delete=True):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT map_id, name, kind FROM map_features WHERE feature_id = ?", (feature_id,))
            row = cur.fetchone()
            if not row:
                return False
            if soft_delete:
                cur.execute("UPDATE map_features SET deleted_at = CURRENT_TIMESTAMP WHERE feature_id = ?", (feature_id,))
            else:
                cur.execute("DELETE FROM map_features WHERE feature_id = ?", (feature_id,))
            self.log_audit(conn, "DELETE_FEATURE", map_id=row["map_id"], details={"feature_id": feature_id, "soft": soft_delete})
            conn.commit()
            return True

    def get_features(self, map_id, include_deleted=False, kind=None):
        with self.get_connection() as conn:
            cur = conn.cursor()
            query = "SELECT * FROM map_features WHERE map_id = ?"
            params = [map_id]
            if not include_deleted:
                query += " AND deleted_at IS NULL"
            if kind:
                query += " AND kind = ?"
                params.append(kind)
            query += " ORDER BY created_at ASC"
            cur.execute(query, params)
            res = []
            for r in cur.fetchall():
                d = dict(r)
                try:
                    d["geometry"] = json.loads(d["geometry_json"])
                except Exception:
                    d["geometry"] = d["geometry_json"]
                try:
                    d["properties"] = json.loads(d["properties_json"]) if d["properties_json"] else {}
                except Exception:
                    d["properties"] = {}
                res.append(d)
            return res

    # --- CONVENIENCE LAYER HELPERS ---

    def add_origin_point(self, map_id, name, x, y, yaw=0.0, is_default_home=True, properties=None):
        """
        Adds or updates an origin / home reference point for initialpose and docking reset.
        """
        import uuid
        fid = "origin_" + str(uuid.uuid4())[:8]
        props = properties.copy() if properties else {}
        props["yaw"] = float(yaw)
        props["is_default_home"] = bool(is_default_home)
        self.add_feature(fid, map_id, "origin_point", name, [float(x), float(y)], props)
        return fid

    def add_destination_point(self, map_id, name, x, y, yaw=0.0, table_number=None, properties=None):
        """
        Adds a navigation destination target (table, delivery stop, room).
        """
        import uuid
        fid = "dest_" + str(uuid.uuid4())[:8]
        props = properties.copy() if properties else {}
        props["yaw"] = float(yaw)
        if table_number is not None:
            props["table_number"] = str(table_number)
        self.add_feature(fid, map_id, "destination_point", name, [float(x), float(y)], props)
        return fid

    def add_charging_station(self, map_id, name, x, y, yaw=0.0, pre_dock_distance=0.8, properties=None):
        """
        Adds a dedicated charging dock pose and its pre-dock approach pose.
        """
        import uuid
        import math
        fid = "dock_" + str(uuid.uuid4())[:8]
        props = properties.copy() if properties else {}
        props["yaw"] = float(yaw)
        # Pre-dock approach point calculated backwards along docking yaw
        props["pre_dock_x"] = float(x) - pre_dock_distance * math.cos(yaw)
        props["pre_dock_y"] = float(y) - pre_dock_distance * math.sin(yaw)
        props["pre_dock_yaw"] = float(yaw)
        props["dock_type"] = props.get("dock_type", "auto_contact")
        self.add_feature(fid, map_id, "charging_dock", name, [float(x), float(y)], props)
        return fid

    def get_origin_points(self, map_id):
        return self.get_features(map_id, kind="origin_point")

    def get_destination_points(self, map_id):
        return self.get_features(map_id, kind="destination_point")

    def get_charging_stations(self, map_id):
        return self.get_features(map_id, kind="charging_dock")

    # --- REVISIONS ---

    def get_latest_revision_number(self, map_id):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT MAX(revision_number) FROM map_revisions WHERE map_id = ?", (map_id,))
            row = cur.fetchone()
            return row[0] if (row and row[0] is not None) else 0

    def publish_revision(self, map_id, revision_number, bundle_relpath, bundle_sha256,
                         features_snapshot, map_yaml_rel, map_pgm_rel,
                         map_amcl_yaml_rel, map_amcl_pgm_rel, thumbnail_rel=None,
                         published_by="operator", notes=""):
        snapshot_json = json.dumps(features_snapshot) if not isinstance(features_snapshot, str) else features_snapshot
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO map_revisions (
                    map_id, revision_number, bundle_relpath, bundle_sha256,
                    features_snapshot_json, map_yaml_relpath, map_pgm_relpath,
                    map_amcl_yaml_relpath, map_amcl_pgm_relpath, thumbnail_relpath,
                    published_by, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (map_id, revision_number, bundle_relpath, bundle_sha256,
                  snapshot_json, map_yaml_rel, map_pgm_rel,
                  map_amcl_yaml_rel, map_amcl_pgm_rel, thumbnail_rel,
                  published_by, notes))
            self.log_audit(conn, "COMPILE_REVISION", map_id=map_id, revision_number=revision_number,
                           details={"bundle_sha256": bundle_sha256, "by": published_by})
            conn.commit()

    def get_revisions(self, map_id):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM map_revisions WHERE map_id = ? ORDER BY revision_number DESC", (map_id,))
            return [dict(r) for r in cur.fetchall()]

    def get_revision(self, map_id, revision_number):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM map_revisions WHERE map_id = ? AND revision_number = ?", (map_id, revision_number))
            row = cur.fetchone()
            return dict(row) if row else None

    # --- ACTIVE STATE & ACTIVATION ---

    def set_active_map(self, map_id, revision_number, activated_by="system"):
        with self.get_connection() as conn:
            cur = conn.cursor()
            # Verify revision exists
            cur.execute("SELECT revision_id FROM map_revisions WHERE map_id = ? AND revision_number = ?",
                        (map_id, revision_number))
            if not cur.fetchone():
                raise ValueError("Cannot activate non-existent revision: map={}, rev={}".format(map_id, revision_number))

            cur.execute("""
                INSERT OR REPLACE INTO active_map_state (singleton_id, map_id, active_revision, activated_at, activated_by)
                VALUES (1, ?, ?, CURRENT_TIMESTAMP, ?)
            """, (map_id, revision_number, activated_by))
            self.log_audit(conn, "ACTIVATE_REVISION", map_id=map_id, revision_number=revision_number,
                           details={"by": activated_by})
            conn.commit()

    def get_active_map(self):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT a.map_id, a.active_revision, a.activated_at, a.activated_by,
                       m.name, m.resolution, m.width, m.height, m.origin_x, m.origin_y, m.origin_yaw,
                       r.bundle_relpath, r.bundle_sha256, r.map_yaml_relpath, r.map_pgm_relpath,
                       r.map_amcl_yaml_relpath, r.map_amcl_pgm_relpath
                FROM active_map_state a
                JOIN maps m ON a.map_id = m.map_id
                JOIN map_revisions r ON a.map_id = r.map_id AND a.active_revision = r.revision_number
                WHERE a.singleton_id = 1
            """)
            row = cur.fetchone()
            return dict(row) if row else None

    # --- AUDIT LOG ---

    def log_audit(self, conn, event_type, map_id=None, revision_number=None, actor="system", details=None):
        details_str = json.dumps(details) if details and not isinstance(details, str) else (details or "{}")
        conn.execute("""
            INSERT INTO map_audit_log (event_type, map_id, revision_number, actor, details_json)
            VALUES (?, ?, ?, ?, ?)
        """, (event_type, map_id, revision_number, actor, details_str))

    def get_audit_logs(self, limit=50):
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM map_audit_log ORDER BY created_at DESC LIMIT ?", (limit,))
            return [dict(r) for r in cur.fetchall()]
