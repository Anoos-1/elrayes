from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit, QMessageBox, QLabel, QDialog, QFormLayout,
    QGroupBox, QScrollArea, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont

from services import create_account, get_accounts, get_account_balance, update_account, delete_account, get_account_by_id
from ui.base_layout import ModuleHeader, ActionBar, SectionCard
from ui.style import COLORS


class SuppliersPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إدارة الموردين")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet("background-color: #F9FAFB;")
        self.resize(1200, 700)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== HEADER =====
        header = ModuleHeader("الموردين", on_close=self.close)
        main_layout.addWidget(header)

        # ===== SCROLL AREA FOR CONTENT =====
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: #F9FAFB; }")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(20)

        # ===== ACTION BAR =====
        actions_config = [
            ("إضافة مورد جديد", self.show_add_section),
            ("تحديث البيانات", self.load),
        ]
        action_bar = ActionBar(actions_config)
        content_layout.addWidget(action_bar)

        # ===== ADD SUPPLIER SECTION =====
        self.add_card = SectionCard("إضافة مورد جديد")
        add_layout = self.add_card.layout
        
        # Input fields
        input_layout = QHBoxLayout()
        input_layout.setSpacing(12)
        
        label1 = QLabel("اسم المورد:")
        label1.setFont(QFont("Segoe UI", 11, QFont.Bold))
        label1.setMinimumWidth(100)
        self.name = QLineEdit()
        self.name.setPlaceholderText("أدخل اسم المورد")
        self.name.setMinimumHeight(40)
        input_layout.addWidget(label1)
        input_layout.addWidget(self.name)
        
        label2 = QLabel("المنطقة:")
        label2.setFont(QFont("Segoe UI", 11, QFont.Bold))
        label2.setMinimumWidth(80)
        self.region = QLineEdit()
        self.region.setPlaceholderText("أدخل المنطقة (اختياري)")
        self.region.setMinimumHeight(40)
        input_layout.addWidget(label2)
        input_layout.addWidget(self.region)
        
        btn_add = QPushButton("إضافة")
        btn_add.setFont(QFont("Segoe UI", 11, QFont.Bold))
        btn_add.setFixedHeight(40)
        btn_add.setMinimumWidth(100)
        btn_add.clicked.connect(self.add_supplier)
        input_layout.addWidget(btn_add)
        
        add_layout.addLayout(input_layout)
        content_layout.addWidget(self.add_card)

        # ===== SUPPLIERS TABLE =====
        table_card = SectionCard("قائمة الموردين")
        table_layout = table_card.layout

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["المورد", "المنطقة", "الرصيد", "الإجراءات"])
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 200)
        self.table.setMinimumHeight(400)
        self.table.setAlternatingRowColors(True)
        table_layout.addWidget(self.table)
        
        content_layout.addWidget(table_card)
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        self.setLayout(main_layout)
        self.load()

    def show_add_section(self):
        """Scroll to add section"""
        self.add_card.setStyleSheet("""
            QFrame {
                background-color: #E8F4FF;
                border: 2px solid #0052CC;
                border-radius: 8px;
            }
        """)

    def load(self):
        self.accounts = get_accounts("supplier")
        self.table.setRowCount(len(self.accounts))

        for i, s in enumerate(self.accounts):
            name_item = QTableWidgetItem(s.name)
            region_item = QTableWidgetItem(s.region if s.region else "-")
            balance = get_account_balance(s.id)
            balance_item = QTableWidgetItem(f"{balance:,.2f}")
            balance_item.setTextAlignment(Qt.AlignCenter)

            # Color balance
            if balance < 0:
                balance_item.setForeground(QColor("#0B8345"))  # Green if positive (we owe)
            elif balance > 0:
                balance_item.setForeground(QColor("#DC2626"))  # Red if negative

            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, region_item)
            self.table.setItem(i, 2, balance_item)
            
            # Add action buttons
            actions_widget = self.create_action_buttons(s.id, s.name)
            self.table.setCellWidget(i, 3, actions_widget)

        self.table.resizeRowsToContents()
    
    def create_action_buttons(self, account_id, account_name):
        """Create edit and delete buttons for each row"""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)
        
        # Edit button
        edit_btn = QPushButton("تعديل")
        edit_btn.setObjectName("editBtn")
        edit_btn.setFixedHeight(32)
        edit_btn.setMinimumWidth(70)
        edit_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        edit_btn.clicked.connect(lambda: self.edit_supplier(account_id, account_name))
        
        # Delete button
        delete_btn = QPushButton("حذف")
        delete_btn.setObjectName("dangerBtn")
        delete_btn.setFixedHeight(32)
        delete_btn.setMinimumWidth(70)
        delete_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        delete_btn.clicked.connect(lambda: self.delete_supplier(account_id, account_name))
        
        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)
        
        widget.setLayout(layout)
        return widget
    
    def edit_supplier(self, account_id, account_name):
        """Edit supplier dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("تعديل المورد")
        dialog.setGeometry(100, 100, 500, 250)
        dialog.setLayoutDirection(Qt.RightToLeft)
        
        layout = QFormLayout()
        
        account = get_account_by_id(account_id)
        current_region = account.region if account and account.region else ""
        
        name_field = QLineEdit(account_name)
        name_field.setMinimumHeight(40)
        region_field = QLineEdit(current_region)
        region_field.setMinimumHeight(40)
        balance = get_account_balance(account_id)
        balance_label = QLabel(f"{balance:,.2f}")
        balance_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        
        layout.addRow("المورد:", name_field)
        layout.addRow("المنطقة:", region_field)
        layout.addRow("الرصيد:", balance_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("حفظ")
        save_btn.setFixedHeight(40)
        save_btn.setMinimumWidth(100)
        cancel_btn = QPushButton("إلغاء")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setMinimumWidth(100)
        cancel_btn.setObjectName("secondaryBtn")
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow(button_layout)
        
        dialog.setLayout(layout)
        
        def save():
            new_name = name_field.text().strip()
            new_region = region_field.text().strip()
            
            if not new_name:
                QMessageBox.warning(dialog, "تنبيه", "اسم المورد مطلوب")
                return
            
            try:
                update_account(account_id, new_name, new_region)
                QMessageBox.information(dialog, "نجاح", "تم تحديث المورد بنجاح")
                dialog.accept()
                self.load()
            except Exception as e:
                QMessageBox.critical(dialog, "خطأ", f"فشل التحديث: {str(e)}")
        
        save_btn.clicked.connect(save)
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def delete_supplier(self, account_id, account_name):
        """Delete supplier with confirmation"""
        reply = QMessageBox.question(
            self, 
            "تأكيد الحذف",
            f"هل تريد حذف المورد '{account_name}'؟",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                delete_account(account_id)
                QMessageBox.information(self, "نجاح", "تم حذف المورد بنجاح")
                self.load()
            except Exception as e:
                QMessageBox.critical(self, "خطأ", f"فشل الحذف: {str(e)}")

    def add_supplier(self):
        name = self.name.text().strip()
        region = self.region.text().strip()
        
        if not name:
            QMessageBox.warning(self, "تنبيه", "اسم المورد مطلوب")
            return
        
        try:
            create_account(name, "supplier", region)
            QMessageBox.information(self, "نجاح", "تم إضافة المورد بنجاح")
            self.name.clear()
            self.region.clear()
            self.load()
        except Exception as e:
            QMessageBox.critical(self, "خطأ", f"فشل الإضافة: {str(e)}")
