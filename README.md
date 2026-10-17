<div align="center">

# ⚡ Laptop Battery Charge Voice Alert

### *Intelligent, Headless Battery Health Monitor with Natural AI Voice Synthesis & Desktop Toast Alerts*

[![GitHub Stars](https://img.shields.io/github/stars/tuhinfay/Laptop-Battery-Charge-Voice-Alert?style=for-the-badge&color=ffd700)](https://github.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/tuhinfay/Laptop-Battery-Charge-Voice-Alert?style=for-the-badge&color=60a5fa)](https://github.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/network/members)
[![License: MIT](https://img.shields.io/badge/License-MIT-34d399.svg?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-0078d4?style=for-the-badge&logo=windows)](https://www.microsoft.com/windows)
[![Python Engine](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)

<p align="center">
  <b>Tired of overcharging your laptop or draining it down to zero without noticing?</b><br>
  <b>Laptop Battery Charge Voice Alert</b> runs completely headless in the background, preserves battery lifespan using smart charge thresholds, and alerts you with ultra-realistic human AI voices (British English, Bengali, or custom TTS models).
</p>

[Quick Install](#-one-line-quick-install) • [Key Features](#-core-features) • [Threshold Matrix](#-alert-thresholds--behavior) • [Uninstallation](#-stop-or-uninstall)

---

</div>

## 🌟 Why Use Laptop Battery Charge Voice Alert?

Most operating systems notify you only when the battery is already about to shut down. Modern lithium-ion laptop batteries last significantly longer when kept between **20% and 80%**. 

**Laptop Battery Charge Voice Alert** bridges this gap:
- 🔊 **Zero Gimmicks, Pure Speech:** High-clarity neural audio keeps you informed across the room without glancing at the screen.
- ⚡ **Zero-Touch Automation:** Automatically detects if Python is missing, installs it silently, registers dependencies, and establishes persistent Windows startup execution.
- 🍃 **Lightweight & Efficient:** Negligible background consumption (~0% CPU, ~18 MB RAM) using native Win32 multimedia APIs.

---

## 🚀 One-Line Quick Install

Open **PowerShell** (Press <kbd>Win</kbd> + <kbd>X</kbd> and select **Terminal** or **PowerShell**) and paste your preferred command:

### 🇬🇧 Option 1: British English (Sonia — Soft & Elegant Voice)
```powershell
& ([scriptblock]::Create((irm [https://raw.githubusercontent.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/main/install.ps1](https://raw.githubusercontent.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/main/install.ps1)))) -Lang "en" -Voice "en-GB-SoniaNeural"