<!-- ============================================================  -->
<!--  ShadowDrop - Security Edition                           -->
<!--  Developer : ATHEX BLACK HAT                                  -->
<!--  Version   : 1.0.0                                            -->
<!-- ============================================================  -->

<div align="center">

```
███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗      ██████╗ ██████╗  ██████╗ ██████╗ 
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║      ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║█████╗██║  ██║██████╔╝██║   ██║██████╔╝
╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║╚════╝██║  ██║██╔══██╗██║   ██║██╔═══╝ 
███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝      ██████╔╝██║  ██║╚██████╔╝██║     
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝       ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     
                                                                                                                  
```

### **ShadowDrop**
**Security Edition** · `v1.0.0`

*Generate customized, standalone `.exe` droppers for authorized CTF lab environments.*

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-green.svg)]()
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)]()
[![License](https://img.shields.io/badge/license-MIT-orange.svg)]()
[![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)]()

</div>

---

## ⚠️ DISCLAIMER

> **READ BEFORE USE**
>
> Ye tool **sirf authorized CTF lab environments**, **penetration testing engagements**, aur **security research** ke liye hai.
>
> **Strictly prohibited:**
> - ❌ Unauthorized systems pe use
> - ❌ Criminal activity
> - ❌ Real-world attacks without written permission
> - ❌ Malicious distribution
>
> **User ki zimmedari:**
> - ✅ Proper authorization lena
> - ✅ Local laws follow karna
> - ✅ Ethical use karna
>
> Developer (ATHEX BLACK HAT) kisi bhi misuse ka zimmedar **nahi** hai. Agar aap authorized nahi hain, toh ye tool **use na karein**.

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [How It Works](#-how-it-works)
- [Examples](#-examples)
- [Troubleshooting](#-troubleshooting)
- [Security Considerations](#-security-considerations)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)
- [Credits](#-credits)

---

## 🎯 Overview

**ShadowDrop** ek interactive tool hai jo aapko **customized standalone `.exe` droppers** generate karne deta hai — CTF labs, red team exercises, aur malware analysis training ke liye.

### What It Does

1. Aap se parameters lete hain (payload URL, filename, folder, etc.)
2. Ek Python source generate karta hai based on aapke original dropper logic
3. **PyInstaller** se automatically `.exe` compile karta hai
4. Standalone binary output deta hai — target machine pe kuch install nahi chahiye

### Why Use It?

| Manual Approach | ShadowDrop |
|---|---|
| Har baar code edit karna | Interactive prompts |
| PyInstaller command yaad rakhna | Automatically handle |
| Config mistakes | Validation + review |
| Repetitive work | 30 seconds mein ready |
| No tracking | Build logs + config files |

---

## ✨ Features

### 🎯 Core Features
- ✅ **Interactive CLI** — Guided prompts, no manual editing
- ✅ **Standalone `.exe` output** — `--onefile` PyInstaller
- ✅ **Hidden execution** — No console window (`--noconsole`)
- ✅ **Config files** — JSON-based, non-interactive builds
- ✅ **CLI overrides** — `--url`, `--name` flags
- ✅ **Build logs** — Har build ka record

### 🛡️ Dropper Capabilities
- ✅ **Auto-elevation** — UAC prompt via `ShellExecuteW`
- ✅ **Defender exclusion** — `Add-MpPreference` (lab only)
- ✅ **Hidden process launch** — `CREATE_NO_WINDOW` + `SW_HIDE`
- ✅ **Fallback download** — TEMP folder agar direct fail ho
- ✅ **Self-delete** — Cleanup batch file
- ✅ **Random delays** — Basic sandbox evasion

### 🎨 Customization
- ✅ **Custom icon** — `.ico` file support
- ✅ **Version info spoofing** — Microsoft/Chrome/Defender metadata
- ✅ **UPX compression** — Smaller EXE size
- ✅ **Custom execution folder** — `%ProgramData%`, `%TEMP%`, etc.

### 🏗️ Developer-Friendly
- ✅ **Modular architecture** — `core/` package
- ✅ **ANSI colors** — Pretty terminal output
- ✅ **Auto-cleanup** — Temp files removed
- ✅ **Cross-platform builder** — Windows/Linux/macOS
- ✅ **Error handling** — Graceful failures

---

### Builder Machine

| Requirement | Minimum | Recommended |
|---|---|---|
| **OS** | Windows 10 / Ubuntu 20.04 / macOS 11 | Any modern OS |
| **Python** | 3.8+ | 3.10+ |
| **pip** | 20.0+ | Latest |
| **Disk** | 500 MB free | 1 GB free |
| **RAM** | 2 GB | 4 GB |
| **Internet** | Required (for PyInstaller download) | — |

### Target Machine

| Requirement | Details |
|---|---|
| **OS** | Windows 7+ (64-bit recommended) |
| **Python** | ❌ Not needed — EXE standalone |
| **Dependencies** | ❌ None — self-contained |
| **Privileges** | Admin (UAC elevation) |

### Payload Server

Koi bhi HTTP server chalega:
- Python: `python -m http.server 8080`
- Node: `npx http-server -p 8080`
- PHP: `php -S 0.0.0.0:8080`
- Nginx / Apache

---

## 🚀 Installation

### Step 1: Clone / Download

```bash
git clone https://github.com/Athexblackhat2/ShadowDrop.git
cd ShadowDrop
```


### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Test Run

```bash
python builder.py --help
```

### Quick Install (One-liner)

```bash
git clone https://github.com/Athexblackhat2/ShadowDrop.git && \
cd ShadowDrop && \
python -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
python builder.py
```

---

## 🎮 Usage

### Mode 1: Interactive (Recommended for First Time)

```bash
python builder.py
```

Follow prompts. Har field ke liye guidance milegi.

### Mode 2: Config File (For Repeat Builds)

```bash
# Edit
nano configs/builder.json

# Build
python builder.py --config configs/builder.json
```

### Mode 3: CLI Overrides

```bash
python builder.py -c configs/builder.json \
    --url http://10.0.0.5:8080/payload.exe \
    --name lab02_dropper
```

### Mode 4: Quiet Mode (CI / Automation)

```bash
python builder.py -c configs/builder.json --quiet
```

Skips authorization prompt + confirmation — automation ke liye.

### CLI Arguments

| Argument | Short | Description |
|---|---|---|
| `--config` | `-c` | Path to JSON config file |
| `--url` | `-u` | Override payload URL |
| `--name` | `-n` | Override output filename |
| `--quiet` | `-q` | Skip confirmation prompts |
| `--help` | `-h` | Show help |

---


### Field Reference

| Field | Type | Required | Description |
|---|---|---|---|
| `EXE_URL` | string | ✅ | Payload download URL |
| `FINAL_NAME` | string | ✅ | Filename on target |
| `EXEC_FOLDER` | string | ✅ | Target folder (env vars allowed) |
| `OUTPUT_NAME` | string | ✅ | Output `.exe` name (no extension) |
| `ICON` | string | ❌ | Path to `.ico` file |
| `UPX` | bool | ❌ | Compress with UPX |
| `VERSION_FILE` | string | ❌ | Version info template |

### Environment Variables in Paths

Windows env vars supported:

| Variable | Expands To |
|---|---|
| `%ProgramData%` | `C:\ProgramData` |
| `%TEMP%` | `C:\Users\<user>\AppData\Local\Temp` |
| `%APPDATA%` | `C:\Users\<user>\AppData\Roaming` |
| `%USERPROFILE%` | `C:\Users\<user>` |
| `%WINDIR%` | `C:\Windows` |
| `%SYSTEMROOT%` | `C:\Windows` |

---

### Module Responsibilities

| Module | Responsibility |
|---|---|
| **`ui.py`** | Banner, ANSI colors, print helpers, panels |
| **`utils.py`** | Input helpers, FS, validation, logging |
| **`config.py`** | Config collection, loading, review |
| **`generator.py`** | Template loading, placeholder injection |
| **`compiler.py`** | PyInstaller invocation, output verification |

### Benefits of Modular Design

- ✅ **Testable** — Har module independently test ho sakta hai
- ✅ **Reusable** — `ui.py` doosre tools mein bhi use kar sakte hain
- ✅ **Maintainable** — Ek feature change = ek file edit
- ✅ **Scalable** — Naya feature add karna easy

---

### Runtime (On Target)

EXE run hone par:

1. **Admin check** — `IsUserAnAdmin()` call
2. **Elevate if needed** — `ShellExecuteW` with `runas`
3. **Add Defender exclusion** — `Add-MpPreference`
4. **Download payload** — `urllib.request` with fake UA
5. **Save to target folder** — `%ProgramData%\Microsoft\Windows\Caches`
6. **Random delay** — 0.5-2s
7. **Launch hidden** — `CREATE_NO_WINDOW` + `SW_HIDE`
8. **Self-delete** — Cleanup batch file

---


## 🔒 Security Considerations

### For Builders

1. **Isolate build environment** — VM use karein
2. **Don't commit real configs** — `.gitignore` already handles
3. **Rotate lab IPs** — After each exercise
4. **Audit build logs** — `logs/` folder check karein
5. **Encrypt sensitive configs** — `gpg` ya `age` use karein

### For Target Systems

1. **Always get authorization** — Written permission
2. **Lab network only** — No production access
3. **Snapshot before test** — VM rollback ke liye
4. **Monitor network** — IDS/IPS logs review karein
5. **Clean up after** — Persistence remove karein

### Detection Vectors (Blue Team Reference)

| Indicator | Detection Method |
|---|---|
| `Add-MpPreference -ExclusionPath` | PowerShell ScriptBlock logging (EID 4104) |
| `%ProgramData%\...\*.exe` | Sysmon EID 11 (file create) |
| `CREATE_NO_WINDOW` | Sysmon EID 1 (process create) |
| HTTP download from raw IP | Network logs / proxy |
| Self-delete batch file | Sysmon EID 1 + 23 |
| PyInstaller binary | Static analysis (PE header, strings) |

**Sysmon config** (recommended events):
- EID 1: Process Create
- EID 3: Network Connect
- EID 11: File Create
- EID 22: DNS Query
- EID 23: File Delete

---

## ❓ FAQ

**Q: Target machine pe Python install karna hoga?**
A: Nahi. EXE standalone hoti hai — PyInstaller sab bundle kar deta hai.

**Q: Kya ye Defender se bypass karega?**
A: Paylaod ko exclusion mai add karta hai.Lekin Sirf authorized labs ke liye use karay.

**Q: Multiple payloads ek saath generate kar sakte hain?**
A: Haan — script loop likh kar (`for cfg in configs/*.json`).

**Q: Payload host kaise setup karun?**
A: `python -m http.server 8080` kafi hai. Folder mein payload rakhein.

**Q: Kya ye Linux ke liye bhi EXE banata hai?**
A: Nahi — PyInstaller cross-compile nahi karta. Windows target ke liye Windows/Linux/macOS builder se build ho sakti hai, par output sirf Windows ke liye.

**Q: UPX safe hai?**
A: Haan, par kabhi kabhi AV false positives badh jate hain. Lab mein test karein.

**Q: Build ke baad source delete ho jata hai?**
A: Haan — temp folder auto-cleanup. Sirf EXE `output/` mein rehti hai.

**Q: Config file mein password/API key rakh sakte hain?**
A: Nahi — configs plain JSON hain. Encryption ke liye `age` ya `gpg` use karein.

---

### Guidelines

- ✅ Follow PEP 8
- ✅ Add docstrings
- ✅ Test changes
- ✅ Update README if needed
- ❌ No offensive enhancements
- ❌ No real-world malware samples


## 👏 Credits

### Developer
- **ATHEX BLACK HAT** — Project author & maintainer

### Built With
- [Python](https://python.org) — Core language
- [PyInstaller](https://pyinstaller.org) — EXE compilation
- [colorama](https://pypi.org/project/colorama/) — Windows ANSI colors

---

## ⭐ Star History

Agar ye project useful laga, toh GitHub pe **star** zaroor karein!

---

<div align="center">

**⚠️ USE RESPONSIBLY — AUTHORIZED LABS ONLY ⚠️**

Made with 🔴 by **ATHEX BLACK HAT**

</div>