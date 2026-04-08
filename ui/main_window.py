from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTabWidget, QLabel, QGroupBox, QGridLayout, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.suppliers import SuppliersPage
from ui.customers import CustomersPage
from ui.bank import BankPage
from ui.transactions import TransactionsPage
from ui.master_data import MasterDataPage
from ui.operation_entry import OperationEntryPage
from ui.treasury import TreasuryPage  # Add this import


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("النظام المالي - رصيد الموردين والعملاء")
        self.resize(1400, 800)
        self.setLayoutDirection(Qt.RightToLeft)

        main_layout = QVBoxLayout()

        # ===== Header =====
        header = QLabel("النظام المالي")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 24, QFont.Bold))
        header.setStyleSheet("""
            background-color: #c0392b;
            color: white;
            padding: 16px;
            border-radius: 8px;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(header)

        # ===== Sections Grid =====
        sections_layout = QHBoxLayout()

        # ---------- Section 1: الموردين ----------
        supplier_section = self._create_section(
            title="الموردين",
            color="#e74c3c",
            icon="📦",
            buttons=[
                ("رصيد الموردين", self.show_suppliers),
                ("تسجيل عملية مورد", lambda: self.open_entry("supplier")),
                ("دفعة مورد", lambda: self.open_transactions("supplier")),
            ]
        )
        sections_layout.addWidget(supplier_section)

        # ---------- Section 2: العملاء ----------
        customer_section = self._create_section(
            title="العملاء",
            color="#2980b9",
            icon="👥",
            buttons=[
                ("رصيد العملاء", self.show_customers),
                ("تسجيل عملية عميل", lambda: self.open_entry("customer")),
                ("تحصيل عميل", lambda: self.open_transactions("customer")),
            ]
        )
        sections_layout.addWidget(customer_section)

        # ---------- Section 3: البنوك ----------
        bank_section = self._create_section(
            title="البنوك",
            color="#27ae60",
            icon="🏦",
            buttons=[
                ("حسابات البنوك", self.open_banks),
                ("الدفعات", lambda: self.open_transactions("bank")),
            ]
        )
        sections_layout.addWidget(bank_section)

        # ---------- Section 4: الخزنة (Treasury/Cash) ----------
        treasury_section = self._create_section(
            title="الخزنة",
            color="#f39c12",
            icon="💰",
            buttons=[
                ("رصيد الخزنة", self.open_treasury),
                ("سحب من البنك", lambda: self.open_cash_transaction("withdrawal")),
                ("إيداع في البنك", lambda: self.open_cash_transaction("deposit")),
                ("دفع نقدي", lambda: self.open_cash_transaction("payment")),
            ]
        )
        sections_layout.addWidget(treasury_section)

        # ---------- Section 5: الإدارة ----------
        admin_section = self._create_section(
            title="الإدارة",
            color="#8e44ad",
            icon="⚙️",
            buttons=[
                ("البيانات الأساسية", self.open_master_data),
            ]
        )
        sections_layout.addWidget(admin_section)

        main_layout.addLayout(sections_layout)

        # ===== Separator =====
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #bdc3c7; margin: 6px 0;")
        main_layout.addWidget(line)

        # ===== Tab Widget (like Excel bottom tabs) =====
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.South)
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
            }
            QTabBar::tab {
                background: #ecf0f1;
                color: #2c3e50;
                padding: 8px 20px;
                margin-right: 2px;
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #bdc3c7;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            QTabBar::tab:selected {
                background: white;
                color: #c0392b;
                border-bottom: 3px solid #c0392b;
            }
        """)

        self.tab_suppliers = SuppliersPage()
        self.tab_customers = CustomersPage()
        self.tab_treasury = TreasuryPage()
        self.tabs.addTab(self.tab_suppliers, "📦 الموردين")
        self.tabs.addTab(self.tab_customers, "👥 العملاء")
        self.tabs.addTab(self.tab_treasury, "💰 الخزنة")

        main_layout.addWidget(self.tabs)

        self.setLayout(main_layout)

    # ===================================================
    # Helper: Create a styled section card
    # ===================================================
    def _create_section(self, title, color, icon, buttons):
        group = QGroupBox()
        group.setStyleSheet(f"""
            QGroupBox {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 12px;
                margin-top: 0px;
                padding: 10px;
            }}
        """)

        layout = QVBoxLayout()

        # Section header
        header = QLabel(f"{icon}  {title}")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setStyleSheet(f"""
            background-color: {color};
            color: white;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 8px;
        """)
        layout.addWidget(header)

        # Section buttons
        for text, callback in buttons:
            btn = QPushButton(text)
            btn.setMinimumHeight(45)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: white;
                    color: {color};
                    border: 2px solid {color};
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    padding: 8px;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    color: white;
                }}
                QPushButton:pressed {{
                    background-color: {color};
                    color: #ecf0f1;
                }}
            """)
            btn.clicked.connect(callback)
            layout.addWidget(btn)

        layout.addStretch()
        group.setLayout(layout)
        return group

    # ===================================================
    # Actions
    # ===================================================
    def show_suppliers(self):
        self.tabs.setCurrentWidget(self.tab_suppliers)
        self.tab_suppliers.load()

    def show_customers(self):
        self.tabs.setCurrentWidget(self.tab_customers)
        self.tab_customers.load()

    def open_banks(self):
        self.w = BankPage()
        self.w.show()

    def open_treasury(self):
        self.tabs.setCurrentWidget(self.tab_treasury)
        self.tab_treasury.load()

    def open_entry(self, acc_type):
        self.w = OperationEntryPage(acc_type)
        self.w.show()

    def open_transactions(self, preset=None):
        self.w = TransactionsPage()
        if preset == "supplier":
            self.w.type.setCurrentText("دفعة مورد")
        elif preset == "customer":
            self.w.type.setCurrentText("تحصيل عميل")
        elif preset == "bank":
            self.w.type.setCurrentText("دفعة بنكية")
        self.w.show()

    def open_cash_transaction(self, trans_type):
        self.w = TransactionsPage()
        if trans_type == "withdrawal":
            self.w.type.setCurrentText("سحب من البنك")
        elif trans_type == "deposit":
            self.w.type.setCurrentText("إيداع في البنك")
        elif trans_type == "payment":
            self.w.type.setCurrentText("دفع نقدي")
        self.w.show()

    def open_master_data(self):
        self.w = MasterDataPage()
        self.w.show()
