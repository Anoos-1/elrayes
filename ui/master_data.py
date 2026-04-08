from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
from PySide6.QtCore import Qt

from services import get_companies, add_company, get_item_types, add_item_type


class MasterDataPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("إدارة البيانات الأساسية")
        self.resize(600, 400)
        self.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()

        tabs = QTabWidget()
        tabs.addTab(self.create_companies_tab(), "الشركات")
        tabs.addTab(self.create_types_tab(), "الأنواع")

        layout.addWidget(tabs)
        self.setLayout(layout)

    # ---------- Companies ----------
    def create_companies_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("اسم الشركة")

        add_btn = QPushButton("إضافة شركة")
        add_btn.clicked.connect(self.add_company_action)

        self.company_table = QTableWidget()
        self.company_table.setColumnCount(1)
        self.company_table.setHorizontalHeaderLabels(["الشركة"])

        layout.addWidget(self.company_input)
        layout.addWidget(add_btn)
        layout.addWidget(self.company_table)

        self.load_companies()
        return widget

    def load_companies(self):
        companies = get_companies()
        self.company_table.setRowCount(len(companies))

        for i, c in enumerate(companies):
            self.company_table.setItem(i, 0, QTableWidgetItem(c.name))

    def add_company_action(self):
        name = self.company_input.text().strip()
        if not name:
            QMessageBox.warning(self, "تنبيه", "أدخل اسم الشركة")
            return

        add_company(name)
        self.company_input.clear()
        self.load_companies()

    # ---------- Item Types ----------
    def create_types_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.type_input = QLineEdit()
        self.type_input.setPlaceholderText("اسم النوع")

        add_btn = QPushButton("إضافة نوع")
        add_btn.clicked.connect(self.add_type_action)

        self.type_table = QTableWidget()
        self.type_table.setColumnCount(1)
        self.type_table.setHorizontalHeaderLabels(["النوع"])

        layout.addWidget(self.type_input)
        layout.addWidget(add_btn)
        layout.addWidget(self.type_table)

        self.load_types()
        return widget

    def load_types(self):
        types = get_item_types()
        self.type_table.setRowCount(len(types))

        for i, t in enumerate(types):
            self.type_table.setItem(i, 0, QTableWidgetItem(t.name))

    def add_type_action(self):
        name = self.type_input.text().strip()
        if not name:
            QMessageBox.warning(self, "تنبيه", "أدخل اسم النوع")
            return

        add_item_type(name)
        self.type_input.clear()
        self.load_types()
