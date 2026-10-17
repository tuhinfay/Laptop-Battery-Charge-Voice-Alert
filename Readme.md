# ⚡ Laptop Battery Charge Voice Alert

[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078D6?logo=windows)](https://github.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-brightgreen.svg)](https://github.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/graphs/commit-activity)

A smart, lightweight Windows background daemon that monitors your laptop's battery health and status. It alerts you with **natural neural voice announcements** (British English by default, Bengali, or any global neural voice) and **clean Windows desktop toast notifications** without running a visible console window.

---

## 🌟 Highlights

- **Natural Neural TTS Voice:** Powered by Microsoft Edge's Neural Text-to-Speech engine for clear, human-like voice notifications (no robotic sounds).
- **Offline Fallback:** Automatically switches to Windows SAPI Speech if you are disconnected from the internet.
- **Dynamic Battery Polling:**
  - **Safe Zone (51% – 79%):** Checks battery once every **5 minutes** to save system resources.
  - **Action Zones (≤ 50% discharging or ≥ 80% charging):** Automatically scales up monitoring to **1 minute** intervals.
- **Battery Health Preservation:**
  - Friendly reminders at **50%** and **80%**.
  - Moderate warning at **30%**.
  - Persistent, repetitive alarms at **20% (low)** and **95% (overcharge risk)** until resolved.
- **Ultra Low Footprint:** Consumes **~0% CPU** and only **~15–25 MB RAM**. Runs silently as a headless background task.
- **Automatic Dependency Resolver:** Required packages (`psutil`, `edge-tts`, `pywin32`) are installed on the fly if missing.

---

## 🚀 One-Line Automated Installation

Open **PowerShell** (Press `Win + X` and select **Windows PowerShell** or **Terminal**), paste any of the commands below, and hit **Enter**.

### 1. Default (Elegant British English - Sonia)
```powershell
irm https://raw.githubusercontent.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/main/install.ps1 | iex
```

### 2. Bengali / বাংলা (Natural Sweet Voice - Nabanita)
```powershell
$env:VOICE_LANG="bn"; irm https://raw.githubusercontent.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/main/install.ps1 | iex
```

### 3. Custom Language / Voice
You can choose any language code (`en`, `bn`, `es`, `fr`, `de`, `hi`, `ar`, etc.) and any Microsoft Neural Voice model. For example, for American English (Ava - Warm & Expressive):
```powershell
$env:VOICE_LANG="en"; $env:VOICE_MODEL="en-US-AvaNeural"; irm https://raw.githubusercontent.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/main/install.ps1 | iex
```

> **What the one-liner does automatically:**
> 1. Clones the engine and configs into `%LOCALAPPDATA%\LaptopBatteryVoiceAlert`.
> 2. Verifies Python and auto-installs missing libraries silently.
> 3. Creates a headless startup runner in your Windows Startup directory.
> 4. Starts the process immediately in the background — no PC reboot required.

---

## ⚙️ Battery Alert Matrix

| Battery Level | Charger Status | Polling Frequency | Alert Action |
| :--- | :--- | :--- | :--- |
| **80% – 94%** | Plugged In | Every 1 min | Voice + Toast: Informs you that battery reached 80% (Once). |
| **≥ 95%** | Plugged In | Every 1 min | Voice + Toast: **Persistent warning** every minute to unplug charger. |
| **51% – 79%** | Any | Every 5 min | Silent idle monitoring (Saves CPU cycles). |
| **≤ 50%** | On Battery | Every 1 min | Voice + Toast: 50% milestone notification (Once). |
| **≤ 30%** | On Battery | Every 1 min | Voice + Toast: Low battery warning to plug in soon (Once). |
| **≤ 20%** | On Battery | Every 1 min | Voice + Toast: **Critical alert** repeating every minute until connected. |

---

## 📦 Manual Setup (From Downloaded Zip / Git Clone)

If you prefer to download and run the script manually:

### Step 1: Clone or Download
```bash
git clone https://github.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert.git
cd Laptop-Battery-Charge-Voice-Alert
```

### Step 2: Install Python Dependencies
```bash
pip install psutil edge-tts pywin32
```
*(If dependencies are not installed manually, the script will attempt to install them on its first run.)*

### Step 3: Run the Script
- **To test in foreground (with terminal log):**
  ```bash
  python battery_guardian.py
  ```
- **To run silently in background:**
  Double-click `battery_guardian.pyw` (it uses `pythonw.exe` without opening a black command prompt window).

### Step 4: Make It Auto-Start with Windows
1. Press `Win + R`, type `shell:startup`, and press **Enter**.
2. Right-click inside the folder, select **New > Shortcut**.
3. Browse and select your `battery_guardian.pyw` file, then save.
4. It will now automatically launch every time your laptop powers on.

---

## 🛠️ Configuration & Customization

The script settings are managed via `config.json` inside the installation folder:

```json
{
  "language": "en",
  "voice": "en-GB-SoniaNeural",
  "check_normal": 300,
  "check_alert": 60,
  "thresholds": {
    "notice_50": 50,
    "warn_30": 30,
    "critical_20": 20,
    "charged_80": 80,
    "unplug_95": 95
  }
}
```

### Popular Neural Voice Options:
| Language / Accent | Voice Identifier | Description |
| :--- | :--- | :--- |
| **British English (Default)** | `en-GB-SoniaNeural` | Elegant, soft, and clear |
| **Bengali (Bangladesh)** | `bn-BD-NabanitaNeural` | Natural, professional, and sweet |
| **Bengali (Male)** | `bn-BD-PradeepNeural` | Clear, standard Bengali |
| **US English (Cute/Warm)** | `en-US-AvaNeural` | Expressive and friendly |
| **US English (Standard)** | `en-US-JennyNeural` | Natural conversation style |
| **Hindi** | `hi-IN-SwaraNeural` | Clear, standard Hindi voice |

---

## 🛑 How to Stop or Uninstall

### Stop the Background Process
1. Press `Ctrl + Shift + Esc` to open **Task Manager**.
2. Go to the **Details** tab.
3. Look for `pythonw.exe`, right-click on it, and click **End Task**.

### Complete Uninstallation
Run this command in PowerShell to remove the startup script, config files, and cached data cleanly:
```powershell
Stop-Process -Name "pythonw" -ErrorAction SilentlyContinue
Remove-Item "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\BatteryGuardian.vbs" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:LOCALAPPDATA\LaptopBatteryVoiceAlert" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Laptop Battery Charge Voice Alert has been completely removed." -ForegroundColor Green
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.