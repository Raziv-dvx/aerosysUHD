

# 🔧 Advanced Installation

```bash
# Create executable with custom icon
pyinstaller --onefile --windowed --icon=icon.ico --name "AeroSys HUD" main.py

# Or use the provided build script
python install.py
```

---

# 🎮 Usage Guide

## Basic Controls

* **Drag:** Click and drag anywhere on the main window
* **Resize:** Grab the bottom-right corner of the widget
* **Close Widget:** Click the red × button
* **Show Full App:** Click the ☰ button on the widget

---

## System Tray Menu

Right-click the system tray icon to access:

* Show / Hide Main Window
* Toggle Floating Widget
* Overlay Mode Settings
* Performance Profiles
* Widget Behavior Settings
* Theme Toggle
* Startup Control
* Quit Application

---

## Overlay Modes

* **Desktop Only:** Visible only on desktop (default)
* **All Screens:** Stays visible in games and fullscreen apps

---

# 🛠️ Configuration

## Settings File Location

```
%APPDATA%/aerohud_config.json
```

---

## Manual Configuration Example

```json
{
  "theme": "dark",
  "overlay_mode": "desktop_only",
  "performance_mode": "balanced",
  "widget_auto_hide": false,
  "widget_click_through": false,
  "widget_opacity": 0.9
}
```

---


