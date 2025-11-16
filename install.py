import os
import sys
import subprocess
import ctypes
import winreg as reg
from pathlib import Path

def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def install_requirements():
    """Install required Python packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        return False

def create_start_menu_shortcut():
    """Create Start Menu shortcut with icon"""
    try:
        # Get paths
        startup_folder = os.path.join(
            os.environ['APPDATA'], 
            "Microsoft", "Windows", "Start Menu", "Programs"
        )
        
        shortcut_path = os.path.join(startup_folder, "AeroSys HUD.lnk")
        icon_path = os.path.abspath("icon.ico")
        script_path = os.path.abspath("main.py")
        
        # Create shortcut using Windows Script Host with icon
        vbs_script = f"""
        Set shell = CreateObject("WScript.Shell")
        Set shortcut = shell.CreateShortcut("{shortcut_path}")
        shortcut.TargetPath = "{sys.executable}"
        shortcut.Arguments = "{script_path}"
        shortcut.WorkingDirectory = "{os.path.dirname(script_path)}"
        shortcut.Description = "AeroSys HUD System Monitor"
        shortcut.IconLocation = "{icon_path}"
        shortcut.Save
        """
        
        with open("create_shortcut.vbs", "w") as f:
            f.write(vbs_script)
            
        subprocess.run(["cscript", "create_shortcut.vbs"], capture_output=True)
        os.remove("create_shortcut.vbs")
        
        print("✓ Start Menu shortcut created with icon")
        return True
    except Exception as e:
        print(f"✗ Failed to create shortcut: {e}")
        return False

def create_desktop_shortcut():
    """Create Desktop shortcut with icon"""
    try:
        desktop_folder = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        shortcut_path = os.path.join(desktop_folder, "AeroSys HUD.lnk")
        icon_path = os.path.abspath("icon.ico")
        script_path = os.path.abspath("main.py")
        
        vbs_script = f"""
        Set shell = CreateObject("WScript.Shell")
        Set shortcut = shell.CreateShortcut("{shortcut_path}")
        shortcut.TargetPath = "{sys.executable}"
        shortcut.Arguments = "{script_path}"
        shortcut.WorkingDirectory = "{os.path.dirname(script_path)}"
        shortcut.Description = "AeroSys HUD System Monitor"
        shortcut.IconLocation = "{icon_path}"
        shortcut.Save
        """
        
        with open("create_desktop_shortcut.vbs", "w") as f:
            f.write(vbs_script)
            
        subprocess.run(["cscript", "create_desktop_shortcut.vbs"], capture_output=True)
        os.remove("create_desktop_shortcut.vbs")
        
        print("✓ Desktop shortcut created with icon")
        return True
    except Exception as e:
        print(f"✗ Failed to create desktop shortcut: {e}")
        return False

def create_exe_with_icon():
    """Create executable using PyInstaller with icon"""
    try:
        icon_path = os.path.abspath("icon.ico")
        
        if not os.path.exists(icon_path):
            print("⚠  Icon file not found, creating executable without icon")
            subprocess.check_call([
                sys.executable, "-m", "PyInstaller", 
                "--onefile", "--windowed", "--name", "AeroSys HUD",
                "main.py"
            ])
        else:
            subprocess.check_call([
                sys.executable, "-m", "PyInstaller", 
                "--onefile", "--windowed", "--name", "AeroSys HUD",
                f"--icon={icon_path}",
                "main.py"
            ])
            print("✓ Executable created with custom icon")
        
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to create executable")
        return False

def create_installer_nsis():
    """Create a proper Windows installer using NSIS (optional)"""
    try:
        # Check if NSIS is installed
        nsis_path = r"C:\Program Files (x86)\NSIS\makensis.exe"
        if not os.path.exists(nsis_path):
            print("⚠  NSIS not found, skipping installer creation")
            print("   Download NSIS from: https://nsis.sourceforge.io/Download")
            return False
            
        # Create NSIS script
        nsis_script = """
        !include "MUI2.nsh"
        
        Name "AeroSys HUD"
        OutFile "AeroSys_HUD_Setup.exe"
        InstallDir "$PROGRAMFILES\\AeroSys HUD"
        
        !define MUI_ICON "icon.ico"
        !define MUI_UNICON "icon.ico"
        !define MUI_ABORTWARNING
        
        !insertmacro MUI_PAGE_WELCOME
        !insertmacro MUI_PAGE_DIRECTORY
        !insertmacro MUI_PAGE_INSTFILES
        !insertmacro MUI_PAGE_FINISH
        
        !insertmacro MUI_UNPAGE_CONFIRM
        !insertmacro MUI_UNPAGE_INSTFILES
        
        !insertmacro MUI_LANGUAGE "English"
        
        Section "Main Application"
            SetOutPath "$INSTDIR"
            File "dist\\AeroSys HUD.exe"
            File "icon.ico"
            
            CreateDirectory "$SMPROGRAMS\\AeroSys HUD"
            CreateShortCut "$SMPROGRAMS\\AeroSys HUD\\AeroSys HUD.lnk" "$INSTDIR\\AeroSys HUD.exe" "" "$INSTDIR\\icon.ico"
            CreateShortCut "$DESKTOP\\AeroSys HUD.lnk" "$INSTDIR\\AeroSys HUD.exe" "" "$INSTDIR\\icon.ico"
            
            WriteUninstaller "$INSTDIR\\Uninstall.exe"
            WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AeroSysHUD" \
                "DisplayName" "AeroSys HUD"
            WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AeroSysHUD" \
                "UninstallString" "$INSTDIR\\Uninstall.exe"
            WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AeroSysHUD" \
                "DisplayIcon" "$INSTDIR\\icon.ico"
        SectionEnd
        
        Section "Uninstall"
            Delete "$INSTDIR\\AeroSys HUD.exe"
            Delete "$INSTDIR\\icon.ico"
            Delete "$INSTDIR\\Uninstall.exe"
            RMDir "$INSTDIR"
            
            Delete "$SMPROGRAMS\\AeroSys HUD\\AeroSys HUD.lnk"
            RMDir "$SMPROGRAMS\\AeroSys HUD"
            Delete "$DESKTOP\\AeroSys HUD.lnk"
            
            DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\AeroSysHUD"
        SectionEnd
        """
        
        with open("installer.nsi", "w") as f:
            f.write(nsis_script)
            
        subprocess.run([nsis_path, "installer.nsi"])
        os.remove("installer.nsi")
        
        print("✓ Windows installer created: AeroSys_HUD_Setup.exe")
        return True
    except Exception as e:
        print(f"✗ Failed to create installer: {e}")
        return False

def main():
    print("AeroSys HUD Installer")
    print("=" * 40)
    
    # Check for icon file
    if not os.path.exists("icon.ico"):
        print("⚠  Warning: icon.ico not found in current directory")
        print("   Please add an icon file for better appearance")
        print("   You can create one at: https://convertio.co/png-ico/")
        print()
    
    if not is_admin():
        print("⚠  Warning: Running without administrator privileges")
        print("   Some features may require admin rights")
        print()
    
    # Install dependencies
    print("1. Installing dependencies...")
    if not install_requirements():
        return
    
    # Create executable
    print("\n2. Creating executable...")
    create_exe_with_icon()
    
    # Create shortcuts
    print("\n3. Creating shortcuts...")
    create_start_menu_shortcut()
    create_desktop_shortcut()
    
    # Optional: Create proper installer
    print("\n4. Creating Windows installer (optional)...")
    create_installer = input("   Create proper Windows installer? (y/n): ").lower().strip()
    if create_installer == 'y':
        create_installer_nsis()
    
    print("\n" + "=" * 40)
    print("Installation completed successfully!")
    print("\nYou can now:")
    print("• Run 'AeroSys HUD.exe' from the dist folder")
    print("• Find AeroSys HUD in your Start Menu")
    print("• Use the desktop shortcut")
    print("• Enable startup from the tray menu")
    
    if os.path.exists("dist/AeroSys HUD.exe"):
        print(f"\nExecutable location: {os.path.abspath('dist/AeroSys HUD.exe')}")

if __name__ == "__main__":
    main()