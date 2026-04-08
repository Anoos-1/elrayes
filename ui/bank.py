from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt
from datetime import datetime


class BankPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("حسابات البنوك")
        self.resize(1000, 600)

        main_layout = QVBoxLayout()

        # ===== Title =====
        title = QLabel("كشف حساب البنك")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin: 10px;
        """)
        main_layout.addWidget(title)

        # ===== Table =====
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "التاريخ", "رقم الشيك", "البيان",
            "صادر دائن -", "وارد مدين +", "الرصيد", "ملاحظات"
        ])

        self.table.setAlternatingRowColors(True)
        self.table.resizeColumnsToContents()
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #dcdde1;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 6px;
                font-weight: bold;
            }
        """)

        main_layout.addWidget(self.table)

        # ===== Buttons =====
        btn_layout = QHBoxLayout()

        self.btn_add_debit = QPushButton("إضافة وارد")
        self.btn_add_credit = QPushButton("إضافة صادر")

        for btn, color in [
            (self.btn_add_debit, "#27ae60"),
            (self.btn_add_credit, "#c0392b")
        ]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    font-size: 16px;
                    border-radius: 8px;
                }}
                QPushButton:hover {{
                    background-color: #2c3e50;
                }}
            """)
            btn_layout.addWidget(btn)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

        # Initial Balance Row
        self.add_opening_balance()

        # Connections
        self.btn_add_debit.clicked.connect(self.add_debit)
        self.btn_add_credit.clicked.connect(self.add_credit)

    # ---------- Opening Balance ----------
    def add_opening_balance(self):
        self.table.insertRow(0)
        self.table.setItem(0, 0, QTableWidgetItem("رصيد أول المدة"))
        self.table.setItem(0, 5, QTableWidgetItem("0"))

    # ---------- Add Debit (وارد) ----------
    def add_debit(self):
        self.add_row(debit=1000, credit=0, description="وارد")

    # ---------- Add Credit (صادر) ----------
    def add_credit(self):
        self.add_row(debit=0, credit=500, description="صادر")

    # ---------- Core Logic ----------
    def add_row(self, debit, credit, description):
        row = self.table.rowCount()
        self.table.insertRow(row)

        date_str = datetime.now().strftime("%Y-%m-%d")

        self.table.setItem(row, 0, QTableWidgetItem(date_str))
        self.table.setItem(row, 2, QTableWidgetItem(description))
        self.table.setItem(row, 3, QTableWidgetItem(str(credit)))
        self.table.setItem(row, 4, QTableWidgetItem(str(debit)))

        # Calculate running balance
        prev_balance = float(self.table.item(row - 1, 5).text())
        new_balance = prev_balance + debit - credit
        self.table.setItem(row, 5, QTableWidgetItem(str(new_balance)))

        self.table.resizeColumnsToContents()
