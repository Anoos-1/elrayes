"""
Suppliers Management Page
إدارة الموردين مع التعديل والحذف والكاش
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


class SuppliersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إدارة الموردين")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet("background-color: #F9FAFB;")
        self.resize(1300, 800)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== HEADER =====
        header = QFrame()
        header.setStyleSheet("background-color: #E63946; border: none;")
        header.setFixedHeight(70)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)
        
        title_label = QLabel("الموردين")
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

        # ===== ADD SUPPLIER SECTION =====
        add_section = QGroupBox("إضافة مورد جديد")
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
                color: #E63946;
                font-weight: bold;
            }
        """)

        add_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("اسم المورد")
        self.name_input.setMinimumHeight(40)

        self.region_input = QLineEdit()
        self.region_input.setPlaceholderText("المنطقة")
        self.region_input.setMinimumHeight(40)

        add_btn = QPushButton("إضافة المورد")
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
        add_btn.clicked.connect(self.add_supplier)

        add_layout.addWidget(QLabel("الاسم:"), 0)
        add_layout.addWidget(self.name_input, 1)
        add_layout.addWidget(QLabel("المنطقة:"), 0)
        add_layout.addWidget(self.region_input, 1)
        add_layout.addWidget(add_btn, 0)

        add_section.setLayout(add_layout)
        content_layout.addWidget(add_section)

        # ===== SUPPLIERS TABLE SECTION =====
        table_section = QGroupBox("قائمة الموردين")
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
                color: #E63946;
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
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["المورد", "المنطقة", "الرصيد", "تعديل", "حذف"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #E5E7EB;
                font-size: 11px;
                border-radius: 6px;
            }
            QHeaderView::section {
                background-color: #E63946;
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
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 80)
        self.table.setRowHeight(0, 28)
        
        self.load()
        table_layout.addWidget(self.table)
        table_section.setLayout(table_layout)
        content_layout.addWidget(table_section)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def load(self):
        """تحميل قائمة الموردين"""
        self.table.setRowCount(0)
        suppliers = get_accounts("supplier")
        
        for i, supplier in enumerate(suppliers):
            self.table.insertRow(i)
            
            # Name
            name_item = QTableWidgetItem(supplier.name)
            name_item.setFont(QFont("Segoe UI", 11))
            self.table.setItem(i, 0, name_item)
            
            # Region
            region_item = QTableWidgetItem(supplier.region if supplier.region else "-")
            region_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(i, 1, region_item)
            
            # Balance (الرصيد)
            balance = get_account_balance(supplier.id)
            balance_item = QTableWidgetItem(f"{balance:,.2f}")
            balance_item.setTextAlignment(Qt.AlignCenter)
            if balance > 0:
                balance_item.setBackground(QColor("#fdecea"))
            elif balance < 0:
                balance_item.setBackground(QColor("#eafaf1"))
            self.table.setItem(i, 2, balance_item)
            
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
            edit_btn.clicked.connect(lambda checked, sid=supplier.id, sname=supplier.name, sregion=supplier.region: self.edit_supplier(sid, sname, sregion))
            self.table.setCellWidget(i, 3, edit_btn)
            
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
            delete_btn.clicked.connect(lambda checked, sid=supplier.id, sname=supplier.name: self.delete_supplier(sid, sname))
            self.table.setCellWidget(i, 4, delete_btn)

    def add_supplier(self):
        """إضافة مورد جديد"""
        name = self.name_input.text().strip()
        region = self.region_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم المورد")
            return
        
        try:
            create_account(name, "supplier", region)
            QMessageBox.information(self, "نجاح", f"تم إضافة المورد '{name}' بنجاح")
            self.name_input.clear()
            self.region_input.clear()
            self.load()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في إضافة المورد: {str(e)}")

    def edit_supplier(self, supplier_id, supplier_name, supplier_region):
        """تعديل بيانات مورد"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"تعديل المورد: {supplier_name}")
        dialog.setLayout(QFormLayout())
        dialog.setLayoutDirection(Qt.RightToLeft)
        
        name_input = QLineEdit()
        name_input.setText(supplier_name)
        
        region_input = QLineEdit()
        region_input.setText(supplier_region if supplier_region else "")
        
        dialog.layout().addRow("اسم المورد:", name_input)
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
        
        save_btn.clicked.connect(lambda: self._save_edit(dialog, supplier_id, name_input.text(), region_input.text()))
        cancel_btn.clicked.connect(dialog.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        dialog.layout().addRow(button_layout)
        
        dialog.exec()

    def _save_edit(self, dialog, supplier_id, new_name, new_region):
        """حفظ التعديل"""
        if not new_name.strip():
            QMessageBox.warning(self, "خطأ", "يرجى إدخال اسم المورد")
            return
        
        try:
            update_account(supplier_id, new_name, new_region)
            QMessageBox.information(self, "نجاح", "تم تحديث بيانات المورد بنجاح")
            dialog.accept()
            self.load()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"خطأ في التحديث: {str(e)}")

    def delete_supplier(self, supplier_id, supplier_name):
        """حذف مورد"""
        reply = QMessageBox.question(
            self,
            "تأكيد الحذف",
            f"هل أنت متأكد من حذف المورد '{supplier_name}'؟\nسيتم حذف جميع عملياته أيضاً.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                delete_account(supplier_id)
                QMessageBox.information(self, "نجاح", "تم حذف المورد بنجاح")
                self.load()
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"خطأ في الحذف: {str(e)}")

    def open_selected_ledger(self):
        """فتح كشف حساب للمورد المختار"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "تنبيه", "يرجى اختيار مورد")
            return
        
        suppliers = get_accounts("supplier")
        supplier = suppliers[current_row]
        self.ledger_window = LedgerViewPage(supplier.id, supplier.name)
        self.ledger_window.show()
