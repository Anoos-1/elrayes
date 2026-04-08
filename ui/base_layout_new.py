"""
Professional Base Layout Components
Clean, clear, and highly readable components for module pages
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QLineEdit, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from .style import COLORS


class ModuleHeader(QFrame):
    """Professional header for module pages - Blue background, clean design"""
    
    def __init__(self, title, on_close=None):
        super().__init__()
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['primary']['main']};
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
        self.setStyleSheet("background-color: #F9FAFB; border: 1px solid #E5E7EB;")
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
    """Professional card for grouping form fields"""
    
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
            separator.setStyleSheet("color: #E5E7EB;")
            self.layout.addWidget(separator)
        
        self.setLayout(self.layout)
    
    def add_field(self, label_text, widget):
        """Add a labeled field to the card"""
        row_layout = QHBoxLayout()
        
        label = QLabel(label_text)
        label.setFont(QFont("Segoe UI", 11))
        label.setStyleSheet("color: #374151; font-weight: 600;")
        label.setMinimumWidth(150)
        
        row_layout.addWidget(label)
        row_layout.addWidget(widget)
        
        self.layout.addLayout(row_layout)
    
    def add_fields_row(self, fields):
        """Add multiple fields in a horizontal row
        fields: List of (label_text, widget) tuples
        """
        row_layout = QHBoxLayout()
        row_layout.setSpacing(12)
        
        for label_text, widget in fields:
            label = QLabel(label_text)
            label.setFont(QFont("Segoe UI", 11))
            label.setStyleSheet("color: #374151; font-weight: 600;")
            label.setMinimumWidth(140)
            
            col_layout = QVBoxLayout()
            col_layout.setSpacing(4)
            col_layout.addWidget(label)
            col_layout.addWidget(widget)
            row_layout.addLayout(col_layout)
        
        self.layout.addLayout(row_layout)


class DataTable(QFrame):
    """Professional data table frame"""
    
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
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Title bar
        if title:
            title_bar = QFrame()
            title_bar.setStyleSheet("""
                QFrame {
                    background-color: #F9FAFB;
                    border-bottom: 1px solid #E5E7EB;
                    border-radius: 8px 8px 0px 0px;
                }
            """)
            title_bar.setFixedHeight(50)
            
            title_layout = QHBoxLayout(title_bar)
            title_layout.setContentsMargins(20, 12, 20, 12)
            
            title_label = QLabel(title)
            title_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
            title_label.setStyleSheet("color: #003D7A;")
            
            title_layout.addWidget(title_label)
            layout.addWidget(title_bar)
        
        # Content area
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.content_layout)
        
        self.setLayout(layout)
    
    def set_table(self, table_widget):
        """Set the table widget"""
        table_widget.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF;
                gridline-color: #E5E7EB;
                border: none;
                border-radius: 0px;
            }
            QTableWidget::item {
                padding: 12px;
            }
            QHeaderView::section {
                background-color: #0052CC;
                color: #FFFFFF;
                padding: 12px;
                font-weight: bold;
                border: none;
            }
        """)
        self.content_layout.addWidget(table_widget)
