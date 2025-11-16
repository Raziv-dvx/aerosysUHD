from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QGridLayout)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QTimer, QSize
from PyQt5.QtGui import QPainter, QLinearGradient, QFont

class AnimatedLabel(QLabel):
    def __init__(self, text=""):
        super().__init__(text)
        self._opacity = 1.0
        
    def get_opacity(self):
        return self._opacity
        
    def set_opacity(self, value):
        self._opacity = value
        self.update()
        
    opacity = pyqtProperty(float, get_opacity, set_opacity)

class CircularProgress(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.value = 0
        self.max_value = 100
        self.color = "#3498db"
        self.setFixedSize(60, 60)
        
    def set_value(self, value):
        self.value = max(0, min(value, self.max_value))
        self.update()
        
    def set_color(self, color):
        self.color = color
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background circle
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.gray)
        painter.drawEllipse(5, 5, 50, 50)
        
        # Progress arc
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(self.color))
        
        # Calculate angle
        angle = int(360 * self.value / self.max_value)
        
        # Draw progress arc
        painter.drawPie(5, 5, 50, 50, 90 * 16, -angle * 16)
        
        # Center text
        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self.value}%")

class MainWindow(QWidget):
    def __init__(self, system_monitor, settings):
        super().__init__()
        self.system_monitor = system_monitor
        self.settings = settings
        self.init_ui()
        
    def init_ui(self):
        # Main layout - more compact
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)
        
        # Header with minimal controls
        header_layout = QHBoxLayout()
        
        self.title_label = AnimatedLabel("AeroSys")
        self.title_label.setAlignment(Qt.AlignLeft)
        header_layout.addWidget(self.title_label)
        
        # Minimal control buttons
        controls_layout = QHBoxLayout()
        
        self.minimize_btn = self.create_control_button("−")
        self.minimize_btn.clicked.connect(self.window().showMinimized)
        
        self.close_btn = self.create_control_button("×")
        self.close_btn.clicked.connect(self.window().hide)
        
        controls_layout.addWidget(self.minimize_btn)
        controls_layout.addWidget(self.close_btn)
        
        header_layout.addLayout(controls_layout)
        main_layout.addLayout(header_layout)
        
        # Compact grid for system metrics
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(10)
        grid_layout.setVerticalSpacing(10)
        
        # Create compact metric cards
        self.cpu_card = self.create_compact_card("CPU", "#3498db")
        self.ram_card = self.create_compact_card("RAM", "#9b59b6") 
        self.gpu_card = self.create_compact_card("GPU", "#e74c3c")
        self.net_card = self.create_compact_card("NET", "#2ecc71")
        self.temp_card = self.create_compact_card("TEMP", "#e67e22")
        self.disk_card = self.create_compact_card("DISK", "#f39c12")
        
        # Add to grid - 2 columns
        grid_layout.addWidget(self.cpu_card, 0, 0)
        grid_layout.addWidget(self.ram_card, 0, 1)
        grid_layout.addWidget(self.gpu_card, 1, 0)
        grid_layout.addWidget(self.net_card, 1, 1)
        grid_layout.addWidget(self.temp_card, 2, 0)
        grid_layout.addWidget(self.disk_card, 2, 1)
        
        main_layout.addLayout(grid_layout)
        
        # Time display - minimal
        time_layout = QVBoxLayout()
        
        self.time_label = AnimatedLabel("00:00:00")
        self.time_label.setAlignment(Qt.AlignCenter)
        
        self.date_label = AnimatedLabel("Jan 1, 2024")
        self.date_label.setAlignment(Qt.AlignCenter)
        
        time_layout.addWidget(self.time_label)
        time_layout.addWidget(self.date_label)
        
        main_layout.addLayout(time_layout)
        
        # Minimal footer with essential controls
        footer_layout = QHBoxLayout()
        
        self.widget_btn = self.create_small_button("Widget")
        self.widget_btn.clicked.connect(lambda: self.window().toggle_widget())
        
        self.theme_btn = self.create_small_button("Theme")
        self.theme_btn.clicked.connect(lambda: self.window().toggle_theme())
        
        footer_layout.addWidget(self.widget_btn)
        footer_layout.addWidget(self.theme_btn)
        
        main_layout.addLayout(footer_layout)
        
        self.setLayout(main_layout)
        self.apply_theme("dark")
        
    def create_control_button(self, text):
        btn = QPushButton(text)
        btn.setFixedSize(20, 20)
        btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 30);
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 50);
            }
        """)
        return btn
        
    def create_small_button(self, text):
        btn = QPushButton(text)
        btn.setFixedHeight(25)
        btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 40);
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 60);
            }
        """)
        return btn
        
    def create_compact_card(self, title, color):
        card = QFrame()
        card.setFixedSize(120, 70)  # Fixed compact size
        card.setObjectName("compactCard")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # Title
        title_label = AnimatedLabel(title)
        title_label.setObjectName("compactTitle")
        title_label.setAlignment(Qt.AlignCenter)
        
        # Value
        value_label = AnimatedLabel("0%")
        value_label.setObjectName("compactValue")
        value_label.setAlignment(Qt.AlignCenter)
        
        # Mini progress bar
        progress = QFrame()
        progress.setFixedHeight(4)
        progress.setObjectName("miniProgress")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(progress)
        
        card.setLayout(layout)
        
        # Store references
        card.title = title
        card.value_label = value_label
        card.progress = progress
        card.color = color
        
        return card
        
    def apply_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(25, 25, 35, 230), 
                        stop:1 rgba(15, 15, 25, 230));
                    color: white;
                    border-radius: 12px;
                }
                #compactCard {
                    background: rgba(45, 45, 55, 160);
                    border: 1px solid rgba(255, 255, 255, 20);
                    border-radius: 8px;
                }
                #compactTitle {
                    color: rgba(255, 255, 255, 160);
                    font-size: 10px;
                    font-weight: bold;
                }
                #compactValue {
                    color: white;
                    font-size: 14px;
                    font-weight: bold;
                }
                #miniProgress {
                    background: rgba(255, 255, 255, 20);
                    border-radius: 2px;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(245, 245, 250, 230), 
                        stop:1 rgba(230, 230, 240, 230));
                    color: #333333;
                    border-radius: 12px;
                }
                #compactCard {
                    background: rgba(250, 250, 255, 160);
                    border: 1px solid rgba(0, 0, 0, 20);
                    border-radius: 8px;
                }
                #compactTitle {
                    color: rgba(0, 0, 0, 160);
                    font-size: 10px;
                    font-weight: bold;
                }
                #compactValue {
                    color: #333333;
                    font-size: 14px;
                    font-weight: bold;
                }
                #miniProgress {
                    background: rgba(0, 0, 0, 20);
                    border-radius: 2px;
                }
            """)
            
    def update_display(self):
        # Update all compact cards
        self.update_compact_card(self.cpu_card, self.system_monitor.cpu_usage)
        self.update_compact_card(self.ram_card, self.system_monitor.ram_usage)
        self.update_compact_card(self.gpu_card, self.system_monitor.gpu_usage)
        self.update_compact_card(self.disk_card, self.system_monitor.disk_usage)
        
        # Network special case
        net_up = self.system_monitor.network_upload
        net_down = self.system_monitor.network_download
        self.net_card.value_label.setText(f"{net_up.split()[0]}↑")
        
        # Temperature
        temp = self.system_monitor.temperature
        self.temp_card.value_label.setText(f"{temp}°")
        
        # Time and date
        self.time_label.setText(self.system_monitor.current_time)
        self.date_label.setText(self.system_monitor.current_date)
        
    def update_compact_card(self, card, value):
        card.value_label.setText(f"{value}%")
        # Update mini progress bar
        card.progress.setStyleSheet(f"""
            #miniProgress {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {card.color}, stop:{max(0.01, value/100)} {card.color},
                    stop:{max(0.01, value/100)} rgba(255, 255, 255, 20), stop:1 rgba(255, 255, 255, 20));
                border-radius: 2px;
            }}
        """)