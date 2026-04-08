from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QMessageBox, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from services import create_account, get_accounts, get_account_balance
from ui.ledger_view import LedgerViewPage


class CustomersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("رصيد العملاء")
        self.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()

        title = QLabel("رصيد العملاء")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #2980b9; margin: 8px;")
        layout.addWidget(title)

        # --- Add Customer ---
        top_layout = QHBoxLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText("اسم العميل")

        self.region = QLineEdit()
        self.region.setPlaceholderText("المنطقة")

        btn_add = QPushButton("إضافة عميل")
        btn_add.clicked.connect(self.add_customer)

        top_layout.addWidget(self.name)
        top_layout.addWidget(self.region)
        top_layout.addWidget(btn_add)
        layout.addLayout(top_layout)

        # --- Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["العميل", "المنطقة", "الرصيد"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #dcdde1;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #2980b9;
                color: white;
                padding: 6px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.table)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        btn_details = QPushButton("عرض كشف الحساب")
        btn_details.clicked.connect(self.open_selected_ledger)

        btn_refresh = QPushButton("تحديث")
        btn_refresh.clicked.connect(self.load)

        btn_layout.addWidget(btn_details)
        btn_layout.addWidget(btn_refresh)
        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.load()

    def load(self):
        self.accounts = get_accounts("customer")
        self.table.setRowCount(len(self.accounts))

        for i, c in enumerate(self.accounts):
            name_item = QTableWidgetItem(c.name)
            region_item = QTableWidgetItem(c.region if c.region else "")
            balance = get_account_balance(c.id)
            balance_item = QTableWidgetItem(str(balance))
            balance_item.setTextAlignment(Qt.AlignCenter)

            if balance > 0:
                balance_item.setBackground(QColor("#eafaf1"))
            elif balance < 0:
                balance_item.setBackground(QColor("#fdecea"))

            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, region_item)
            self.table.setItem(i, 2, balance_item)

        self.table.setAlternatingRowColors(True)
        self.table.resizeColumnsToContents()

    def add_customer(self):
        if not self.name.text().strip():
            QMessageBox.warning(self, "تنبيه", "اسم العميل مطلوب")
            return

        create_account(self.name.text(), "customer", self.region.text())
        self.name.clear()
        self.region.clear()
        self.load()

    def open_selected_ledger(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "تنبيه", "اختر عميل أولاً")
            return

        acc = self.accounts[row]
        self.w = LedgerViewPage(acc.id, acc.name)
        self.w.show()
