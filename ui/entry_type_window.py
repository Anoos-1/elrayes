from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt

from ui.operation_entry import OperationEntryPage


class EntryTypeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("تسجيل العمليات")
        self.resize(400, 300)

        layout = QVBoxLayout()

        title = QLabel("اختار نوع الحساب")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(title)

        self.btn_supplier = QPushButton("تسجيل مورد")
        self.btn_customer = QPushButton("تسجيل عميل")
        self.btn_bank = QPushButton("تسجيل بنك")

        for btn in [self.btn_supplier, self.btn_customer, self.btn_bank]:
            btn.setMinimumHeight(50)
            layout.addWidget(btn)

        self.setLayout(layout)

        self.btn_supplier.clicked.connect(lambda: self.open_entry("supplier"))
        self.btn_customer.clicked.connect(lambda: self.open_entry("customer"))
        self.btn_bank.clicked.connect(lambda: self.open_entry("bank"))

    def open_entry(self, acc_type):
        self.w = OperationEntryPage(acc_type)
        self.w.show()
