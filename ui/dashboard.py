"""
Dashboard Home Page - Module Selection Interface
Corporate professional dashboard with module cards
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QGridLayout, QFrame, QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor, QIcon
from PySide6.QtCore import QSize
from .style import COLORS


class DashboardCard(QFrame):
    """Professional dashboard card with visual hierarchy and elevation"""
    
    clicked = Signal()
    
    def __init__(self, title, description, icon_char="", color="#457B9D"):
        super().__init__()
        self.color = color
        self.setFixedSize(340, 160)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setLineWidth(0)
        self.setMidLineWidth(0)
        self.setCursor(Qt.PointingHandCursor)
        
        # Professional card with subtle border and light background
        self.setStyleSheet(f"""
            DashboardCard {{
                background-color: #F8F9FA;
                border-radius: 4px;
                border: 1px solid #E0E0E0;
                padding: 0px;
            }}
            DashboardCard:hover {{
                background-color: white;
                border: 2px solid {color};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)
        
        # Title - Bold primary color
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 15, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {color};")
        
        # Description - Secondary text
        if description:
            desc_label = QLabel(description)
            desc_label.setFont(QFont("Segoe UI", 10))
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setStyleSheet("color: #666666;")
            desc_label.setWordWrap(True)
        
        layout.addWidget(title_label)
        if description:
            layout.addWidget(desc_label)
        layout.addStretch()
        
        self.setLayout(layout)
    
    @staticmethod
    def _darken_color(hex_color, factor):
        """Darken a hex color"""
        hex_color = hex_color.lstrip('#')
        r = max(0, int(hex_color[0:2], 16) - factor)
        g = max(0, int(hex_color[2:4], 16) - factor)
        b = max(0, int(hex_color[4:6], 16) - factor)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)


class DashboardPage(QWidget):
    """
    Dashboard Home Page
    Displays all available modules as interactive cards
    """
    
    # Signals for module selection
    module_selected = Signal(str)  # Module name
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("النظام المالي - لوحة التحكم")
        self.resize(1400, 800)
        self.setLayoutDirection(Qt.RightToLeft)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ===== HEADER =====
        header = self._create_header()
        main_layout.addWidget(header)
        
        # ===== CONTENT AREA =====
        content_widget = QWidget()
        content_widget.setStyleSheet(f"background-color: {COLORS['neutral']['page_bg']};")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(16)
        
        # Title Section
        title_section = QVBoxLayout()
        title_section.setSpacing(8)
        
        main_title = QLabel("اختر القسم الذي تريد العمل فيه")
        main_title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        main_title.setStyleSheet(f"color: {COLORS['neutral']['header_bg']};")
        title_section.addWidget(main_title)
        
        subtitle = QLabel("الوصول السريع لجميع وحدات النظام")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet(f"color: {COLORS['neutral']['text_secondary']};")
        title_section.addWidget(subtitle)
        content_layout.addLayout(title_section)
        
        # ===== MODULES GRID (Spacing System: 16px) =====
        modules_grid = QGridLayout()
        modules_grid.setSpacing(16)
        modules_grid.setAlignment(Qt.AlignTop | Qt.AlignRight)
        
        # Define modules: (title, description, icon, module_name)
        modules = [
            ("الموردين", "إدارة بيانات الموردين والعمليات", "📦", "suppliers"),
            ("العملاء", "إدارة العملاء والتحصيل", "👥", "customers"),
            ("البنوك", "إدارة الحسابات البنكية", "🏦", "banks"),
            ("الخزنة", "إدارة النقدية والتحويلات", "💰", "treasury"),
            ("الإدارة", "البيانات الأساسية والإعدادات", "⚙️", "admin"),
        ]
        
        for row, (title, desc, icon, module_name) in enumerate(modules):
            color = COLORS[module_name]['primary']
            card = DashboardCard(title, desc, icon, color)
            card.clicked.connect(lambda m=module_name: self.module_selected.emit(m))
            col = row % 3
            grid_row = row // 3
            modules_grid.addWidget(card, grid_row, col)
        
        content_layout.addLayout(modules_grid)
        content_layout.addStretch()
        
        # Add scroll area
        scroll = QScrollArea()
        scroll.setWidget(content_widget)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {COLORS['neutral']['page_bg']};
            }}
            QScrollBar:vertical {{
                background-color: #E8E8E8;
                width: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: #999999;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: #666666;
            }}
        """)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)
        self.setStyleSheet(f"background-color: {COLORS['neutral']['page_bg']};")

    
    def _create_header(self):
        """Create page header with system title"""
        header = QFrame()
        header.setFrameStyle(QFrame.StyledPanel)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['neutral']['header_bg']};
                border: none;
            }}
        """)
        header.setFixedHeight(100)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(48, 20, 48, 20)
        header_layout.setSpacing(16)
        
        # Logo/Title area
        title = QLabel("النظام المالي")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setStyleSheet("color: white;")
        
        subtitle = QLabel("لوحة التحكم الرئيسية")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.85);")
        
        logo_layout = QVBoxLayout()
        logo_layout.addWidget(title)
        logo_layout.addWidget(subtitle)
        
        header_layout.addLayout(logo_layout)
        header_layout.addStretch()
        
        # Date/Time info (optional)
        from datetime import datetime
        date_label = QLabel(datetime.now().strftime("%d/%m/%Y"))
        date_label.setFont(QFont("Arial", 10))
        date_label.setStyleSheet("color: #95a5a6;")
        header_layout.addWidget(date_label)
        
        return header
