"""
Professional Base Layout Components
Clean, clear, and highly readable components for module pages
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QLineEdit, QComboBox, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from .style import COLORS


class ModuleHeader(QFrame):
    """Professional header for module pages - Blue background, clean design"""
    
    def __init__(self, title, color=None, on_close=None):
        super().__init__()
        self.setFrameStyle(QFrame.NoFrame)
        # Use provided color or fall back to primary blue
        bg_color = color if color else COLORS['primary']['main']
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: none;
                padding: 0px;
            }}
        """)
        self.setFixedHeight(70)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(20)
        
        # Main title - white text, bold, large
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # Return to Dashboard button
        if on_close:
            return_btn = QPushButton("العودة للوحة التحكم")
            return_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
            return_btn.setFixedHeight(44)
            return_btn.setMinimumWidth(160)
            return_btn.setStyleSheet("""
                QPushButton {
                    background-color: #DC2626;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 12px;
                    text-decoration: underline;
                }
                QPushButton:hover {
                    background-color: #B91C1C;
                }
            """)
            return_btn.clicked.connect(on_close)
            layout.addWidget(return_btn)
        
        self.setLayout(layout)


class ActionBar(QFrame):
    """Professional action bar with large buttons for easy navigation"""
    
    def __init__(self, buttons_config):
        """
        Args:
            buttons_config: List of (button_text, clicked_slot, button_type) tuples
                          button_type: 'primary' (blue), 'danger' (red), 'edit' (yellow), 'secondary' (gray)
        """
        super().__init__()
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet("background-color: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 8px;")
        self.setFixedHeight(60)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(12)
        
        # Create buttons
        self.buttons = {}
        for item in buttons_config:
            if len(item) == 3:
                btn_text, btn_slot, btn_type = item
            else:
                btn_text, btn_slot = item
                btn_type = 'primary'
            
            btn = QPushButton(btn_text)
            btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
            btn.setFixedHeight(40)
            btn.setMinimumWidth(120)
            
            # Apply style based on type
            if btn_type == 'danger':
                btn.setObjectName('dangerBtn')
            elif btn_type == 'edit':
                btn.setObjectName('editBtn')
            elif btn_type == 'secondary':
                btn.setObjectName('secondaryBtn')
            # else primary - default styling
            
            btn.clicked.connect(btn_slot)
            layout.addWidget(btn)
            self.buttons[btn_text] = btn
        
        layout.addStretch()
        self.setLayout(layout)


class SectionCard(QFrame):
    """Professional card for grouping content"""
    
    def __init__(self, title=""):
        super().__init__()
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
            }
        """)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(16)
        
        # Optional title
        if title:
            title_label = QLabel(title)
            title_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
            title_label.setStyleSheet("color: #003D7A;")
            self.layout.addWidget(title_label)
            
            # Separator line
            separator = QFrame()
            separator.setFrameShape(QFrame.HLine)
            separator.setStyleSheet("background-color: #E5E7EB;")
            self.layout.addWidget(separator)
        
        self.setLayout(self.layout)


# For backwards compatibility
ActionSection = ActionBar

