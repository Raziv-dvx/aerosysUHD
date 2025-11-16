

# 🐛 Known Issues (Alpha)

## Current Limitations

* GPU monitoring limited to basic detection
* Temperature sensors may not work on all systems
* No per-process monitoring yet
* Occasional visual glitches during window resize
* Startup feature requires admin rights

---

## Planned Fixes for V1

* Improved GPU monitoring with NVIDIA/AMD API support
* Better temperature sensor compatibility
* Process-level monitoring
* Custom theme creation
* Plugin system for extensions

---

# 🤝 Contributing

We welcome contributions!
Please see our **Contributing Guide** for details.

---

## Development Setup

```bash
git clone https://github.com/yourusername/AeroSys-HUD.git
cd AeroSys-HUD
pip install -r requirements.txt

# Make your changes and test
python main.py

# Create test build
pyinstaller --onefile --windowed main.py
```

---

## Code Style

* Follow **PEP 8**
* Use descriptive variable names
* Comment complex logic
* Test on **Windows 10 & 11**

---

# 📊 Technical Details

## Built With

* **Python 3.7+** – core language
* **PyQt5** – GUI framework
* **psutil** – system monitoring
* **PyInstaller** – executable packaging

---

## Architecture

* **Modular design** – UI, monitoring, settings separated
* **Event-driven** – smooth real-time updates
* **Resource efficient** – minimal CPU/RAM usage
* **Extensible** – easy to add new features

---

## Performance Impact

* **CPU:** under 1% average
* **RAM:** ~50MB
* **Update interval:** 0.5s–3s (configurable)

---

# 📄 License

This project is licensed under the **MIT License**.
See the LICENSE file for more details.

---

# 🆘 Support

## Common Issues

**Widget doesn't stay on top in games?**
Enable **All Screens Overlay Mode** from the tray.

**Temperature shows 0°C?**
Your system may not expose temperature sensors to Python.

**Startup doesn't work?**
Run the app **as Administrator** once.

**App uses too much CPU?**
Switch to **Low Power Mode** in Performance Settings.

---

## Getting Help

* Check the documentation
* Open an issue
* Suggest new features
* Ask questions in Discussions

---

# 🏗️ Project Status

* **Current Version:** Alpha V1 Pre-Build
* **Stability:** Experimental
* **Windows Support:** 10 & 11
* **Active Development:** Yes

---

## Roadmap

* **V1 Stable** – bug fixes & performance improvements
* **V2** – plugin system + advanced monitoring
* **V3** – Linux/macOS support

---

⭐ **Star this repo if you find it useful!**
Built with ❤️ for the PC enthusiast community

---

