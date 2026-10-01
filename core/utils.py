#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utils module - filesystem, validation, logging helpers.
"""

import os
import sys
import shutil
import tempfile
from datetime import datetime

from .ui import C, info, warn, error, success


# ============================================================
# INPUT HELPERS
# ============================================================
def get_input(prompt, default=None, required=True):
    """Get user input with optional default."""
    if default:
        display = f"{C.CYAN}{prompt}{C.RESET} {C.DIM}[{default}]{C.RESET}: "
    else:
        display = f"{C.CYAN}{prompt}{C.RESET}: "

    try:
        value = input(display).strip()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{C.RED}[!] Cancelled by user.{C.RESET}")
        sys.exit(1)

    if not value:
        if default is not None:
            return default
        if required:
            error("This field is required.")
            return get_input(prompt, default, required)
    return value


def get_yes_no(prompt, default="n"):
    """Yes/No input."""
    display = f"{C.CYAN}{prompt}{C.RESET} {C.DIM}(y/n) [{default}]{C.RESET}: "
    try:
        value = input(display).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{C.RED}[!] Cancelled by user.{C.RESET}")
        sys.exit(1)
    if not value:
        value = default
    return value == 'y'


# ============================================================
# FILESYSTEM HELPERS
# ============================================================
def ensure_dir(path):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)
    return path


def make_temp_dir(prefix="dropper_build_"):
    """Create a temp working directory."""
    return tempfile.mkdtemp(prefix=prefix)


def cleanup_temp(temp_dir):
    """Safely remove temp build directory."""
    try:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception:
        pass


def file_size_kb(path):
    """Return file size in KB, or 0 if missing."""
    try:
        return os.path.getsize(path) / 1024
    except Exception:
        return 0


def safe_filename(name):
    """Sanitize a filename."""
    bad_chars = '<>:"/\\|?*'
    for ch in bad_chars:
        name = name.replace(ch, '_')
    return name.strip() or "output"


# ============================================================
# VALIDATION
# ============================================================
def validate_url(url):
    """Basic URL validation."""
    if not url:
        return False
    return url.startswith(("http://", "https://", "ftp://"))


def validate_config(config):
    """Validate config dict. Returns (ok, errors)."""
    errors = []

    if not config.get("EXE_URL"):
        errors.append("EXE_URL is empty")
    elif not validate_url(config["EXE_URL"]):
        errors.append("EXE_URL is not a valid URL")

    if not config.get("FINAL_NAME"):
        errors.append("FINAL_NAME is empty")

    if not config.get("OUTPUT_NAME"):
        errors.append("OUTPUT_NAME is empty")

    if config.get("ICON") and not os.path.exists(config["ICON"]):
        errors.append(f"Icon not found: {config['ICON']}")

    return (len(errors) == 0, errors)


# ============================================================
# LOGGING
# ============================================================
LOG_DIR = "logs"


def init_logs():
    """Ensure logs directory exists."""
    ensure_dir(LOG_DIR)


def log_build(config, exe_path, extra=None):
    """Write a build log entry."""
    init_logs()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"build_{ts}.log")

    try:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"Build Log — {datetime.now().isoformat()}\n")
            f.write("=" * 55 + "\n\n")
            f.write("[CONFIG]\n")
            for k, v in config.items():
                f.write(f"  {k} = {v}\n")
            f.write("\n[OUTPUT]\n")
            f.write(f"  exe = {exe_path}\n")
            f.write(f"  size_kb = {file_size_kb(exe_path):.2f}\n")

            if extra:
                f.write("\n[EXTRA]\n")
                for k, v in extra.items():
                    f.write(f"  {k} = {v}\n")

        return log_path
    except Exception:
        return None