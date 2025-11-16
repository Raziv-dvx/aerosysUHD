import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu, QAction, QStyle, QSlider, QLabel, QVBoxLayout, QDialog, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap, QMouseEvent
from PyQt5.QtCore import QTimer, Qt, QPoint, QSize
from ui_main import MainWindow
from ui_widget import FloatingWidget
from system_monitor import SystemMonitor
from settings import Settings

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("AeroSys HUD - Settings")
        self.setFixedSize(300, 400)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Settings")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        layout.addWidget(title)
        
        # Close button
        close_btn = QPushButton("×")
        close_btn.setFixedSize(25, 25)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 30);
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 0, 0, 100);
            }
        """)
        
        header_layout = QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        layout.addLayout(header_layout)
        
        # Add your settings controls here
        layout.addStretch()
        
        self.setLayout(layout)
        self.apply_dark_theme()
        
    def apply_dark_theme(self):
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(30, 30, 40, 230), 
                    stop:1 rgba(20, 20, 30, 230));
                border: 1px solid rgba(255, 255, 255, 30);
                border-radius: 15px;
            }
        """)

class AeroSysHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.system_monitor = SystemMonitor()
        
        # Set application icon
        self.set_application_icon()
        
        # Initialize UI components
        self.main_window = MainWindow(self.system_monitor, self.settings)
        
        # Set up main window
        self.setCentralWidget(self.main_window)
        self.setWindowTitle("AeroSys HUD")
        self.setGeometry(100, 100, 300, 400)
        self.setMinimumSize(250, 350)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Dragging variables
        self.dragging = False
        self.drag_position = QPoint()
        
        # System tray
        self.setup_tray()
        
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(1000)
        
        # Apply initial settings
        self.apply_theme()
        self.update_overlay_mode(self.settings.overlay_mode)
        
    def set_application_icon(self):
        """Set the application icon from file or embedded resource"""
        icon_path = self.get_icon_path()
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            self.setWindowIcon(app_icon)
        else:
            # Fallback to system icon
            self.setWindowIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
            
    def get_icon_path(self):
        """Get the path to the icon file, works for both development and packaged exe"""
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            base_path = sys._MEIPASS
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        icon_path = os.path.join(base_path, "icon.ico")
        return icon_path
        
    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        
        # Set tray icon
        icon_path = self.get_icon_path()
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))
        
        tray_menu = QMenu()
        
        # View Menu
        view_menu = QMenu("View", self)
        
        show_action = QAction("Show Main Window", self)
        show_action.triggered.connect(self.show_main_window)
        view_menu.addAction(show_action)
        
        toggle_widget_action = QAction("Toggle Floating Widget", self)
        toggle_widget_action.triggered.connect(self.toggle_widget)
        view_menu.addAction(toggle_widget_action)
        
        self.overlay_action = QAction("Overlay: Desktop Only", self)
        self.overlay_action.triggered.connect(self.toggle_overlay_mode)
        view_menu.addAction(self.overlay_action)
        
        tray_menu.addMenu(view_menu)
        
        # Settings Menu
        settings_menu = QMenu("Settings", self)
        
        startup_action = QAction("Startup with Windows", self, checkable=True)
        startup_action.setChecked(self.settings.startup_enabled)
        startup_action.triggered.connect(self.toggle_startup)
        settings_menu.addAction(startup_action)
        
        theme_action = QAction("Toggle Theme", self)
        theme_action.triggered.connect(self.toggle_theme)
        settings_menu.addAction(theme_action)
        
        # Performance Submenu
        performance_menu = QMenu("Performance Mode", self)
        
        balanced_action = QAction("Balanced", self, checkable=True)
        balanced_action.setChecked(self.settings.performance_mode == "balanced")
        balanced_action.triggered.connect(lambda: self.set_performance_mode("balanced"))
        
        low_power_action = QAction("Low Power", self, checkable=True)
        low_power_action.setChecked(self.settings.performance_mode == "low_power")
        low_power_action.triggered.connect(lambda: self.set_performance_mode("low_power"))
        
        high_perf_action = QAction("High Performance", self, checkable=True)
        high_perf_action.setChecked(self.settings.performance_mode == "high_performance")
        high_perf_action.triggered.connect(lambda: self.set_performance_mode("high_performance"))
        
        performance_menu.addAction(balanced_action)
        performance_menu.addAction(low_power_action)
        performance_menu.addAction(high_perf_action)
        settings_menu.addMenu(performance_menu)
        
        # Widget Settings Submenu
        widget_menu = QMenu("Widget Settings", self)
        
        self.auto_hide_action = QAction("Auto-Hide Widget", self, checkable=True)
        self.auto_hide_action.setChecked(self.settings.widget_auto_hide)
        self.auto_hide_action.triggered.connect(self.toggle_auto_hide)
        widget_menu.addAction(self.auto_hide_action)
        
        self.click_through_action = QAction("Click-Through Mode", self, checkable=True)
        self.click_through_action.setChecked(self.settings.widget_click_through)
        self.click_through_action.triggered.connect(self.toggle_click_through)
        widget_menu.addAction(self.click_through_action)
        
        # Opacity Submenu
        opacity_menu = QMenu("Widget Opacity", self)
        
        opacity_values = [0.3, 0.5, 0.7, 0.9, 1.0]
        for opacity in opacity_values:
            opacity_action = QAction(f"{int(opacity*100)}%", self, checkable=True)
            opacity_action.setChecked(self.settings.widget_opacity == opacity)
            opacity_action.triggered.connect(lambda checked, o=opacity: self.set_widget_opacity(o))
            opacity_menu.addAction(opacity_action)
        
        widget_menu.addMenu(opacity_menu)
        settings_menu.addMenu(widget_menu)
        
        tray_menu.addMenu(settings_menu)
        tray_menu.addSeparator()
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_main_window()
            
    def show_main_window(self):
        self.show()
        self.raise_()
        self.activateWindow()
        
    def toggle_widget(self):
        if not hasattr(self, 'floating_widget') or not self.floating_widget:
            self.floating_widget = FloatingWidget(self.system_monitor, self.settings)
            self.floating_widget.on_show_full_app = self.show_main_window
            self.floating_widget.on_widget_closed = lambda: setattr(self, 'floating_widget', None)
            self.update_widget_settings()
            self.floating_widget.show()
        else:
            if self.floating_widget.isVisible():
                self.floating_widget.hide()
            else:
                self.floating_widget.show()
                
    def update_widget_settings(self):
        """Apply current settings to widget"""
        if hasattr(self, 'floating_widget') and self.floating_widget:
            self.floating_widget.set_auto_hide(self.settings.widget_auto_hide)
            self.floating_widget.set_click_through(self.settings.widget_click_through)
            self.floating_widget.set_opacity(self.settings.widget_opacity)
                
    def toggle_startup(self):
        self.settings.toggle_startup()
        
    def toggle_overlay_mode(self):
        new_mode = self.settings.toggle_overlay_mode()
        self.update_overlay_mode(new_mode)
        
    def update_overlay_mode(self, mode):
        if mode == "all_screens":
            # Make visible on all screens/workspaces
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            if hasattr(self, 'floating_widget') and self.floating_widget:
                self.floating_widget.setWindowFlags(self.floating_widget.windowFlags() | Qt.WindowStaysOnTopHint)
            self.overlay_action.setText("Overlay: All Screens")
        else:
            # Desktop only
            current_flags = self.windowFlags()
            self.setWindowFlags((current_flags & ~Qt.WindowStaysOnTopHint) | Qt.FramelessWindowHint)
            if hasattr(self, 'floating_widget') and self.floating_widget:
                widget_flags = self.floating_widget.windowFlags()
                self.floating_widget.setWindowFlags((widget_flags & ~Qt.WindowStaysOnTopHint) | Qt.FramelessWindowHint | Qt.Tool)
            self.overlay_action.setText("Overlay: Desktop Only")
        
        self.show()  # Re-apply window flags
        if hasattr(self, 'floating_widget') and self.floating_widget:
            self.floating_widget.show()
            
    def set_performance_mode(self, mode):
        self.settings.set_performance_mode(mode)
        if mode == "low_power":
            self.update_timer.setInterval(3000)  # Update every 3 seconds
        elif mode == "high_performance":
            self.update_timer.setInterval(500)   # Update every 0.5 seconds
        else:
            self.update_timer.setInterval(1000)  # Default 1 second
            
    def toggle_auto_hide(self):
        enabled = self.settings.toggle_auto_hide()
        if hasattr(self, 'floating_widget') and self.floating_widget:
            self.floating_widget.set_auto_hide(enabled)
            
    def toggle_click_through(self):
        enabled = self.settings.toggle_click_through()
        if hasattr(self, 'floating_widget') and self.floating_widget:
            self.floating_widget.set_click_through(enabled)
            
    def set_widget_opacity(self, opacity):
        self.settings.set_widget_opacity(opacity)
        if hasattr(self, 'floating_widget') and self.floating_widget:
            self.floating_widget.set_opacity(opacity)
        
    def toggle_theme(self):
        self.settings.toggle_theme()
        self.apply_theme()
        
    def apply_theme(self):
        theme = self.settings.theme
        self.main_window.apply_theme(theme)
        if hasattr(self, 'floating_widget') and self.floating_widget:
            self.floating_widget.apply_theme(theme)
        
    def update_data(self):
        self.system_monitor.update_all()
        self.main_window.update_display()
        if hasattr(self, 'floating_widget') and self.floating_widget and self.floating_widget.isVisible():
            self.floating_widget.update_display()
            
    def quit_app(self):
        if hasattr(self, 'floating_widget') and self.floating_widget:
            self.floating_widget.close()
        QApplication.quit()

    # Dragging functionality for main window
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.dragging = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Set application style
    app.setStyle("Fusion")
    
    window = AeroSysHUD()
    window.show()
    
    sys.exit(app.exec_())