"""
Customers Management Page
إدارة العملاء مع التعديل والحذف والكاش
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QMessageBox, QLabel,
    QDialog, QFormLayout, QGroupBox, QScrollArea, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from services import create_account, get_accounts, get_account_balance, update_account, delete_account
from ui.ledger_view import LedgerViewPage


class CustomersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إدارة العملاء")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet("background-color: #F9FAFB;")
        self.resize(1300, 800)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== HEADER =====
        header = QFrame()
        header.setStyleSheet("background-color: #3498db; border: none;")
        header.setFixedHeight(70)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)
        
        title_label = QLabel("العملاء")
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

        # ===== ADD CUSTOMER SECTION =====
        add_section = QGroupBox("إضافة عميل جديد")
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
                color: #3498db;
                font-weight: bold;
            }
        """)

        add_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("اسم العميل")
        self.name_input.setMinimumHeight(40)

        self.region_input = QLineEdit()
        self.region_input.setPlaceholderText("المنطقة")
        self.region_input.setMinimumHeight(40)

        self.cash_input = QLineEdit()
        self.cash_input.setPlaceholderText("الكاش (اختياري)")
        self.cash_input.setMinimumHeight(40)

        add_btn = QPushButton("إضافة العميل")
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
        add_btn.clicked.connect(self.add_customer)

        add_layout.addWidget(QLabel("الاسم:"), 0)
        add_layout.addWidget(self.name_input, 1)
        add_layout.addWidget(QLabel("المنطقة:"), 0)
        add_layout.addWidget(self.region_input, 1)
        add_layout.addWidget(QLabel("الكاش:"), 0)
        add_layout.addWidget(self.cash_input, 1)
        add_layout.addWidget(add_btn, 0)

        add_section.setLayout(add_layout)
        content_layout.addWidget(add_section)

        # ===== CUSTOMERS TABLE SECTION =====
        table_section = QGroupBox("قائمة العملاء")
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
                color: #3498db;
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
        self.table.setHorizontalHeaderLabels(["العميل", "المنطقة", "الرصيد", "الكاش", "تعديل", "حذف"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #E5E7EB;
                font-size: 13px;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 10px;
                font-weight: bold;
                border: none;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 80)
        
        self.load()
        table_layout.addWidget(self.table)
        table_section.setLayout(table_layout)
        content_layout.addWidget(table_section)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def load(self):
        """تحميل قائمة العملاء"""
        self.table.setRowCount(0)
        customers = get_accounts("customer")
        
        for i, customer in enumerate(customers):
            self.table.insertRow(i)
            
            # Name
            name_item = QTableWidgetItem(customer.name)
            name_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(i, 0, name_item)
            
            # Region
            region_item = QTableWidgetItem(customer.region if customer.region else "-")
            region_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, region_item)
            
            # Balance (الرصيد)
            balance = get_account_balance(customer.id)
            balance_item = QTableWidgetItem(f"{balance:,.2f}")
            balance_item.setTextAlignment(Qt.AlignCenter)
            if balance > 0:
                balance_item.setBackground(QColor("#e3f2fd"))
            elif balance < 0:
                balance_item.setBackground(QColor("#eafaf1"))
            self.table.setItem(i, 2, balance_item)
            
            # Cash (الكاش)
            cash_item = QTableWidgetItem("-")
            cash_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 3, cash_item)
            
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
            edit_btn.clicked.connect(lambda checked, cid=customer.id, cname=customer.name, cregion=customer.region: self.edit_customer(cid, cname, cregion))
            self.table.setCellWidget(i, 4, edit_btn)
            
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
            delete_btn.clicked.connect(lambda checked, cid=customer.id, cname=customer.name: self.delete_customer(cid, cname))
            self.table.setCellWidget(i, 5, delete_btn)

    def add_customer(self):
        """إضافة عميل جديد"""
        name = self.name_input.text().strip()
        region = self.region_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم العميل")
            return
        
        try:
            create_account(name, "customer", region)
            QMessageBox.information(self, "نجاح", f"تم إضافة العميل '{name}' بنجاح")
            self.name_input.clear()
            self.region_input.clear()
            self.cash_input.clear()
            self.load()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في إضافة العميل: {str(e)}")

    def edit_customer(self, customer_id, customer_name, customer_region):
        """تعديل بيانات عميل"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"تعديل العميل: {customer_name}")
        dialog.setLayout(QFormLayout())
        dialog.setLayoutDirection(Qt.RightToLeft)
        
        name_input = QLineEdit()
        name_input.setText(customer_name)
        
        region_input = QLineEdit()
        region_input.setText(customer_region if customer_region else "")
        
        dialog.layout().addRow("اسم العميل:", name_input)
        dialog.layout().addRow("المنطقة:", region_input)
        
        button_layout = QHBoxLayout()
        save_btn = QPushButton("حفظ")
        cancel_btn = QPushButton("إلغاء")
        
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #0052CC;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
        """)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
            }
        """)
        
        save_btn.clicked.connect(lambda: self._save_edit(dialog, customer_id, name_input.text(), region_input.text()))
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        dialog.layout().addRow(button_layout)
        
        dialog.exec()

    def _save_edit(self, dialog, customer_id, new_name, new_region):
        """حفظ التعديل"""
        if not new_name.strip():
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم العميل")
            return
        
        try:
            update_account(customer_id, new_name, new_region)
            QMessageBox.information(self, "نجاح", "تم تحديث بيانات العميل بنجاح")
            dialog.accept()
            self.load()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في التحديث: {str(e)}")

    def delete_customer(self, customer_id, customer_name):
        """حذف عميل"""
        reply = QMessageBox.question(
            self,
            "تأكيد الحذف",
            f"هل أنت متأكد من حذف العميل '{customer_name}'؟\nسيتم حذف جميع عملياته أيضاً.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                delete_account(customer_id)
                QMessageBox.information(self, "نجاح", "تم حذف العميل بنجاح")
                self.load()
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"خطأ في الحذف: {str(e)}")
