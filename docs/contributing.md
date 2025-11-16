# Contributing to AeroSys HUD

We love your input! We want to make contributing to AeroSys HUD as easy and transparent as possible.

## Development Process

1. Fork the repo and create your branch from `main`
2. Make your changes
3. Test on Windows 10/11
4. Submit a pull request

## Code Style

### Python
- Follow PEP 8 guidelines
- Use descriptive variable names
- Comment complex logic sections
- Type hints encouraged but not required

### UI/UX
- Maintain glassmorphism design language
- Ensure smooth animations (60fps target)
- Test both dark and light themes
- Keep minimalistic approach

### Git Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters or less

## Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/Raziv-dvx/aerosysUHD.git
cd AeroSys-HUD

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test your changes
python main.py
