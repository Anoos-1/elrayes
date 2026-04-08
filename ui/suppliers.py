from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QMessageBox, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from services import create_account, get_accounts, get_account_balance
from ui.ledger_view import LedgerViewPage


class SuppliersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("رصيد الموردين")
        self.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()

        # --- Title ---
        title = QLabel("رصيد الموردين")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #c0392b; margin: 8px;")
        layout.addWidget(title)

        # --- Add Supplier ---
        top_layout = QHBoxLayout()
        self.name = QLineEdit()
        self.name.setPlaceholderText("اسم المورد")

        self.region = QLineEdit()
        self.region.setPlaceholderText("المنطقة")

        btn_add = QPushButton("إضافة مورد")
        btn_add.clicked.connect(self.add_supplier)

        top_layout.addWidget(self.name)
        top_layout.addWidget(self.region)
        top_layout.addWidget(btn_add)
        layout.addLayout(top_layout)

        # --- Table ---
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["المورد", "المنطقة", "الرصيد"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #dcdde1;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #c0392b;
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
        self.accounts = get_accounts("supplier")
        self.table.setRowCount(len(self.accounts))

        for i, s in enumerate(self.accounts):
            name_item = QTableWidgetItem(s.name)
            region_item = QTableWidgetItem(s.region if s.region else "")
            balance = get_account_balance(s.id)
            balance_item = QTableWidgetItem(str(balance))
            balance_item.setTextAlignment(Qt.AlignCenter)

            # Color balance
            if balance > 0:
                balance_item.setBackground(QColor("#fdecea"))
            elif balance < 0:
                balance_item.setBackground(QColor("#eafaf1"))

            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, region_item)
            self.table.setItem(i, 2, balance_item)

        self.table.setAlternatingRowColors(True)
        self.table.resizeColumnsToContents()

    def add_supplier(self):
        if not self.name.text().strip():
            QMessageBox.warning(self, "تنبيه", "اسم المورد مطلوب")
            return

        create_account(self.name.text(), "supplier", self.region.text())
        self.name.clear()
        self.region.clear()
        self.load()

    def open_selected_ledger(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "تنبيه", "اختر مورد أولاً")
            return

        acc = self.accounts[row]
        self.w = LedgerViewPage(acc.id, acc.name)
        self.w.show()
