<div align="center">

# ⚡ Laptop Battery Charge Voice Alert

### *Intelligent, Headless Battery Health Assistant with Natural AI Voice Synthesis & Desktop Toast Alerts*

[![GitHub Stars](https://img.shields.io/github/stars/tuhinfay/Laptop-Battery-Charge-Voice-Alert?style=for-the-badge&color=ffd700)](https://github.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/tuhinfay/Laptop-Battery-Charge-Voice-Alert?style=for-the-badge&color=60a5fa)](https://github.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/network/members)
[![License: MIT](https://img.shields.io/badge/License-MIT-34d399.svg?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078d4?style=for-the-badge&logo=windows)](https://www.microsoft.com/windows)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)

<p align="center">
  <b>Protect your laptop's battery life without checking taskbars or remembering timers.</b><br>
  Runs 100% headless in the background, preserves battery cycle count, and talks to you using ultra-realistic AI voice models (British English, Bengali, or custom TTS engines).
</p>

[Quick Install](#-one-line-quick-installation) • [Command Explanations](#-how-the-commands-work) • [Features](#-core-features) • [Thresholds](#-battery-monitoring-logic) • [Uninstall](#-stop-or-uninstall)

---

</div>

## 🌟 Why Do You Need This?

Most operating systems only pop up an alert when your laptop is at 10% or about to turn off. Modern lithium-ion laptop batteries degrade fastest when held at 100% for long durations or drained below 20%.

**Laptop Battery Charge Voice Alert** automates your battery health:
- 🔊 **Voice Alerts Across The Room:** Clear voice reminders tell you when to plug in or unplug your charger without looking at your screen.
- ⚡ **Zero-Touch Setup:** One command sets up everything: checks for Python, installs required packages, fetches files from this repository, adds startup triggers, and launches silently.
- 🍃 **Ultra-Lightweight Resource Usage:** Consumes nearly 0% CPU and only ~15–20 MB RAM using native Windows Win32 audio drivers.

---

## 🚀 One-Line Quick Installation

Open **PowerShell** (Press <kbd>Win</kbd> + <kbd>X</kbd> and choose **Terminal** or **PowerShell**), copy your preferred command below, paste it, and press <kbd>Enter</kbd>:

### 🇬🇧 Option 1: British English (Default: Sonia - Soft & Natural)
> *Best for everyday work. Speaks in natural British English voice.*

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/main/install.ps1))) -Lang "en" -Voice "en-GB-SoniaNeural"
```

### 🇧🇩 Option 2: Bengali / বাংলা (Nabanita - মিষ্টি ও স্পষ্ট বাংলা ভয়েস)
> *বাংলায় মিষ্টি ও স্পষ্ট ভয়েসে ব্যাটারি চার্জ ও আনপ্লাগ করার সতর্কতা দেবে।*

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/main/install.ps1))) -Lang "bn" -Voice "bn-BD-NabanitaNeural"
```

### 🌐 Option 3: Interactive Setup (Choose On Screen)
> *Prompts you on the terminal with a simple menu (1 for English, 2 for Bengali, 3 for Custom Voice).*

```powershell
irm https://raw.githubusercontent.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/main/install.ps1 | iex
```

### 🎨 Option 4: Custom Neural Voice (Any Language)
> *Replace with any Edge TTS voice model (e.g., American Ava, Spanish, Hindi, French, Japanese).*

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/main/install.ps1))) -Lang "en" -Voice "en-US-AvaNeural"
```

---

## 🔍 How the Commands Work

Every command downloads the raw setup engine directly from this public repository and executes it in memory:

1. **`irm` (`Invoke-RestMethod`):** Securely fetches the latest `install.ps1` script from `https://raw.githubusercontent.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/main/install.ps1`.
2. **Auto-Python Check:** The script checks whether Python is present. If missing, it uses `winget` or the official installer to configure Python 3 silently without popups.
3. **Dependency Injection:** Installs `psutil` (battery polling), `edge-tts` (neural speech synthesis), and `pywin32` (Windows API adapter) silently.
4. **Local Installation:** Downloads `battery_guardian.pyw` and builds `config.json` inside `%LOCALAPPDATA%\LaptopBatteryVoiceAlert`.
5. **Autostart Registration:** Adds a hidden launcher (`BatteryGuardian.vbs`) to `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup` so the monitor runs automatically after every reboot or startup.
6. **Background Execution:** Starts `pythonw.exe` immediately without showing any command prompt window.

