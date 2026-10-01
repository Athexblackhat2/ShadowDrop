#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI module - banner, colors, print helpers.
"""

import os
import sys
from datetime import datetime


# ============================================================
# VERSION / BRANDING
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


# ============================================================
# BANNER
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


# ============================================================
# HELPERS
# ============================================================
def enable_ansi_windows():
    """Enable ANSI colors on Windows CMD."""
    if os.name == 'nt':
        try:
            os.system('')
        except Exception:
            pass


def clear_screen():
    """Clear terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_banner():
    """Print styled banner."""
    clear_screen()
    print(C.CYAN + C.BOLD + BANNER + C.RESET)
    print(C.MAGENTA + SUBTITLE + C.RESET)
    print(f"  {C.DIM}Developer :{C.RESET} {C.GREEN}{C.BOLD}{DEVELOPER}{C.RESET}")
    print(f"  {C.DIM}Version   :{C.RESET} {C.GREEN}{VERSION}{C.RESET}")
    print(f"  {C.DIM}Project   :{C.RESET} {C.GREEN}{PROJECT}{C.RESET}")
    print(f"  {C.DIM}Timestamp :{C.RESET} {C.GREEN}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{C.RESET}")
    print()


# ============================================================
# STATUS PRINTERS
# ============================================================
def info(msg):
    print(f"{C.CYAN}[*]{C.RESET} {msg}")


def success(msg):
    print(f"{C.GREEN}[+]{C.RESET} {msg}")


def warn(msg):
    print(f"{C.YELLOW}[!]{C.RESET} {msg}")


def error(msg):
    print(f"{C.RED}[-]{C.RESET} {msg}")


def step(num, total, msg):
    print(f"{C.BLUE}[{num}/{total}]{C.RESET} {C.BOLD}{msg}{C.RESET}")


def dim(msg):
    print(f"{C.DIM}{msg}{C.RESET}")


def blank():
    print()


# ============================================================
# BOXES / PANELS
# ============================================================
def box_header(title):
    """Print a section header."""
    print(f"{C.YELLOW}{C.BOLD}[*] {title}{C.RESET}")
    print(f"{C.DIM}{'-' * 55}{C.RESET}")


def box_panel(title, rows):
    """Print a bordered panel with key-value rows."""
    print()
    print(f"{C.MAGENTA}{C.BOLD}┌{'─' * 57}┐{C.RESET}")
    padded = f"  {title}"
    print(f"{C.MAGENTA}{C.BOLD}│{C.RESET}{C.BOLD}{padded:<57}{C.RESET}"
          f"{C.MAGENTA}{C.BOLD}│{C.RESET}")
    print(f"{C.MAGENTA}{C.BOLD}├{'─' * 57}┤{C.RESET}")

    for label, value in rows:
        val_str = str(value)
        if len(val_str) > 38:
            val_str = "..." + val_str[-35:]
        print(f"{C.MAGENTA}{C.BOLD}│{C.RESET}  {C.DIM}{label:<14}{C.RESET} "
              f"{C.GREEN}{val_str:<40}{C.RESET}{C.MAGENTA}{C.BOLD}│{C.RESET}")

    print(f"{C.MAGENTA}{C.BOLD}└{'─' * 57}┘{C.RESET}")
    print()


def success_banner():
    """Print success banner."""
    print(f"{C.BG_GREEN}{C.WHITE}{C.BOLD}  ✅  BUILD SUCCESSFUL  {C.RESET}")
    print()


def auth_warning():
    """Print authorization warning."""
    print(f"{C.BG_RED}{C.WHITE}{C.BOLD}  ⚠  AUTHORIZATION REQUIRED  {C.RESET}")
    print(f"{C.YELLOW}This tool is for authorized CTF labs only.{C.RESET}")
    print()


def footer():
    """Print footer."""
    print(f"  {C.DIM}Developer: {DEVELOPER}  ·  {PROJECT} v{VERSION}{C.RESET}")
    print()