from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

from ui.suppliers import SuppliersPage
from ui.customers import CustomersPage
from ui.bank import BankPage


class InquiryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("استعلام")
        self.resize(400, 300)

        layout = QVBoxLayout()

        title = QLabel("شاشة الاستعلام")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(title)

        self.btn_suppliers = QPushButton("رصيد الموردين")
        self.btn_customers = QPushButton("رصيد العملاء")
        self.btn_bank = QPushButton("حسابات البنوك")

        for btn in [self.btn_suppliers, self.btn_customers, self.btn_bank]:
            btn.setMinimumHeight(50)
            layout.addWidget(btn)

        self.setLayout(layout)

        # Connections
        self.btn_suppliers.clicked.connect(self.open_suppliers)
        self.btn_customers.clicked.connect(self.open_customers)
        self.btn_bank.clicked.connect(self.open_bank)

    def open_suppliers(self):
        self.w = SuppliersPage()
        self.w.show()

    def open_customers(self):
        self.w = CustomersPage()
        self.w.show()

    def open_bank(self):
        self.w = BankPage()
        self.w.show()
