import json
import os
import sys
import winreg as reg

class Settings:
    def __init__(self):
        self.config_file = "aerohud_config.json"
        self.theme = "dark"
        self.widget_visible = False
        self.startup_enabled = False
        self.main_window_position = [100, 100]
        self.widget_position = [1200, 100]
        
        # New settings
        self.overlay_mode = "desktop_only"  # or "all_screens"
        self.performance_mode = "balanced"  # balanced, low_power, high_performance
        self.widget_auto_hide = False
        self.widget_click_through = False
        self.widget_opacity = 0.9
        
        self.load_settings()
        self.check_startup()
        
    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.theme = data.get('theme', 'dark')
                    self.widget_visible = data.get('widget_visible', False)
                    self.startup_enabled = data.get('startup_enabled', False)
                    self.main_window_position = data.get('main_window_position', [100, 100])
                    self.widget_position = data.get('widget_position', [1200, 100])
                    
                    # New settings
                    self.overlay_mode = data.get('overlay_mode', 'desktop_only')
                    self.performance_mode = data.get('performance_mode', 'balanced')
                    self.widget_auto_hide = data.get('widget_auto_hide', False)
                    self.widget_click_through = data.get('widget_click_through', False)
                    self.widget_opacity = data.get('widget_opacity', 0.9)
            except:
                self.create_default_settings()
        else:
            self.create_default_settings()
            
    def save_settings(self):
        data = {
            'theme': self.theme,
            'widget_visible': self.widget_visible,
            'startup_enabled': self.startup_enabled,
            'main_window_position': self.main_window_position,
            'widget_position': self.widget_position,
            
            # New settings
            'overlay_mode': self.overlay_mode,
            'performance_mode': self.performance_mode,
            'widget_auto_hide': self.widget_auto_hide,
            'widget_click_through': self.widget_click_through,
            'widget_opacity': self.widget_opacity
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=4)
            
    def create_default_settings(self):
        self.theme = "dark"
        self.widget_visible = False
        self.startup_enabled = False
        self.main_window_position = [100, 100]
        self.widget_position = [1200, 100]
        self.overlay_mode = "desktop_only"
        self.performance_mode = "balanced"
        self.widget_auto_hide = False
        self.widget_click_through = False
        self.widget_opacity = 0.9
        self.save_settings()
        
    def toggle_theme(self):
        self.theme = "light" if self.theme == "dark" else "dark"
        self.save_settings()
        
    def toggle_startup(self):
        if self.startup_enabled:
            self.disable_startup()
        else:
            self.enable_startup()
        self.save_settings()
        return self.startup_enabled
        
    def enable_startup(self):
        """Add application to Windows startup"""
        try:
            key = reg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with reg.OpenKey(key, subkey, 0, reg.KEY_SET_VALUE) as registry_key:
                app_path = os.path.abspath(sys.argv[0])
                # If running as script, use pythonw.exe to run without console
                if app_path.endswith('.py'):
                    pythonw_path = sys.executable.replace('python.exe', 'pythonw.exe')
                    app_path = f'"{pythonw_path}" "{app_path}"'
                
                reg.SetValueEx(registry_key, "AeroSysHUD", 0, reg.REG_SZ, app_path)
                self.startup_enabled = True
                return True
        except Exception as e:
            print(f"Failed to enable startup: {e}")
            return False
            
    def disable_startup(self):
        """Remove application from Windows startup"""
        try:
            key = reg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with reg.OpenKey(key, subkey, 0, reg.KEY_SET_VALUE) as registry_key:
                reg.DeleteValue(registry_key, "AeroSysHUD")
                self.startup_enabled = False
                return True
        except Exception as e:
            print(f"Failed to disable startup: {e}")
            return False
            
    def check_startup(self):
        """Check if application is in Windows startup"""
        try:
            key = reg.HKEY_CURRENT_USER
            subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
            
            with reg.OpenKey(key, subkey, 0, reg.KEY_READ) as registry_key:
                try:
                    reg.QueryValueEx(registry_key, "AeroSysHUD")
                    self.startup_enabled = True
                except FileNotFoundError:
                    self.startup_enabled = False
        except Exception as e:
            print(f"Failed to check startup: {e}")
            self.startup_enabled = False

    # New methods for overlay mode
    def toggle_overlay_mode(self):
        self.overlay_mode = "all_screens" if self.overlay_mode == "desktop_only" else "desktop_only"
        self.save_settings()
        return self.overlay_mode

    # New methods for performance mode
    def set_performance_mode(self, mode):
        self.performance_mode = mode
        self.save_settings()

    # New methods for widget auto-hide
    def toggle_auto_hide(self):
        self.widget_auto_hide = not self.widget_auto_hide
        self.save_settings()
        return self.widget_auto_hide

    # New methods for widget click-through
    def toggle_click_through(self):
        self.widget_click_through = not self.widget_click_through
        self.save_settings()
        return self.widget_click_through

    # New methods for widget opacity
    def set_widget_opacity(self, opacity):
        self.widget_opacity = max(0.1, min(1.0, opacity))
        self.save_settings()