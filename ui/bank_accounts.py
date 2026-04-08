"""
Bank Accounts Management Page
إدارة حسابات البنوك مع كامل العمليات (إضافة - تعديل - حذف)
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QMessageBox, QLabel, QDialog, QFormLayout,
    QGroupBox, QScrollArea, QFrame, QHeaderView, QDoubleSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont, QIcon

from services import (
    create_bank_account, get_bank_accounts, get_bank_account_by_id, 
    update_bank_account, delete_bank_account
)


class AddBankAccountPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إضافة حساب بنكي")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet("background-color: #F9FAFB;")
        self.resize(1400, 800)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== HEADER =====
        header = QFrame()
        header.setStyleSheet("background-color: #28A745; border: none;")
        header.setFixedHeight(70)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)
        
        title_label = QLabel("حسابات البنوك")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        close_btn = QPushButton("العودة")
        close_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        close_btn.setFixedHeight(44)
        close_btn.setMinimumWidth(160)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC2626;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B91C1C;
            }
        """)
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)
        main_layout.addWidget(header)

        # ===== SCROLL AREA FOR CONTENT =====
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #F9FAFB; }")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(20)

        # ===== ADD BANK ACCOUNT SECTION =====
        add_section = self._create_add_section()
        content_layout.addWidget(add_section)

        # ===== BANK ACCOUNTS TABLE SECTION =====
        table_section = self._create_table_section()
        content_layout.addWidget(table_section)

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)
        self.load()

    def _create_add_section(self):
        """Create the 'Add Bank Account' section"""
        add_section = QGroupBox("إضافة حساب بنكي جديد")
        add_section.setStyleSheet("""
            QGroupBox {
                background: linear-gradient(135deg, #ffffff 0%, #F0F9F5 100%);
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 20px;
                border: 2px solid #28A745;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                right: 10px;
                padding: 0 6px;
                color: #28A745;
                font-weight: bold;
                font-size: 13px;
            }
        """)

        add_layout = QVBoxLayout()
        add_layout.setContentsMargins(15, 15, 15, 15)
        add_layout.setSpacing(12)

        # Input row with fields
        input_row = QHBoxLayout()
        input_row.setSpacing(12)

        # Bank Name
        label1 = QLabel("اسم البنك:")
        label1.setFont(QFont("Segoe UI", 11, QFont.Bold))
        label1.setMinimumWidth(100)
        input_row.addWidget(label1)

        self.bank_name_input = QLineEdit()
        self.bank_name_input.setPlaceholderText("البنك الأهلي، بنك مصر، إلخ")
        self.bank_name_input.setMinimumHeight(40)
        self._style_line_edit(self.bank_name_input)
        input_row.addWidget(self.bank_name_input)

        # Account Name
        label2 = QLabel("اسم الحساب:")
        label2.setFont(QFont("Segoe UI", 11, QFont.Bold))
        label2.setMinimumWidth(100)
        input_row.addWidget(label2)

        self.account_name_input = QLineEdit()
        self.account_name_input.setPlaceholderText("حساب جاري، حساب توفير، إلخ")
        self.account_name_input.setMinimumHeight(40)
        self._style_line_edit(self.account_name_input)
        input_row.addWidget(self.account_name_input)

        # Account Number
        label3 = QLabel("رقم الحساب:")
        label3.setFont(QFont("Segoe UI", 11, QFont.Bold))
        label3.setMinimumWidth(100)
        input_row.addWidget(label3)

        self.account_number_input = QLineEdit()
        self.account_number_input.setPlaceholderText("0123456789")
        self.account_number_input.setMinimumHeight(40)
        self._style_line_edit(self.account_number_input)
        input_row.addWidget(self.account_number_input)

        # Initial Balance
        label4 = QLabel("الرصيد الابتدائي:")
        label4.setFont(QFont("Segoe UI", 11, QFont.Bold))
        label4.setMinimumWidth(100)
        input_row.addWidget(label4)

        self.balance_input = QDoubleSpinBox()
        self.balance_input.setMinimumHeight(40)
        self.balance_input.setMaximum(9999999.99)
        self.balance_input.setValue(0)
        self.balance_input.setStyleSheet("""
            QDoubleSpinBox {
                background-color: white;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
            }
            QDoubleSpinBox:focus {
                border: 2px solid #28A745;
                background-color: #F0F9F5;
            }
        """)
        input_row.addWidget(self.balance_input)

        # Add Button with green color and icon
        add_btn = QPushButton("+ إضافة حساب")
        add_btn.setMinimumHeight(40)
        add_btn.setMinimumWidth(150)
        add_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1E7E34;
            }
        """)
        add_btn.clicked.connect(self.add_account)
        input_row.addWidget(add_btn)

        add_layout.addLayout(input_row)
        add_section.setLayout(add_layout)
        return add_section

    def _create_table_section(self):
        """Create the Bank Accounts Table section"""
        table_section = QGroupBox("الحسابات المسجلة")
        table_section.setStyleSheet("""
            QGroupBox {
                background-color: white;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 20px;
                border: 1px solid #E5E7EB;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                right: 10px;
                padding: 0 6px;
                color: #28A745;
                font-weight: bold;
            }
        """)

        table_layout = QVBoxLayout()

        # Create action buttons toolbar
        action_layout = QHBoxLayout()
        refresh_btn = QPushButton("تحديث القائمة")
        refresh_btn.setMinimumHeight(40)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
        """)
        refresh_btn.clicked.connect(self.load)
        action_layout.addStretch()
        action_layout.addWidget(refresh_btn)
        table_layout.addLayout(action_layout)

        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["اسم البنك", "اسم الحساب", "رقم الحساب", "الرصيد الحالي", "تعديل", "حذف"])
        
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #E5E7EB;
                font-size: 11px;
                border-radius: 6px;
                border: none;
            }
            QHeaderView::section {
                background-color: #28A745;
                color: white;
                padding: 6px;
                font-weight: bold;
                border: none;
                height: 32px;
            }
            QTableWidget::item {
                padding: 4px;
                height: 28px;
            }
        """)
        
        # Set column resize modes
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Bank name
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Account name
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Account number
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # Current balance
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Edit button
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Delete button
        
        self.table.setMinimumHeight(300)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 80)
        
        table_layout.addWidget(self.table)
        table_section.setLayout(table_layout)
        return table_section

    def _style_line_edit(self, line_edit):
        """Apply consistent styling to QLineEdit"""
        line_edit.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #28A745;
                background-color: #F0F9F5;
            }
        """)

    def load(self):
        """Load all bank accounts into the table"""
        self.table.setRowCount(0)
        accounts = get_bank_accounts()
        
        for i, account in enumerate(accounts):
            self.table.insertRow(i)
            
            # Bank Name
            bank_item = QTableWidgetItem(account.bank_name)
            bank_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(i, 0, bank_item)
            
            # Account Name
            acc_name_item = QTableWidgetItem(account.account_name)
            acc_name_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(i, 1, acc_name_item)
            
            # Account Number
            acc_num_item = QTableWidgetItem(account.account_number)
            acc_num_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(i, 2, acc_num_item)
            
            # Current Balance
            balance_item = QTableWidgetItem(f"{account.current_balance:,.2f}")
            balance_item.setFont(QFont("Segoe UI", 11))
            balance_item.setTextAlignment(Qt.AlignCenter)
            
            # Color balance based on value
            if account.current_balance > 0:
                balance_item.setForeground(QColor("#10B981"))  # Green
            elif account.current_balance < 0:
                balance_item.setForeground(QColor("#EF4444"))  # Red
            
            self.table.setItem(i, 3, balance_item)
            
            # Edit Button
            edit_btn = QPushButton("تعديل")
            edit_btn.setMinimumHeight(32)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3B82F6;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1D4ED8;
                }
            """)
            edit_btn.clicked.connect(lambda checked, aid=account.id, aname=account.account_name: self.edit_account(aid, aname))
            self.table.setCellWidget(i, 4, edit_btn)
            
            # Delete Button
            delete_btn = QPushButton("حذف")
            delete_btn.setMinimumHeight(32)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #EF4444;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #DC2626;
                }
            """)
            delete_btn.clicked.connect(lambda checked, aid=account.id, aname=account.account_name: self.delete_account(aid, aname))
            self.table.setCellWidget(i, 5, delete_btn)

    def add_account(self):
        """Add a new bank account"""
        bank_name = self.bank_name_input.text().strip()
        account_name = self.account_name_input.text().strip()
        account_number = self.account_number_input.text().strip()
        initial_balance = self.balance_input.value()
        
        if not bank_name or not account_name or not account_number:
            QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول المطلوبة")
            return
        
        try:
            create_bank_account(bank_name, account_name, account_number, initial_balance)
            QMessageBox.information(self, "نجاح", f"تم إضافة الحساب '{account_name}' بنجاح")
            
            # Clear inputs
            self.bank_name_input.clear()
            self.account_name_input.clear()
            self.account_number_input.clear()
            self.balance_input.setValue(0)
            
            self.load()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في إضافة الحساب: {str(e)}")

    def edit_account(self, account_id, account_name):
        """Edit a bank account"""
        account = get_bank_account_by_id(account_id)
        if not account:
            QMessageBox.warning(self, "خطأ", "لم يتم العثور على الحساب")
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"تعديل الحساب: {account_name}")
        dialog.setLayout(QFormLayout())
        dialog.setLayoutDirection(Qt.RightToLeft)
        
        bank_name_input = QLineEdit()
        bank_name_input.setText(account.bank_name)
        
        account_name_input = QLineEdit()
        account_name_input.setText(account.account_name)
        
        account_number_input = QLineEdit()
        account_number_input.setText(account.account_number)
        
        balance_spinbox = QDoubleSpinBox()
        balance_spinbox.setMaximum(9999999.99)
        balance_spinbox.setValue(account.current_balance)
        
        dialog.layout().addRow("اسم البنك:", bank_name_input)
        dialog.layout().addRow("اسم الحساب:", account_name_input)
        dialog.layout().addRow("رقم الحساب:", account_number_input)
        dialog.layout().addRow("الرصيد الحالي:", balance_spinbox)
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton("حفظ")
        cancel_btn = QPushButton("إلغاء")
        
        save_btn.clicked.connect(lambda: self._save_edit(
            dialog, account_id, bank_name_input.text(),
            account_name_input.text(), account_number_input.text(),
            balance_spinbox.value()
        ))
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        dialog.layout().addRow(button_layout)
        
        dialog.exec()

    def _save_edit(self, dialog, account_id, bank_name, account_name, account_number, balance):
        """Save the edited bank account"""
        if not bank_name.strip() or not account_name.strip() or not account_number.strip():
            QMessageBox.warning(self, "خطأ", "يرجى ملء جميع الحقول المطلوبة")
            return
        
        try:
            account = get_bank_account_by_id(account_id)
            if account:
                # Calculate balance difference
                balance_change = balance - account.current_balance
                account.initial_balance = account.initial_balance + balance_change
                account.current_balance = balance
            
            update_bank_account(account_id, bank_name, account_name, account_number)
            QMessageBox.information(self, "نجاح", "تم تحديث الحساب بنجاح")
            dialog.accept()
            self.load()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في التحديث: {str(e)}")

    def delete_account(self, account_id, account_name):
        """Delete a bank account"""
        reply = QMessageBox.question(
            self,
            "تأكيد الحذف",
            f"هل أنت متأكد من حذف الحساب '{account_name}'؟",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                delete_bank_account(account_id)
                QMessageBox.information(self, "نجاح", "تم حذف الحساب بنجاح")
                self.load()
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"خطأ في الحذف: {str(e)}")
