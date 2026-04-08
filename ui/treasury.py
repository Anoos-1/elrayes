from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QLabel, QDialog, QComboBox,
    QSpinBox, QDoubleSpinBox, QFormLayout, QMessageBox, QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from datetime import datetime
from models.operations import Operation


class TreasuryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayoutDirection(Qt.RightToLeft)
        self.banks = self.load_banks()  # Load banks from database
        layout = QVBoxLayout()

        # Header
        header = QLabel("رصيد الخزنة - دورة الأموال")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setStyleSheet("""
            background-color: #f39c12;
            color: white;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 10px;
        """)
        layout.addWidget(header)

        # Treasury Balance Display
        balance_layout = QHBoxLayout()
        balance_label = QLabel("الرصيد الحالي:")
        balance_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.balance_value = QLabel("0.00 ج.م")
        self.balance_value.setFont(QFont("Arial", 14, QFont.Bold))
        self.balance_value.setStyleSheet("color: #27ae60;")
        balance_layout.addWidget(balance_label)
        balance_layout.addWidget(self.balance_value)
        balance_layout.addStretch()
        layout.addLayout(balance_layout)

        # Treasury Transactions Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "التاريخ", "النوع", "البنك", "المبلغ (ج.م)", "الرصيد (ج.م)", "ملاحظات", "إجراءات"
        ])
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 100)
        self.table.setColumnWidth(5, 150)
        self.table.setColumnWidth(6, 120)
        self.table.setAlternatingRowColors(True)
        self.table.setRowHeight(0, 30)
        layout.addWidget(self.table)

        # Action Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        btn_withdrawal = QPushButton("سحب من البنك 🏦➜💰")
        btn_withdrawal.setMinimumHeight(40)
        btn_withdrawal.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        btn_withdrawal.clicked.connect(lambda: self.open_transaction_dialog("سحب من البنك"))
        buttons_layout.addWidget(btn_withdrawal)

        btn_deposit = QPushButton("إيداع في البنك 💰➜🏦")
        btn_deposit.setMinimumHeight(40)
        btn_deposit.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #229954; }
        """)
        btn_deposit.clicked.connect(lambda: self.open_transaction_dialog("إيداع في البنك"))
        buttons_layout.addWidget(btn_deposit)

        btn_payment = QPushButton("دفع نقدي 💵")
        btn_payment.setMinimumHeight(40)
        btn_payment.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #c0392b; }
        """)
        btn_payment.clicked.connect(lambda: self.open_transaction_dialog("دفع نقدي"))
        buttons_layout.addWidget(btn_payment)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def load_banks(self):
        """Load banks from database"""
        # TODO: Load from database
        return [
            "البنك الأهلي",
            "بنك الراجحي",
            "بنك الرياض",
            "بنك ساب",
            "بنك الإنماء",
            "بنك الخليج"
        ]

    def open_transaction_dialog(self, trans_type):
        dialog = CashTransactionDialog(trans_type, self.banks, self)
        if dialog.exec():
            self.add_transaction(dialog.get_data())

    def add_transaction(self, data):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # التاريخ
        self.table.setItem(row, 0, QTableWidgetItem(data['date']))
        
        # النوع
        type_item = QTableWidgetItem(data['type_ar'])
        self.table.setItem(row, 1, type_item)

        # البنك
        self.table.setItem(row, 2, QTableWidgetItem(data['bank']))

        # المبلغ (قرّب الأرقام)
        amount = Operation.format_number(data['amount'])
        amount_item = QTableWidgetItem(f"{amount:.2f}")
        amount_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 3, amount_item)

        # الرصيد (قرّب الأرقام)
        balance = Operation.format_number(data['balance'])
        balance_item = QTableWidgetItem(f"{balance:.2f}")
        balance_item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(row, 4, balance_item)

        # ملاحظات
        self.table.setItem(row, 5, QTableWidgetItem(data['notes']))

        # إجراءات (تعديل / حذف)
        actions_widget = QWidget()
        actions_layout = QHBoxLayout()
        actions_layout.setContentsMargins(2, 2, 2, 2)

        btn_edit = QPushButton("تعديل ✏️")
        btn_edit.setMaximumWidth(70)
        btn_edit.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #e67e22; }
        """)
        btn_edit.clicked.connect(lambda: self.edit_transaction(row))

        btn_delete = QPushButton("حذف ❌")
        btn_delete.setMaximumWidth(70)
        btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #a93226; }
        """)
        btn_delete.clicked.connect(lambda: self.delete_transaction(row))

        actions_layout.addWidget(btn_edit)
        actions_layout.addWidget(btn_delete)
        actions_layout.addStretch()
        actions_widget.setLayout(actions_layout)

        self.table.setCellWidget(row, 6, actions_widget)
        self.update_balance()

    def edit_transaction(self, row):
        # Get current data
        dialog = CashTransactionDialog("تعديل", self.banks, self, row_data={
            'date': self.table.item(row, 0).text(),
            'bank': self.table.item(row, 2).text(),
            'amount': self.table.item(row, 3).text(),
            'notes': self.table.item(row, 5).text(),
        })
        if dialog.exec():
            data = dialog.get_data()
            self.table.setItem(row, 0, QTableWidgetItem(data['date']))
            self.table.setItem(row, 2, QTableWidgetItem(data['bank']))
            amount = Operation.format_number(data['amount'])
            self.table.setItem(row, 3, QTableWidgetItem(f"{amount:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(data['notes']))
            self.update_balance()

    def delete_transaction(self, row):
        reply = QMessageBox.question(self, "تأكيد الحذف", 
                                      "هل تريد حذف هذه العملية؟",
                                      QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.table.removeRow(row)
            self.update_balance()

    def update_balance(self):
        if self.table.rowCount() == 0:
            self.balance_value.setText("0.00 ج.م")
            return
        
        last_balance = self.table.item(self.table.rowCount() - 1, 4).text()
        balance = Operation.format_number(last_balance)
        self.balance_value.setText(f"{balance:.2f} ج.م")
        
        # Change color based on balance
        if balance >= 0:
            self.balance_value.setStyleSheet("color: #27ae60;")
        else:
            self.balance_value.setStyleSheet("color: #c0392b;")

    def load(self):
        # Load treasury data from database
        self.table.setRowCount(0)
        # TODO: Load transactions from database


class CashTransactionDialog(QDialog):
    def __init__(self, trans_type, banks_list, parent=None, row_data=None):
        super().__init__(parent)
        self.trans_type = trans_type
        self.row_data = row_data or {}
        self.setWindowTitle("عملية خزنة")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setGeometry(100, 100, 400, 350)
        
        layout = QFormLayout()

        # التاريخ
        self.date_input = QSpinBox()
        self.date_input.setValue(int(datetime.now().strftime("%Y%m%d")))
        layout.addRow("التاريخ (YYYYMMDD):", self.date_input)

        # اختيار البنك (مهم للدفع والسحب والإيداع)
        bank_label = QLabel("البنك:")
        self.bank_combo = QComboBox()
        self.bank_combo.addItems(banks_list)
        if row_data and 'bank' in row_data:
            self.bank_combo.setCurrentText(row_data['bank'])
        layout.addRow(bank_label, self.bank_combo)

        # المبلغ
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(999999999.99)
        self.amount_input.setDecimals(2)
        self.amount_input.setSuffix(" ج.م")
        if row_data and 'amount' in row_data:
            self.amount_input.setValue(float(row_data['amount']))
        layout.addRow("المبلغ:", self.amount_input)

        # الخصم (نسبة مئوية)
        self.discount_input = QDoubleSpinBox()
        self.discount_input.setMaximum(100.0)
        self.discount_input.setDecimals(2)
        self.discount_input.setSuffix(" %")
        layout.addRow("الخصم (%):", self.discount_input)

        # ملاحظات
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
        if row_data and 'notes' in row_data:
            self.notes_input.setPlainText(row_data['notes'])
        layout.addRow("ملاحظات:", self.notes_input)

        # أزرار
        buttons_layout = QHBoxLayout()
        btn_save = QPushButton("حفظ ✓")
        btn_save.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #229954; }
        """)
        btn_save.clicked.connect(self.accept)

        btn_cancel = QPushButton("إلغاء")
        btn_cancel.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #566573; }
        """)
        btn_cancel.clicked.connect(self.reject)

        buttons_layout.addWidget(btn_save)
        buttons_layout.addWidget(btn_cancel)
        layout.addRow(buttons_layout)

        self.setLayout(layout)

    def get_data(self):
        # حساب المبلغ بعد الخصم
        amount = self.amount_input.value()
        discount_percent = self.discount_input.value()
        final_amount = Operation.calculate_discount(amount, discount_percent)
        
        return {
            'date': str(self.date_input.value()),
            'type_ar': self.trans_type,
            'bank': self.bank_combo.currentText(),
            'amount': final_amount,
            'discount': Operation.format_number(discount_percent),
            'balance': final_amount,
            'notes': self.notes_input.toPlainText()
        }