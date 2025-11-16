from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer, QPoint, QSize
from PyQt5.QtGui import QMouseEvent, QFont, QPainter, QColor

class FloatingWidget(QWidget):
    def __init__(self, system_monitor, settings):
        super().__init__()
        self.system_monitor = system_monitor
        self.settings = settings
        self.dragging = False
        self.drag_position = QPoint()
        self.resize_edge = None
        self.minimum_size = QSize(150, 100)
        self.auto_hide = False
        
        # Auto-hide timer
        self.auto_hide_timer = QTimer()
        self.auto_hide_timer.timeout.connect(self.hide_widget)
        
        self.init_ui()
        self.apply_theme(self.settings.theme)
        self.apply_settings()
        
    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumSize(self.minimum_size)
        self.resize(180, 120)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)
        
        # Header with title and buttons
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("AeroSys")
        self.title_label.setObjectName("widgetTitle")
        
        self.show_full_btn = QPushButton("☰")
        self.show_full_btn.setFixedSize(16, 16)
        self.show_full_btn.setObjectName("widgetMenuBtn")
        self.show_full_btn.setToolTip("Show Full Application")
        
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(16, 16)
        self.close_btn.setObjectName("widgetCloseBtn")
        self.close_btn.setToolTip("Close Widget")
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.show_full_btn)
        header_layout.addWidget(self.close_btn)
        
        layout.addLayout(header_layout)
        
        # Compact metrics in horizontal layout
        metrics_layout = QHBoxLayout()
        
        # CPU
        cpu_frame = QFrame()
        cpu_layout = QVBoxLayout()
        cpu_layout.setContentsMargins(5, 2, 5, 2)
        
        cpu_title = QLabel("CPU")
        cpu_title.setObjectName("widgetMetricTitle")
        self.cpu_value = QLabel("0%")
        self.cpu_value.setObjectName("widgetMetricValue")
        
        cpu_layout.addWidget(cpu_title)
        cpu_layout.addWidget(self.cpu_value)
        cpu_frame.setLayout(cpu_layout)
        
        # RAM
        ram_frame = QFrame()
        ram_layout = QVBoxLayout()
        ram_layout.setContentsMargins(5, 2, 5, 2)
        
        ram_title = QLabel("RAM")
        ram_title.setObjectName("widgetMetricTitle")
        self.ram_value = QLabel("0%")
        self.ram_value.setObjectName("widgetMetricValue")
        
        ram_layout.addWidget(ram_title)
        ram_layout.addWidget(self.ram_value)
        ram_frame.setLayout(ram_layout)
        
        metrics_layout.addWidget(cpu_frame)
        metrics_layout.addWidget(ram_frame)
        
        layout.addLayout(metrics_layout)
        
        # Time
        self.time_label = QLabel("00:00:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setObjectName("widgetTime")
        
        layout.addWidget(self.time_label)
        
        self.setLayout(layout)
        
        # Connect signals
        self.close_btn.clicked.connect(self.close_widget)
        self.show_full_btn.clicked.connect(self.show_full_app)
        
        # Enable mouse tracking for auto-hide
        self.setMouseTracking(True)
        
    def apply_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet("""
                QWidget {
                    background: rgba(30, 30, 40, 200);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 40);
                    border-radius: 10px;
                }
                #widgetTitle {
                    color: rgba(255, 255, 255, 180);
                    font-size: 11px;
                    font-weight: bold;
                }
                #widgetMetricTitle {
                    color: rgba(255, 255, 255, 140);
                    font-size: 9px;
                    font-weight: bold;
                }
                #widgetMetricValue {
                    color: white;
                    font-size: 12px;
                    font-weight: bold;
                }
                #widgetTime {
                    color: rgba(255, 255, 255, 200);
                    font-size: 14px;
                    font-weight: bold;
                }
                #widgetMenuBtn, #widgetCloseBtn {
                    background: transparent;
                    color: rgba(255, 255, 255, 180);
                    border: none;
                    border-radius: 3px;
                    font-size: 12px;
                    font-weight: bold;
                }
                #widgetMenuBtn:hover {
                    background: rgba(255, 255, 255, 30);
                }
                #widgetCloseBtn:hover {
                    background: rgba(255, 0, 0, 100);
                    color: white;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background: rgba(240, 240, 245, 200);
                    color: #333333;
                    border: 1px solid rgba(0, 0, 0, 40);
                    border-radius: 10px;
                }
                #widgetTitle {
                    color: rgba(0, 0, 0, 180);
                    font-size: 11px;
                    font-weight: bold;
                }
                #widgetMetricTitle {
                    color: rgba(0, 0, 0, 140);
                    font-size: 9px;
                    font-weight: bold;
                }
                #widgetMetricValue {
                    color: #333333;
                    font-size: 12px;
                    font-weight: bold;
                }
                #widgetTime {
                    color: rgba(0, 0, 0, 200);
                    font-size: 14px;
                    font-weight: bold;
                }
                #widgetMenuBtn, #widgetCloseBtn {
                    background: transparent;
                    color: rgba(0, 0, 0, 180);
                    border: none;
                    border-radius: 3px;
                    font-size: 12px;
                    font-weight: bold;
                }
                #widgetMenuBtn:hover {
                    background: rgba(0, 0, 0, 30);
                }
                #widgetCloseBtn:hover {
                    background: rgba(255, 0, 0, 100);
                    color: white;
                }
            """)
            
    def apply_settings(self):
        """Apply current settings to widget"""
        self.set_opacity(self.settings.widget_opacity)
        self.set_click_through(self.settings.widget_click_through)
        self.set_auto_hide(self.settings.widget_auto_hide)
            
    def set_opacity(self, value):
        """Set widget opacity (0.0 to 1.0)"""
        self.setWindowOpacity(value)
        
    def set_click_through(self, enabled):
        """Make widget transparent to mouse events"""
        if enabled:
            self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            self.setWindowFlags(self.windowFlags() | Qt.WindowTransparentForInput)
        else:
            self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowTransparentForInput)
        self.show()
        
    def set_auto_hide(self, enabled):
        """Enable/disable auto-hide feature"""
        self.auto_hide = enabled
        if enabled:
            # Start with widget hidden
            self.hide()
        else:
            self.auto_hide_timer.stop()
            self.show()
            
    def hide_widget(self):
        """Hide widget for auto-hide feature"""
        if self.auto_hide:
            self.hide()
            
    def enterEvent(self, event):
        """Mouse enters widget - show it"""
        if self.auto_hide:
            self.auto_hide_timer.stop()
            self.show()
            
    def leaveEvent(self, event):
        """Mouse leaves widget - hide after delay"""
        if self.auto_hide:
            self.auto_hide_timer.start(2000)  # Hide after 2 seconds

    def close_widget(self):
        """Close the widget"""
        self.hide()
        if hasattr(self, 'on_widget_closed'):
            self.on_widget_closed()
            
    def show_full_app(self):
        """Show the main application"""
        if hasattr(self, 'on_show_full_app'):
            self.on_show_full_app()
            
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # Check if click is near edges for resizing
            rect = self.rect()
            edge_margin = 5
            
            if (rect.width() - event.pos().x() <= edge_margin and 
                rect.height() - event.pos().y() <= edge_margin):
                self.resize_edge = 'bottom_right'
            else:
                self.dragging = True
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
            
    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            self.move(event.globalPos() - self.drag_position)
            event.accept()
        elif self.resize_edge == 'bottom_right':
            new_size = QSize(
                max(self.minimum_size.width(), event.pos().x()),
                max(self.minimum_size.height(), event.pos().y())
            )
            self.resize(new_size)
            
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.dragging = False
        self.resize_edge = None
        
    def update_display(self):
        self.cpu_value.setText(f"{self.system_monitor.cpu_usage}%")
        self.ram_value.setText(f"{self.system_monitor.ram_usage}%")
        self.time_label.setText(self.system_monitor.current_time)