param (
    [string]$Lang = "",
    [string]$Voice = ""
)

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "   Laptop Battery Charge Voice Alert - Auto Setup   " -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Cyan

# ১. পাইথন চেক ও অটো-ইনস্টলেশন (যদি পিসিতে পাইথন না থাকে)
function Ensure-Python {
    try {
        $null = python --version 2>&1
        Write-Host "[OK] Python is already installed." -ForegroundColor Green
    } catch {
        Write-Host "`nPython not detected! Automatically installing Python..." -ForegroundColor Yellow
        if (Get-Command winget -ErrorAction SilentlyContinue) {
            winget install Python.Python.3.11 --silent --accept-source-agreements --accept-package-agreements
        } else {
            $installerUrl = "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe"
            $installerPath = "$env:TEMP\python_installer.exe"
            Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath
            Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait
            Remove-Item $installerPath -Force -ErrorAction SilentlyContinue
        }
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        Write-Host "[OK] Python installed successfully!" -ForegroundColor Green
    }
}

Ensure-Python

# ২. ভাষা ও ভয়েস নির্বাচন (যদি কমান্ডে না দেওয়া থাকে)
if (-not $Lang) {
    Write-Host "`nSelect your alert language / ভাষা নির্বাচন করুন:" -ForegroundColor Yellow
    Write-Host "1. British English (Sonia - Elegant & Cute) [Default]"
    Write-Host "2. Bengali / বাংলা (Nabanita - Natural Voice)"
    Write-Host "3. Custom Language / Voice"
    $choice = Read-Host "Enter choice [1, 2, or 3] (Default is 1)"
    
    if ($choice -eq "2") {
        $Lang = "bn"
        $Voice = "bn-BD-NabanitaNeural"
    } elseif ($choice -eq "3") {
        $Lang = Read-Host "Enter Language Code (e.g., en, bn, hi, es, fr)"
        $Voice = Read-Host "Enter Edge TTS Voice Model (e.g., en-US-AvaNeural, hi-IN-SwaraNeural)"
    } else {
        $Lang = "en"
        $Voice = "en-GB-SoniaNeural"
    }
}

if (-not $Voice) {
    if ($Lang -eq "bn") {
        $Voice = "bn-BD-NabanitaNeural"
    } else {
        $Voice = "en-GB-SoniaNeural"
    }
}

# ৩. ফাইল ডাউনলোড ও ডিরেক্টরি সেটআপ
$targetDir = "$env:LOCALAPPDATA\LaptopBatteryVoiceAlert"
if (!(Test-Path -Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
}

$repoBaseUrl = "https://raw.githubusercontent.com/tuhinfay/Laptop-Battery-Charge-Voice-Alert/main"

Write-Host "`nDownloading latest files from repository..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "$repoBaseUrl/battery_guardian.pyw" -OutFile "$targetDir\battery_guardian.pyw"

$configJson = @"
{
  "language": "$Lang",
  "voice": "$Voice",
  "check_normal": 300,
  "check_alert": 60,
  "thresholds": {
    "warn_50": 50,
    "warn_30": 30,
    "critical_20": 20,
    "warn_80": 80,
    "max_95": 95
  }
}
"@
$configJson | Out-File -FilePath "$targetDir\config.json" -Encoding utf8

# ৪. উইন্ডোজ স্টার্টআপে সাইলেন্ট ভিবিএস স্ক্রিপ্ট যুক্ত করা
$startupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$vbsPath = "$startupFolder\BatteryGuardian.vbs"

$vbsContent = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw """ & "$targetDir\battery_guardian.pyw""" , 0, False
"@
$vbsContent | Out-File -FilePath $vbsPath -Encoding ascii

# ৫. প্যাকেজ ডিপেন্ডেন্সি ইন্সটল
Write-Host "Installing runtime dependencies (psutil, edge-tts, pywin32)..." -ForegroundColor Yellow
Start-Process -FilePath "python" -ArgumentList "-m pip install psutil edge-tts pywin32 --quiet" -Wait -NoNewWindow

# ৬. ব্যাকগ্রাউন্ডে তাৎক্ষণিক রান করা
Write-Host "Starting Battery Voice Alert in background..." -ForegroundColor Green
wscript $vbsPath

Write-Host "`n[SUCCESS] Setup complete! Voice Alert is active and will autostart on Windows boot." -ForegroundColor Green