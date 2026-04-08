"""
Main Application Window - Navigation Hub
Manages dashboard and module page switching
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QStackedWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.dashboard import DashboardPage
from ui.suppliers import SuppliersPage
from ui.customers import CustomersPage
from ui.bank import BankPage
from ui.treasury import TreasuryPage
from ui.master_data import MasterDataPage


class ModuleNavigationBar(QFrame):
    """Top navigation bar with back button and module info"""
    
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet("""
            ModuleNavigationBar {
                background-color: white;
                border-bottom: 1px solid #ecf0f1;
                padding: 12px;
            }
        """)
        self.setFixedHeight(60)
        self.setVisible(False)  # Hidden by default
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(15)
        
        # Back button
        self.back_btn = QPushButton("← العودة إلى لوحة التحكم")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #ecf0f1;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                color: #2c3e50;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d5dbdb;
            }
        """)
        layout.addWidget(self.back_btn)
        
        # Module name (will be updated)
        self.module_name = QLabel()
        self.module_name.setFont(QFont("Arial", 12, QFont.Bold))
        self.module_name.setStyleSheet("color: #2c3e50;")
        layout.addWidget(self.module_name)
        
        layout.addStretch()
        self.setLayout(layout)


class MainWindow(QWidget):
    """
    Main Application Window
    Contains dashboard and module pages
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("النظام المالي - Financial Management System")
        self.resize(1400, 850)
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet("background-color: #f8f9fa;")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # ===== NAVIGATION BAR =====
        self.nav_bar = ModuleNavigationBar()
        main_layout.addWidget(self.nav_bar)
        
        # ===== STACKED WIDGET (Pages Container) =====
        self.stacked_widget = QStackedWidget()
        
        # Create all pages
        self.pages = {}
        self._create_pages()
        
        main_layout.addWidget(self.stacked_widget)
        
        # Connect dashboard signals
        dashboard = self.pages['dashboard']
        dashboard.module_selected.connect(self._on_module_selected)
        
        # Connect back button
        self.nav_bar.back_btn.clicked.connect(self._go_to_dashboard)
        
        self.setLayout(main_layout)
        
        # Show dashboard initially
        self._go_to_dashboard()
    
    def _create_pages(self):
        """Create all application pages"""
        pages_config = [
            ('dashboard', DashboardPage()),
            ('suppliers', SuppliersPage()),
            ('customers', CustomersPage()),
            ('banks', BankPage()),
            ('treasury', TreasuryPage()),
            ('admin', MasterDataPage()),
        ]
        
        for page_name, page_widget in pages_config:
            self.pages[page_name] = page_widget
            self.stacked_widget.addWidget(page_widget)
    
    def _on_module_selected(self, module_name):
        """Handle module card selection"""
        module_map = {
            'suppliers': ('suppliers', 'الموردين'),
            'customers': ('customers', 'العملاء'),
            'banks': ('banks', 'البنوك'),
            'treasury': ('treasury', 'الخزنة'),
            'admin': ('admin', 'الإدارة'),
        }
        
        if module_name in module_map:
            page_key, module_title = module_map[module_name]
            self.nav_bar.module_name.setText(module_title)
            self.stacked_widget.setCurrentWidget(self.pages[page_key])
            self.nav_bar.setVisible(True)
    
    def _go_to_dashboard(self):
        """Return to dashboard"""
        self.stacked_widget.setCurrentWidget(self.pages['dashboard'])
        self.nav_bar.setVisible(False)
