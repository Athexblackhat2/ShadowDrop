#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compiler module - PyInstaller wrapper.
"""

import os
import sys
import subprocess

from .ui import info, success, error, warn, dim
from .utils import ensure_dir, file_size_kb


# ============================================================
# PYINSTALLER DETECTION
# ============================================================
def check_pyinstaller():
    """Return PyInstaller version or None."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except Exception:
        return None


# ============================================================
# COMMAND BUILDER
# ============================================================
def build_command(py_path, config, temp_dir, output_dir):
    """Construct PyInstaller command list."""
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--name", config["OUTPUT_NAME"],
        "--distpath", output_dir,
        "--workpath", os.path.join(temp_dir, "build"),
        "--specpath", temp_dir,
        "--clean",
        "--noconfirm",
    ]

    # Icon
    icon = config.get("ICON")
    if icon:
        icon_abs = os.path.abspath(icon)
        if os.path.exists(icon_abs):
            cmd.extend(["--icon", icon_abs])
        else:
            warn(f"Icon not found, skipping: {icon}")

    # UPX compression
    if config.get("UPX"):
        cmd.extend(["--upx-dir", temp_dir])

    cmd.append(py_path)
    return cmd


# ============================================================
# BUILD
# ============================================================
def build_exe(py_path, config, temp_dir, output_dir="output", timeout=600):
    """Compile .py to .exe via PyInstaller."""
    output_dir = os.path.abspath(output_dir)
    ensure_dir(output_dir)

    cmd = build_command(py_path, config, temp_dir, output_dir)

    dim(f"$ {' '.join(cmd)}")
    print()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        error(f"PyInstaller timed out ({timeout}s).")
        return None
    except Exception as e:
        error(f"PyInstaller invocation failed: {e}")
        return None

    if result.returncode != 0:
        error("PyInstaller failed!")
        stderr_tail = (result.stderr or "")[-2000:]
        if stderr_tail:
            dim(stderr_tail)
        return None

    exe_path = os.path.join(output_dir, f"{config['OUTPUT_NAME']}.exe")
    if os.path.exists(exe_path):
        return exe_path

    error(f"Expected output not found: {exe_path}")
    return None


def print_build_result(exe_path, config):
    """Print success panel."""
    from .ui import success_banner, footer
    success_banner()

    size_kb = file_size_kb(exe_path)
    print(f"  {C.DIM}├─{C.RESET} {C.BOLD}Output   :{C.RESET} {C.GREEN}{exe_path}{C.RESET}")
    print(f"  {C.DIM}├─{C.RESET} {C.BOLD}Size     :{C.RESET} {C.GREEN}{size_kb:.2f} KB{C.RESET}")
    print(f"  {C.DIM}├─{C.RESET} {C.BOLD}Target   :{C.RESET} {C.CYAN}{config['EXE_URL']}{C.RESET}")
    print(f"  {C.DIM}├─{C.RESET} {C.BOLD}Folder   :{C.RESET} {C.CYAN}{config['EXEC_FOLDER']}{C.RESET}")
    print(f"  {C.DIM}└─{C.RESET} {C.BOLD}Name     :{C.RESET} {C.CYAN}{config['FINAL_NAME']}{C.RESET}")
    print()
    print(f"  {C.YELLOW}🚀 Ready to deploy in CTF lab.{C.RESET}")
    footer()


# Imported here to avoid circular import at top
from .ui import C