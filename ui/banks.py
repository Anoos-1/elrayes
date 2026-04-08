"""
Banks Management Page
إدارة حسابات البنوك مع كامل العمليات (إضافة - تعديل - حذف)
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QMessageBox, QLabel, QDialog, QFormLayout,
    QGroupBox, QScrollArea, QFrame, QSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from services import create_account, get_accounts, get_account_balance, update_account, delete_account, get_account_by_id


class BanksPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إدارة البنوك")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet("background-color: #F9FAFB;")
        self.resize(1200, 700)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== HEADER =====
        header = QFrame()
        header.setStyleSheet("background-color: #1D7874; border: none;")
        header.setFixedHeight(70)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)
        
        title_label = QLabel("البنوك")
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

        # ===== ADD BANK SECTION =====
        add_section = QGroupBox("إضافة بنك جديد")
        add_section.setStyleSheet("""
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
                color: #003D7A;
                font-weight: bold;
            }
        """)

        add_layout = QHBoxLayout()

        self.bank_name_input = QLineEdit()
        self.bank_name_input.setPlaceholderText("اسم البنك")
        self.bank_name_input.setMinimumHeight(40)

        add_btn = QPushButton("إضافة البنك")
        add_btn.setMinimumHeight(40)
        add_btn.setMinimumWidth(120)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #0052CC;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0041A8;
            }
        """)
        add_btn.clicked.connect(self.add_bank)

        add_layout.addWidget(QLabel("اسم البنك:"), 0)
        add_layout.addWidget(self.bank_name_input, 1)
        add_layout.addWidget(add_btn, 0)

        add_section.setLayout(add_layout)
        content_layout.addWidget(add_section)

        # ===== BANKS TABLE SECTION =====
        table_section = QGroupBox("البنوك المسجلة")
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
                color: #003D7A;
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
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["البنك", "الرصيد", "تعديل", "حذف"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #E5E7EB;
                font-size: 13px;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #003D7A;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 100)
        self.table.setColumnWidth(3, 100)
        
        self.load()
        table_layout.addWidget(self.table)
        table_section.setLayout(table_layout)
        content_layout.addWidget(table_section)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def load(self):
        """تحميل قائمة البنوك"""
        self.table.setRowCount(0)
        banks = get_accounts("bank")
        
        for i, bank in enumerate(banks):
            self.table.insertRow(i)
            
            # Name
            name_item = QTableWidgetItem(bank.name)
            name_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(i, 0, name_item)
            
            # Balance
            balance = get_account_balance(bank.id)
            balance_item = QTableWidgetItem(f"{balance:,.2f}")
            balance_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, balance_item)
            

            # Edit button
            edit_btn = QPushButton("✏️ تعديل")
            edit_btn.setMinimumHeight(32)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFD700;
                    color: black;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #FFC700;
                }
            """)
            edit_btn.clicked.connect(lambda checked, bid=bank.id, bname=bank.name: self.edit_bank(bid, bname))
            self.table.setCellWidget(i, 2, edit_btn)
            
            # Delete button
            delete_btn = QPushButton("🗑️ حذف")
            delete_btn.setMinimumHeight(32)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #DC2626;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #B91C1C;
                }
            """)
            delete_btn.clicked.connect(lambda checked, bid=bank.id, bname=bank.name: self.delete_bank(bid, bname))
            self.table.setCellWidget(i, 3, delete_btn)

    def add_bank(self):
        """إضافة بنك جديد"""
        name = self.bank_name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم البنك")
            return
        
        try:
            create_account(name, "bank")
            QMessageBox.information(self, "نجاح", f"تم إضافة البنك '{name}' بنجاح")
            self.bank_name_input.clear()
            self.load()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في إضافة البنك: {str(e)}")

    def edit_bank(self, bank_id, bank_name):
        """تعديل بنك"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"تعديل البنك: {bank_name}")
        dialog.setLayout(QFormLayout())
        dialog.setLayoutDirection(Qt.RightToLeft)
        
        name_input = QLineEdit()
        name_input.setText(bank_name)
        
        dialog.layout().addRow("اسم البنك:", name_input)
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton("حفظ")
        cancel_btn = QPushButton("إلغاء")
        
        save_btn.clicked.connect(lambda: self._save_edit(dialog, bank_id, name_input.text()))
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        dialog.layout().addRow(button_layout)
        
        dialog.exec()

    def _save_edit(self, dialog, bank_id, new_name):
        """حفظ التعديل"""
        if not new_name.strip():
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم البنك")
            return
        
        try:
            update_account(bank_id, new_name, "")
            QMessageBox.information(self, "نجاح", "تم تحديث البنك بنجاح")
            dialog.accept()
            self.load()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في التحديث: {str(e)}")

    def delete_bank(self, bank_id, bank_name):
        """حذف بنك"""
        reply = QMessageBox.question(
            self,
            "تأكيد الحذف",
            f"هل أنت متأكد من حذف البنك '{bank_name}'؟",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                delete_account(bank_id)
                QMessageBox.information(self, "نجاح", "تم حذف البنك بنجاح")
                self.load()
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"خطأ في الحذف: {str(e)}")
