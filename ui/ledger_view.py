from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from services import get_operations, get_account_balance


class LedgerViewPage(QWidget):
    def __init__(self, account_id, account_name):
        super().__init__()

        self.account_id = account_id
        self.account_name = account_name

        self.setWindowTitle(f"كشف حساب - {account_name}")
        self.resize(1300, 650)
        self.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()

        # ===== Title =====
        title = QLabel(f"كشف حساب: {account_name}")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("""
            color: white;
            background-color: #c0392b;
            padding: 10px;
            border-radius: 6px;
            margin: 6px;
        """)
        layout.addWidget(title)

        # ===== Table — matching Excel columns =====
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "اسم العميل",       # A - Customer Name
            "المنطقة",          # B - Region
            "سعر الطن",        # C - Price per ton
            "النوع",            # D - Type
            "الوزن قبل الخصم",  # E - Gross Weight
            "الوزن بعد الخصم",  # F - Net Weight
            "حساب الموردين",    # G - Supplier Amount
            "الدفعات",          # H - Payments
            "الرصيد",           # I - Balance
            "التاريخ",          # J - Date
            "رقم المحضر",      # K - Record Number
        ])

        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #bdc3c7;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #c0392b;
                color: white;
                padding: 8px;
                font-weight: bold;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 4px;
            }
        """)

        layout.addWidget(self.table)

        # ===== Balance Summary =====
        self.balance_label = QLabel("")
        self.balance_label.setAlignment(Qt.AlignCenter)
        self.balance_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.balance_label.setStyleSheet("margin: 8px; padding: 8px;")
        layout.addWidget(self.balance_label)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        operations = get_operations(self.account_id)

        total_rows = len(operations) + 1  # +1 for opening balance row
        self.table.setRowCount(total_rows)

        # ===== Row 0: رصيد أول المدة =====
        opening_item = QTableWidgetItem("رصيد أول المدة")
        opening_item.setTextAlignment(Qt.AlignCenter)
        opening_item.setFont(QFont("Arial", 12, QFont.Bold))
        opening_item.setBackground(QColor("#f9e79f"))
        self.table.setItem(0, 0, opening_item)

        # Empty cells for row 0
        for col in range(1, 11):
            empty = QTableWidgetItem("")
            empty.setBackground(QColor("#f9e79f"))
            self.table.setItem(0, col, empty)

        # ===== Operation Rows =====
        running_balance = 0

        for i, op in enumerate(operations, start=1):
            running_balance += (op.supplier_amount - op.payment)

            row_data = [
                self.account_name,                                       # اسم العميل
                "",                                                       # المنطقة
                str(op.price_per_ton) if op.price_per_ton else "",       # سعر الطن
                op.item_type if op.item_type else "",                    # النوع
                str(op.gross_weight) if op.gross_weight else "",         # قبل الخصم
                str(op.net_weight) if op.net_weight else "",             # بعد الخصم
                str(op.supplier_amount) if op.supplier_amount else "0",  # حساب الموردين
                str(op.payment) if op.payment else "0",                  # الدفعات
                str(running_balance),                                     # الرصيد
                str(op.date) if op.date else "",                         # التاريخ
                op.record_number if op.record_number else "",            # رقم المحضر
            ]

            for c, val in enumerate(row_data):
                cell = QTableWidgetItem(val)
                cell.setTextAlignment(Qt.AlignCenter)

                # Color: حساب الموردين (green if > 0)
                if c == 6:
                    try:
                        v = float(val)
                        if v > 0:
                            cell.setBackground(QColor("#d5f5e3"))
                    except ValueError:
                        pass

                # Color: الدفعات (light blue if > 0)
                if c == 7:
                    try:
                        v = float(val)
                        if v > 0:
                            cell.setBackground(QColor("#d6eaf8"))
                    except ValueError:
                        pass

                # Color: الرصيد
                if c == 8:
                    try:
                        v = float(val)
                        if v > 0:
                            cell.setBackground(QColor("#fdecea"))
                            cell.setForeground(QColor("#c0392b"))
                        elif v < 0:
                            cell.setBackground(QColor("#eafaf1"))
                            cell.setForeground(QColor("#27ae60"))
                    except ValueError:
                        pass

                self.table.setItem(i, c, cell)

        # Set balance in opening row
        bal_item = QTableWidgetItem(str(running_balance))
        bal_item.setTextAlignment(Qt.AlignCenter)
        bal_item.setFont(QFont("Arial", 12, QFont.Bold))
        bal_item.setBackground(QColor("#f9e79f"))
        self.table.setItem(0, 8, bal_item)

        self.table.resizeColumnsToContents()

        # ===== Balance Summary =====
        if running_balance > 0:
            self.balance_label.setText(f"الرصيد الحالي: {running_balance} (مدين)")
            self.balance_label.setStyleSheet("color: #c0392b; font-size: 16px; font-weight: bold;")
        elif running_balance < 0:
            self.balance_label.setText(f"الرصيد الحالي: {running_balance} (دائن)")
            self.balance_label.setStyleSheet("color: #27ae60; font-size: 16px; font-weight: bold;")
        else:
            self.balance_label.setText("الرصيد الحالي: 0 (متزن)")
            self.balance_label.setStyleSheet("color: #2c3e50; font-size: 16px; font-weight: bold;")
