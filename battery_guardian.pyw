import os
import sys
import json
import time
import ctypes
import asyncio
import subprocess

# মিসিং ডিপেন্ডেন্সি ব্যাকগ্রাউন্ডে অটো-ইন্সটল
REQUIRED_PACKAGES = ["psutil", "edge-tts", "pywin32"]
for pkg in REQUIRED_PACKAGES:
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", pkg, "--quiet", "--no-warn-script-location"]
        )

import psutil
import edge_tts
import win32com.client

APP_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(APP_DIR, "config.json")

# বহুভাষিক নোটিফিকেশন ও ভয়েস মেসেজ
MESSAGES = {
    "en": {
        "title_notice": "Battery Notice",
        "title_warn": "Low Battery Warning",
        "title_critical": "Critical Battery Alert!",
        "title_charged": "Battery Charged",
        "title_unplug": "Unplug Charger!",
        "notice_50": "Notice. Battery level is at {p} percent.",
        "warn_30": "Battery dropped to {p} percent. Please consider plugging in.",
        "critical_20": "Warning! Battery is critically low at {p} percent. Please connect the charger immediately.",
        "charged_80": "Battery reached {p} percent. It is sufficiently charged.",
        "unplug_95": "Attention! Battery is at {p} percent. Please disconnect the charger to save battery health."
    },
    "bn": {
        "title_notice": "ব্যাটারি নোটিশ",
        "title_warn": "লো ব্যাটারি সতর্কতা",
        "title_critical": "জরুরি সতর্কতা!",
        "title_charged": "পর্যাপ্ত চার্জ সম্পন্ন",
        "title_unplug": "চার্জার খুলে ফেলুন!",
        "notice_50": "আপনার ল্যাপটপের ব্যাটারি চার্জ এখন {p} শতাংশ।",
        "warn_30": "ব্যাটারি চার্জ {p} শতাংশে নেমে এসেছে। চার্জে দেওয়ার প্রস্তুতি নিন।",
        "critical_20": "সতর্কতা! ব্যাটারি চার্জ মাত্র {p} শতাংশ। দ্রুত চার্জার সংযোগ করুন।",
        "charged_80": "ব্যাটারি চার্জ {p} শতাংশ হয়েছে। পর্যাপ্ত চার্জ সম্পন্ন।",
        "unplug_95": "ব্যাটারি চার্জ {p} শতাংশ হয়েছে। ব্যাটারির সুরক্ষায় দয়া করে চার্জারটি আনপ্লাগ করুন।"
    }
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "language": "en",
        "voice": "en-GB-SoniaNeural",
        "check_normal": 300,
        "check_alert": 60
    }

cfg = load_config()
LANG = cfg.get("language", "en")
VOICE = cfg.get("voice", "en-GB-SoniaNeural")
msg_dict = MESSAGES.get(LANG, MESSAGES["en"])

winmm = ctypes.windll.winmm

def play_audio(file_path):
    alias = "battery_alert_snd"
    winmm.mciSendStringW(f'open "{file_path}" type mpegvideo alias {alias}', None, 0, None)
    winmm.mciSendStringW(f'play {alias} wait', None, 0, None)
    winmm.mciSendStringW(f'close {alias}', None, 0, None)

def speak(text):
    temp_file = os.path.join(os.environ.get("TEMP", "."), "bg_voice.mp3")
    try:
        async def _run():
            com = edge_tts.Communicate(text, VOICE)
            await com.save(temp_file)
        asyncio.run(_run())
        play_audio(temp_file)
        if os.path.exists(temp_file):
            os.remove(temp_file)
    except Exception:
        # ইন্টারনেট অফলাইন থাকলে উইন্ডোজের নিজস্ব SAPI স্পিকার ফলব্যাক
        try:
            spk = win32com.client.Dispatch("SAPI.SpVoice")
            spk.Speak(text)
        except Exception:
            pass

def alert_user(title, text):
    ps_cmd = (
        f"[void] [System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms');"
        f"$notify = New-Object System.Windows.Forms.NotifyIcon;"
        f"$notify.Icon = [System.Drawing.SystemIcons]::Information;"
        f"$notify.Visible = $True;"
        f"$notify.ShowBalloonTip(5000, '{title}', '{text}', [System.Windows.Forms.ToolTipIcon]::Info);"
    )
    subprocess.Popen(["powershell", "-WindowStyle", "Hidden", "-Command", ps_cmd])
    speak(text)

warn_50_sent = False
warn_30_sent = False
warn_80_sent = False

while True:
    battery = psutil.sensors_battery()
    if battery is None:
        time.sleep(cfg.get("check_normal", 300))
        continue

    percent = battery.percent
    is_plugged = battery.power_plugged
    sleep_time = cfg.get("check_normal", 300)

    # চার্জার ছাড়া অবস্থা (ডিসচার্জিং)
    if not is_plugged:
        warn_80_sent = False
        if percent <= 50:
            sleep_time = cfg.get("check_alert", 60)
            if percent <= 20:
                alert_user(msg_dict["title_critical"], msg_dict["critical_20"].format(p=percent))
            elif percent <= 30:
                if not warn_30_sent:
                    alert_user(msg_dict["title_warn"], msg_dict["warn_30"].format(p=percent))
                    warn_30_sent = True
            else:
                if not warn_50_sent:
                    alert_user(msg_dict["title_notice"], msg_dict["notice_50"].format(p=percent))
                    warn_50_sent = True
        else:
            warn_50_sent = False
            warn_30_sent = False
            sleep_time = cfg.get("check_normal", 300)

    # চার্জার লাগানো অবস্থা (চার্জিং)
    else:
        warn_50_sent = False
        warn_30_sent = False
        if percent >= 80:
            sleep_time = cfg.get("check_alert", 60)
            if percent >= 95:
                alert_user(msg_dict["title_unplug"], msg_dict["unplug_95"].format(p=percent))
            else:
                if not warn_80_sent:
                    alert_user(msg_dict["title_charged"], msg_dict["charged_80"].format(p=percent))
                    warn_80_sent = True
        else:
            warn_80_sent = False
            sleep_time = cfg.get("check_normal", 300)

    time.sleep(sleep_time)