from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem,
    QMessageBox, QComboBox, QGroupBox, QGridLayout, QDateEdit
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

from services import get_accounts, add_operation, get_item_types


class OperationEntryPage(QWidget):
    def __init__(self, acc_type="supplier"):
        super().__init__()

        self.acc_type = acc_type
        self.setWindowTitle("تسجيل العمليات")
        self.resize(1200, 750)
        self.setLayoutDirection(Qt.RightToLeft)

        main_layout = QVBoxLayout()

        # ===== Title =====
        title_text = "تسجيل عمليات المورد" if acc_type == "supplier" else "تسجيل عمليات العميل"
        title = QLabel(title_text)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color:white; background-color:#c0392b; padding:10px; border-radius:6px;")
        main_layout.addWidget(title)

        # ===== Account Selection =====
        acc_group = QGroupBox("اختيار الحساب")
        acc_layout = QHBoxLayout()

        self.account_combo = QComboBox()
        self.load_accounts()

        acc_layout.addWidget(QLabel("الحساب:"))
        acc_layout.addWidget(self.account_combo)
        acc_group.setLayout(acc_layout)
        main_layout.addWidget(acc_group)

        # ===== Input Fields — Matching Excel =====
        input_group = QGroupBox("بيانات العملية")
        input_grid = QGridLayout()

        # Row 0
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.record_input = QLineEdit()
        self.record_input.setPlaceholderText("رقم المحضر")

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("البيان / الوصف")

        input_grid.addWidget(QLabel("التاريخ:"), 0, 0)
        input_grid.addWidget(self.date_input, 0, 1)
        input_grid.addWidget(QLabel("رقم المحضر:"), 0, 2)
        input_grid.addWidget(self.record_input, 0, 3)
        input_grid.addWidget(QLabel("الوصف:"), 0, 4)
        input_grid.addWidget(self.desc_input, 0, 5)

        # Row 1 — Item type & price
        self.type_combo = QComboBox()
        self.type_combo.setEditable(True)
        self.load_item_types()

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("سعر الطن")

        input_grid.addWidget(QLabel("النوع:"), 1, 0)
        input_grid.addWidget(self.type_combo, 1, 1)
        input_grid.addWidget(QLabel("سعر الطن:"), 1, 2)
        input_grid.addWidget(self.price_input, 1, 3)

        # Row 2 — Weight fields
        self.gross_input = QLineEdit()
        self.gross_input.setPlaceholderText("الوزن قبل الخصم")

        self.deduction_input = QLineEdit()
        self.deduction_input.setPlaceholderText("نسبة الخصم %")

        self.net_input = QLineEdit()
        self.net_input.setPlaceholderText("الوزن بعد الخصم")
        self.net_input.setReadOnly(True)
        self.net_input.setStyleSheet("background-color: #eafaf1; font-weight: bold;")

        input_grid.addWidget(QLabel("قبل الخصم:"), 2, 0)
        input_grid.addWidget(self.gross_input, 2, 1)
        input_grid.addWidget(QLabel("نسبة الخصم %:"), 2, 2)
        input_grid.addWidget(self.deduction_input, 2, 3)
        input_grid.addWidget(QLabel("بعد الخصم:"), 2, 4)
        input_grid.addWidget(self.net_input, 2, 5)

        # Row 3 — Amount fields
        self.supplier_amount_input = QLineEdit()
        self.supplier_amount_input.setPlaceholderText("حساب الموردين")
        self.supplier_amount_input.setReadOnly(True)
        self.supplier_amount_input.setStyleSheet("background-color: #d5f5e3; font-weight: bold;")

        self.payment_input = QLineEdit()
        self.payment_input.setPlaceholderText("الدفعات")
        self.payment_input.setText("0")

        input_grid.addWidget(QLabel("حساب الموردين:"), 3, 0)
        input_grid.addWidget(self.supplier_amount_input, 3, 1)
        input_grid.addWidget(QLabel("الدفعات:"), 3, 2)
        input_grid.addWidget(self.payment_input, 3, 3)

        input_group.setLayout(input_grid)
        main_layout.addWidget(input_group)

        # Auto-calculations
        self.gross_input.textChanged.connect(self.calc_net_weight)
        self.deduction_input.textChanged.connect(self.calc_net_weight)
        self.price_input.textChanged.connect(self.calc_supplier_amount)

        # ===== Add Button =====
        add_btn = QPushButton("إضافة للجدول")
        add_btn.setStyleSheet("background-color:#3498db; color:white; padding:10px; font-size:14px;")
        add_btn.clicked.connect(self.add_row)
        main_layout.addWidget(add_btn)

        # ===== Table =====
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "التاريخ", "رقم المحضر", "الوصف", "النوع", "سعر الطن",
            "قبل الخصم", "الخصم", "بعد الخصم", "حساب الموردين", "الدفعات"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QHeaderView::section {
                background-color: #c0392b;
                color: white;
                padding: 6px;
                font-weight: bold;
            }
        """)
        main_layout.addWidget(self.table)

        # ===== Save Button =====
        save_btn = QPushButton("حفظ الكل")
        save_btn.setObjectName("saveBtn")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color:#27ae60; color:white;
                font-size:16px; padding:12px; border-radius:6px;
            }
        """)
        save_btn.clicked.connect(self.save_operations)
        main_layout.addWidget(save_btn)

        self.setLayout(main_layout)

    def load_accounts(self):
        self.account_combo.clear()
        accounts = get_accounts(self.acc_type)
        for acc in accounts:
            self.account_combo.addItem(acc.name, acc.id)

    def load_item_types(self):
        self.type_combo.clear()
        types = get_item_types()
        for t in types:
            self.type_combo.addItem(t.name)

    def calc_net_weight(self):
        try:
            gross = float(self.gross_input.text()) if self.gross_input.text() else 0
            # الخصم الآن نسبة مئوية، لا رقم ثابت
            deduction_percent = float(self.deduction_input.text()) if self.deduction_input.text() else 0
            # حساب الوزن بعد الخصم: gross - (gross * deduction_percent / 100)
            deduction_amount = (gross * deduction_percent) / 100
            net = max(gross - deduction_amount, 0)
            self.net_input.setText(str(round(net, 2)))
            self.calc_supplier_amount()
        except ValueError:
            self.net_input.setText("")

    def calc_supplier_amount(self):
        try:
            net = float(self.net_input.text()) if self.net_input.text() else 0
            price = float(self.price_input.text()) if self.price_input.text() else 0
            amount = net * price
            self.supplier_amount_input.setText(str(amount))
        except ValueError:
            self.supplier_amount_input.setText("")

    def add_row(self):
        desc = self.desc_input.text().strip()
        gross = self.gross_input.text().strip()
        price = self.price_input.text().strip()

        if not gross and not self.payment_input.text().strip():
            QMessageBox.warning(self, "تنبيه", "أدخل الوزن أو الدفعة")
            return

        op_date = self.date_input.date().toString("yyyy-MM-dd")
        record = self.record_input.text().strip()
        item_type = self.type_combo.currentText()
        deduction = self.deduction_input.text().strip() if self.deduction_input.text().strip() else "0"
        net = self.net_input.text().strip() if self.net_input.text().strip() else "0"
        supplier_amount = self.supplier_amount_input.text().strip() if self.supplier_amount_input.text().strip() else "0"
        payment = self.payment_input.text().strip() if self.payment_input.text().strip() else "0"

        row = self.table.rowCount()
        self.table.insertRow(row)

        values = [
            op_date, record, desc, item_type, price if price else "0",
            gross if gross else "0", deduction, net, supplier_amount, payment
        ]

        for c, val in enumerate(values):
            self.table.setItem(row, c, QTableWidgetItem(val))

        self.table.resizeColumnsToContents()

        # Clear inputs (keep date and account)
        self.record_input.clear()
        self.desc_input.clear()
        self.gross_input.clear()
        self.deduction_input.clear()
        self.net_input.clear()
        self.price_input.clear()
        self.supplier_amount_input.clear()
        self.payment_input.setText("0")

    def save_operations(self):
        if self.account_combo.currentIndex() == -1:
            QMessageBox.warning(self, "خطأ", "اختر حساب أولاً")
            return

        account_id = self.account_combo.currentData()

        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "خطأ", "لا توجد عمليات لحفظها")
            return

        from datetime import date

        for row in range(self.table.rowCount()):
            try:
                op_date_str = self.table.item(row, 0).text()
                record_number = self.table.item(row, 1).text()
                description = self.table.item(row, 2).text()
                item_type = self.table.item(row, 3).text()
                price_per_ton = float(self.table.item(row, 4).text())
                gross_weight = float(self.table.item(row, 5).text())
                deduction = float(self.table.item(row, 6).text())
                net_weight = float(self.table.item(row, 7).text())
                supplier_amount = float(self.table.item(row, 8).text())
                payment = float(self.table.item(row, 9).text())

                # Parse date
                parts = op_date_str.split("-")
                op_date = date(int(parts[0]), int(parts[1]), int(parts[2])) if len(parts) == 3 else date.today()

                add_operation(
                    account_id=account_id,
                    account_type=self.acc_type,
                    description=description,
                    item_type=item_type,
                    price_per_ton=price_per_ton,
                    gross_weight=gross_weight,
                    deduction=deduction,
                    net_weight=net_weight,
                    supplier_amount=supplier_amount,
                    payment=payment,
                    op_date=op_date,
                    record_number=record_number
                )

            except Exception as e:
                QMessageBox.warning(self, "خطأ", f"خطأ في الصف {row + 1}: {e}")
                return

        QMessageBox.information(self, "تم", "تم حفظ العمليات بنجاح")
        self.table.setRowCount(0)
