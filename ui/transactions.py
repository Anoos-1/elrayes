from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QDoubleSpinBox,
    QPushButton, QComboBox, QTextEdit, QDialog, QLabel, QMessageBox, QDateEdit, QGroupBox, QGridLayout, QLineEdit
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont
from models.operations import Operation

from services import get_accounts, customer_payment, pay_supplier


class TransactionsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("الدفعات")
        self.resize(600, 400)
        self.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()

        title = QLabel("تسجيل الدفعات")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color:white; background-color:#c0392b; padding:10px; border-radius:6px;")
        layout.addWidget(title)

        # ===== Form =====
        form_group = QGroupBox("بيانات الدفعة")
        form = QGridLayout()

        self.type = QComboBox()
        self.type.addItems(["دفعة مورد", "تحصيل عميل"])
        self.type.currentIndexChanged.connect(self.load_data)

        self.entity = QComboBox()
        self.bank = QComboBox()

        self.amount = QLineEdit()
        self.amount.setPlaceholderText("المبلغ")

        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.record_input = QLineEdit()
        self.record_input.setPlaceholderText("رقم المحضر / الشيك")

        form.addWidget(QLabel("النوع:"), 0, 0)
        form.addWidget(self.type, 0, 1)
        form.addWidget(QLabel("الحساب:"), 1, 0)
        form.addWidget(self.entity, 1, 1)
        form.addWidget(QLabel("البنك:"), 2, 0)
        form.addWidget(self.bank, 2, 1)
        form.addWidget(QLabel("المبلغ:"), 3, 0)
        form.addWidget(self.amount, 3, 1)
        form.addWidget(QLabel("التاريخ:"), 4, 0)
        form.addWidget(self.date_input, 4, 1)
        form.addWidget(QLabel("رقم المحضر:"), 5, 0)
        form.addWidget(self.record_input, 5, 1)

        form_group.setLayout(form)
        layout.addWidget(form_group)

        btn = QPushButton("تنفيذ الدفعة")
        btn.setStyleSheet("background-color:#27ae60; color:white; padding:12px; font-size:14px;")
        btn.clicked.connect(self.execute)
        layout.addWidget(btn)

        self.setLayout(layout)
        self.load_data()

    def load_data(self):
        self.entity.clear()
        self.bank.clear()

        if self.type.currentText() == "تحصيل عميل":
            entities = get_accounts("customer")
        else:
            entities = get_accounts("supplier")

        banks = get_accounts("bank")

        if not entities:
            self.entity.addItem("لا يوجد حسابات", None)
            self.entity.setEnabled(False)
        else:
            self.entity.setEnabled(True)
            for e in entities:
                self.entity.addItem(e.name, e.id)

        if not banks:
            self.bank.addItem("لا يوجد بنوك", None)
            self.bank.setEnabled(False)
        else:
            self.bank.setEnabled(True)
            for b in banks:
                self.bank.addItem(b.name, b.id)

    def execute(self):
        entity_id = self.entity.currentData()
        bank_id = self.bank.currentData()

        if entity_id is None:
            QMessageBox.warning(self, "تنبيه", "اختر حساب صحيح")
            return
        if bank_id is None:
            QMessageBox.warning(self, "تنبيه", "اختر بنك صحيح")
            return

        try:
            amount = float(self.amount.text().strip())
        except (ValueError, TypeError):
            QMessageBox.warning(self, "تنبيه", "أدخل مبلغ صحيح")
            return

        from datetime import date
        qdate = self.date_input.date()
        op_date = date(qdate.year(), qdate.month(), qdate.day())
        record = self.record_input.text().strip()

        if self.type.currentText() == "تحصيل عميل":
            customer_payment(entity_id, bank_id, amount, record, op_date)
        else:
            pay_supplier(entity_id, bank_id, amount, record, op_date)

        QMessageBox.information(self, "تم", "تم تسجيل الدفعة بنجاح")
        self.amount.clear()
        self.record_input.clear()


class CashPaymentDialog(QDialog):
    """Dialog for supplier/customer transactions with discount and damage"""
    
    def __init__(self, party_type="supplier", parent=None):
        super().__init__(parent)
        self.party_type = party_type
        self.setWindowTitle(f"عملية {'مورد' if party_type == 'supplier' else 'عميل'}")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setGeometry(100, 100, 450, 400)
        
        layout = QFormLayout()

        # المبلغ الأساسي
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(999999999.99)
        self.amount_input.setDecimals(2)
        self.amount_input.setSuffix(" ج.م")
        self.amount_input.valueChanged.connect(self.calculate_total)
        layout.addRow("المبلغ الأساسي:", self.amount_input)

        # الخصم (نسبة مئوية)
        self.discount_input = QDoubleSpinBox()
        self.discount_input.setMaximum(100.0)
        self.discount_input.setDecimals(2)
        self.discount_input.setSuffix(" %")
        self.discount_input.valueChanged.connect(self.calculate_total)
        layout.addRow("الخصم من الكارتون (%):", self.discount_input)

        # الهالك (تالف) - نسبة مئوية
        self.damage_input = QDoubleSpinBox()
        self.damage_input.setMaximum(100.0)
        self.damage_input.setDecimals(2)
        self.damage_input.setSuffix(" %")
        self.damage_input.valueChanged.connect(self.calculate_total)
        layout.addRow("الهالك/التالف (%):", self.damage_input)

        # المبلغ بعد الخصم والهالك
        self.final_label = QLabel("0.00 ج.م")
        self.final_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.final_label.setStyleSheet("color: #c0392b;")
        layout.addRow("المبلغ النهائي:", self.final_label)

        # ملاحظات
        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(80)
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

    def calculate_total(self):
        """Calculate final amount after discount and damage"""
        amount = self.amount_input.value()
        discount_percent = self.discount_input.value()
        damage_percent = self.damage_input.value()
        
        # Apply discount first
        after_discount = Operation.calculate_discount(amount, discount_percent)
        
        # Then apply damage
        final_amount = Operation.calculate_with_damage(after_discount, damage_percent)
        
        self.final_label.setText(f"{final_amount:.2f} ج.م")

    def get_data(self):
        amount = self.amount_input.value()
        discount_percent = self.discount_input.value()
        damage_percent = self.damage_input.value()
        
        after_discount = Operation.calculate_discount(amount, discount_percent)
        final_amount = Operation.calculate_with_damage(after_discount, damage_percent)
        
        return {
            'amount': Operation.format_number(amount),
            'discount': Operation.format_number(discount_percent),
            'damage': Operation.format_number(damage_percent),
            'final_amount': final_amount,
            'notes': self.notes_input.toPlainText(),
            'currency': 'ج.م'
        }