---

## ✨ Core Features

| Feature | Description |
| :--- | :--- |
| **Edge Neural AI Audio** | Clear, studio-grade neural voice output powered by Microsoft Edge TTS. |
| **Offline SAPI Fallback** | Automatically falls back to Windows SAPI TTS if there is no internet connection. |
| **Zero GUI Distraction** | Operates headless via `pythonw.exe` without cluttering the screen or taskbar. |
| **Adaptive Sleep Cycles** | Checks every **5 minutes** during safe zones (51%–79%) and scales to **1 minute** during action zones. |
| **Plug-and-Play Setup** | Does not require Git, manual folder setups, or manual environment path editing. |
| **Desktop Toast Alerts** | Displays native Windows balloon/toast notifications alongside the voice alert. |

---

## ⚙️ Battery Monitoring Logic

```
0% [=== CRITICAL === 20%] [== LOW == 30%] [== NOTICE == 50%] ---- [IDLE: 51%-79%] ---- [80% == CHARGED ==] [95% === UNPLUG === 100%]
```

| Battery Level | Charger State | Polling Check | Triggered Alert | Description |
| :---: | :---: | :---: | :--- | :--- |
| **≥ 95%** | Connected | 1 minute | **Unplug Charger!** | Urgent repeating voice reminder every minute to prevent overcharging. |
| **80% to 94%** | Connected | 1 minute | **Battery Charged** | Notification that the battery reached its healthy 80% mark (Once). |
| **51% to 79%** | Any | 5 minutes | **Standby Monitoring** | Resource-saving interval; checks quietly without notifications. |
| **≤ 50%** | On Battery | 1 minute | **Battery Notice** | Alerts that the battery is down to 50% (Once). |
| **≤ 30%** | On Battery | 1 minute | **Low Battery Warning** | Reminder that battery charge is running low (Once). |
| **≤ 20%** | On Battery | 1 minute | **Critical Battery Alert** | Persistent alarm every minute until the charger is plugged back in. |

---

## 🛠️ Manual Installation (Offline / Clone Method)

If you prefer to clone the repository manually:

1. Clone this repository:
   ```bash
   git clone https://github.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert.git
   cd Laptop-Battery-Charge-Voice-Alert
   ```

2. Install dependencies:
   ```bash
   pip install psutil edge-tts pywin32
   ```

3. Customize your settings in `config.json`:
   ```json
   {
     "language": "en",
     "voice": "en-GB-SoniaNeural",
     "check_normal": 300,
     "check_alert": 60
   }
   ```
   *(For Bengali, change `"language": "bn"` and `"voice": "bn-BD-NabanitaNeural"`)*

4. Run the background monitor:
   Double-click `battery_guardian.pyw` or run:
   ```bash
   pythonw battery_guardian.pyw
   ```

---

## 🛑 Stop or Uninstall

### Stop the Background Process
1. Press <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Esc</kbd> to open **Task Manager**.
2. Go to the **Details** tab.
3. Locate `pythonw.exe`, right-click it, and select **End task**.

### Complete Removal
To completely remove the autostart launcher, application folder, and configurations, run this single line in PowerShell:

```powershell
Stop-Process -Name "pythonw" -ErrorAction SilentlyContinue; Remove-Item "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\BatteryGuardian.vbs" -Force -ErrorAction SilentlyContinue; Remove-Item "$env:LOCALAPPDATA\LaptopBatteryVoiceAlert" -Recurse -Force -ErrorAction SilentlyContinue; Write-Host "Laptop Battery Charge Voice Alert uninstalled completely." -ForegroundColor Green
```

---

## 🤝 Contributing

Contributions are welcome!
1. Fork the Project.
2. Create your Feature Branch (`git checkout -b feature/NewFeature`).
3. Commit your Changes (`git commit -m 'Add NewFeature'`).
4. Push to the Branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

<div align="center">

Developed with ❤️ by [Tuhinfay](https://github.com/tuhinfay)

⭐ **If this project saves your laptop battery, please give it a Star on GitHub!** ⭐

</div>
