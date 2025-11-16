# AeroSys HUD 🚀

> **Alpha - V1 Pre-Build** | *Beautiful System Monitoring for Windows*

![AeroSys HUD](docs/screenshots/Screenshot(3).png)

AeroSys HUD is a modern, minimalist system monitoring application with beautiful glassmorphism UI, real-time performance metrics, and a customizable floating widget. Built with Python and PyQt5 for Windows.

---

## ✨ Features

### 🎨 **Visual Excellence**
- **Glassmorphism UI** with blur effects and transparency
- **Dark/Light Theme** support with smooth transitions
- **Rounded Corners** and modern design language
- **Smooth Animations** for all interactions
- **Color-coded Metrics** (CPU: Blue, RAM: Purple, GPU: Red, etc.)

### 📊 **Real-Time Monitoring**
- **CPU Usage** with live percentage and graphs
- **RAM Usage** and memory statistics
- **GPU Usage** monitoring (when available)
- **Network Speed** (Upload/Download)
- **Disk Usage** and storage information
- **Temperature** sensors (system dependent)
- **Battery Level** for laptops
- **Live Clock & Date**

### 🪟 **Smart Widget System**
- **Floating Widget** - Always on top, minimal footprint
- **Draggable & Resizable** - Position anywhere on screen
- **Auto-Hide Mode** - Shows on hover, hides automatically
- **Click-Through Mode** - Widget becomes transparent to mouse
- **Opacity Control** - Adjust transparency (30%-100%)

### ⚡ **Performance & Control**
- **Overlay Modes**: Desktop Only vs All Screens
- **Performance Profiles**: 
  - Low Power (3s updates)
  - Balanced (1s updates) 
  - High Performance (0.5s updates)
- **Startup Integration** - Launch with Windows
- **System Tray** - Minimal background operation

---

## 🚀 Quick Start

### Prerequisites
- **Windows 10/11** (Optimized for Windows 11)
- **Python 3.7+** (if running from source)
- **Administrator Rights** (for startup features)

### Installation Options

#### Option 1: Download Pre-Built Executable (Recommended)
1. Download `AeroSys HUD.exe` from [Releases](../../releases)
2. Run the executable - no installation required!
3. Right-click system tray icon to access settings

#### Option 2: Install from Source
```bash
# Clone repository
git clone https://github.com/Raziv-dvx/aerosysUHD.git
cd AeroSys-HUD

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# Or create your own executable
python install.py
