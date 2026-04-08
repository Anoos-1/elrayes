"""
Account Statement (Ledger) Page
كشف حساب الموردين والعملاء
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QLabel, QFrame, QHeaderView, QPushButton,
    QDateEdit, QComboBox
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QColor, QFont

from services import get_operations, get_account_balance, get_account_by_id


class AccountStatementPage(QWidget):
    def __init__(self, account_id, account_name, account_type="supplier"):
        super().__init__()

        self.account_id = account_id
        self.account_name = account_name
        self.account_type = account_type  # 'supplier' or 'customer'

        self.setWindowTitle(f"كشف حساب - {account_name}")
        self.setLayoutDirection(Qt.RightToLeft)
        self.setStyleSheet("background-color: #F9FAFB;")
        self.resize(1400, 900)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== HEADER =====
        header_color = "#E63946" if account_type == "supplier" else "#3498db"
        header = self._create_header(header_color)
        main_layout.addWidget(header)

        # ===== CONTENT AREA =====
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(24, 24, 24, 24)
        content_layout.setSpacing(16)

        # Account Info Card
        info_card = self._create_account_info_card()
        content_layout.addWidget(info_card)

        # Filter Row
        filter_row = self._create_filter_row()
        content_layout.addLayout(filter_row)

        # Table
        self.table = self._create_table()
        content_layout.addWidget(self.table)

        # Summary Card
        summary_card = self._create_summary_card()
        content_layout.addWidget(summary_card)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        self.load_data()

    def _create_header(self, color):
        """Create the header frame"""
        header = QFrame()
        header.setStyleSheet(f"background-color: {color}; border: none;")
        header.setFixedHeight(70)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(24, 16, 24, 16)
        
        title_label = QLabel("كشف حساب")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel(f"({self.account_name})")
        subtitle_label.setFont(QFont("Segoe UI", 14))
        subtitle_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
        header_layout.addWidget(subtitle_label)
        
        header_layout.addStretch()
        
        close_btn = QPushButton("العودة")
        close_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        close_btn.setFixedHeight(40)
        close_btn.setMinimumWidth(120)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.2);
                color: white;
                border: 2px solid white;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.4);
            }
        """)
        close_btn.clicked.connect(self.close)
        header_layout.addWidget(close_btn)
        
        return header

    def _create_account_info_card(self):
        """Create account information card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        layout = QHBoxLayout(card)
        layout.setSpacing(40)

        # Account Name
        name_label = QLabel("اسم الحساب:")
        name_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        name_value = QLabel(self.account_name)
        name_value.setFont(QFont("Segoe UI", 11))
        
        # Account Type
        type_label = QLabel("نوع الحساب:")
        type_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        type_text = "مورد" if self.account_type == "supplier" else "عميل"
        type_value = QLabel(type_text)
        type_value.setFont(QFont("Segoe UI", 11))
        
        # Current Balance
        current_balance = get_account_balance(self.account_id)
        balance_label = QLabel("الرصيد الحالي:")
        balance_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        balance_value = QLabel(f"{current_balance:,.2f}")
        balance_value.setFont(QFont("Segoe UI", 11, QFont.Bold))
        if current_balance > 0:
            balance_value.setStyleSheet("color: #DC2626;")  # Red for debit
        elif current_balance < 0:
            balance_value.setStyleSheet("color: #10B981;")  # Green for credit
        
        layout.addWidget(name_label)
        layout.addWidget(name_value)
        layout.addSpacing(20)
        layout.addWidget(type_label)
        layout.addWidget(type_value)
        layout.addSpacing(20)
        layout.addWidget(balance_label)
        layout.addWidget(balance_value)
        layout.addStretch()
        
        return card

    def _create_filter_row(self):
        """Create filter controls"""
        layout = QHBoxLayout()
        layout.setSpacing(12)

        # From Date
        from_label = QLabel("من التاريخ:")
        self.from_date = QDateEdit()
        self.from_date.setDate(QDate.currentDate().addMonths(-1))
        self.from_date.setCalendarPopup(True)
        self.from_date.setMinimumHeight(36)

        # To Date
        to_label = QLabel("إلى التاريخ:")
        self.to_date = QDateEdit()
        self.to_date.setDate(QDate.currentDate())
        self.to_date.setCalendarPopup(True)
        self.to_date.setMinimumHeight(36)

        # Filter Button
        filter_btn = QPushButton("تطبيق الفلترة")
        filter_btn.setMinimumHeight(36)
        filter_btn.setMinimumWidth(120)
        filter_btn.setStyleSheet("""
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
        filter_btn.clicked.connect(self.load_data)

        layout.addWidget(from_label)
        layout.addWidget(self.from_date)
        layout.addSpacing(20)
        layout.addWidget(to_label)
        layout.addWidget(self.to_date)
        layout.addSpacing(20)
        layout.addWidget(filter_btn)
        layout.addStretch()

        return layout

    def _create_table(self):
        """Create the statement table"""
        table = QTableWidget()
        table.setColumnCount(11)
        table.setHorizontalHeaderLabels([
            "التاريخ",           # Date
            "رقم المحضر",       # Record Number
            "البيان",           # Description
            "نوع العنصر",       # Item Type
            "سعر الطن",         # Price per ton
            "الوزن (قبل)",     # Gross Weight
            "الوزن (بعد)",      # Net Weight
            "مدين",             # Supplier Amount (Debit)
            "دائن",             # Payment (Credit)
            "الرصيد",           # Balance
            "ملاحظات",          # Notes
        ])

        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: #E5E7EB;
                font-size: 11px;
                border-radius: 6px;
                border: none;
            }
            QHeaderView::section {
                background-color: #1F2937;
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
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Date
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Record Number
        header.setSectionResizeMode(2, QHeaderView.Stretch)           # Description
        header.setSectionResizeMode(3, QHeaderView.Stretch)           # Item Type
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Price
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Gross Weight
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Net Weight
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Debit
        header.setSectionResizeMode(8, QHeaderView.ResizeToContents)  # Credit
        header.setSectionResizeMode(9, QHeaderView.ResizeToContents)  # Balance
        header.setSectionResizeMode(10, QHeaderView.Stretch)          # Notes

        table.setMinimumHeight(400)

        return table

    def _create_summary_card(self):
        """Create summary card with totals"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: linear-gradient(135deg, #ffffff 0%, #F9FAFB 100%);
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        layout = QHBoxLayout(card)
        layout.setSpacing(30)

        self.summary_labels = {}

        # Opening Balance
        opening_label = QLabel("رصيد أول المدة:")
        opening_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.summary_labels['opening'] = QLabel("0.00")
        self.summary_labels['opening'].setFont(QFont("Segoe UI", 11, QFont.Bold))
        
        layout.addWidget(opening_label)
        layout.addWidget(self.summary_labels['opening'])
        layout.addSpacing(20)

        # Total Debits
        debit_label = QLabel("إجمالي المدين:")
        debit_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.summary_labels['debit'] = QLabel("0.00")
        self.summary_labels['debit'].setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.summary_labels['debit'].setStyleSheet("color: #DC2626;")
        
        layout.addWidget(debit_label)
        layout.addWidget(self.summary_labels['debit'])
        layout.addSpacing(20)

        # Total Credits
        credit_label = QLabel("إجمالي الدائن:")
        credit_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.summary_labels['credit'] = QLabel("0.00")
        self.summary_labels['credit'].setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.summary_labels['credit'].setStyleSheet("color: #10B981;")
        
        layout.addWidget(credit_label)
        layout.addWidget(self.summary_labels['credit'])
        layout.addSpacing(20)

        # Closing Balance
        closing_label = QLabel("رصيد آخر المدة:")
        closing_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.summary_labels['closing'] = QLabel("0.00")
        self.summary_labels['closing'].setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.summary_labels['closing'].setStyleSheet("color: #2563EB;")
        
        layout.addWidget(closing_label)
        layout.addWidget(self.summary_labels['closing'])
        layout.addStretch()

        return card

    def load_data(self):
        """Load operations and populate table"""
        from_date = self.from_date.date().toPython()
        to_date = self.to_date.date().toPython()

        operations = get_operations(self.account_id)
        
        # Filter by date range
        filtered_ops = [op for op in operations 
                       if from_date <= op.date <= to_date]

        self.table.setRowCount(len(filtered_ops) + 1)

        # Opening balance row
        running_balance = 0
        for op in operations:
            if op.date < from_date:
                running_balance += (op.supplier_amount - op.payment)

        opening_balance = running_balance
        self._add_opening_balance_row(opening_balance)

        # Operation rows
        total_debits = 0
        total_credits = 0

        for i, op in enumerate(filtered_ops, start=1):
            running_balance += (op.supplier_amount - op.payment)
            total_debits += op.supplier_amount
            total_credits += op.payment

            row_data = [
                str(op.date) if op.date else "",                        # التاريخ
                op.record_number if op.record_number else "",           # رقم المحضر
                op.description if op.description else "",               # البيان
                op.item_type if op.item_type else "",                   # نوع العنصر
                f"{op.price_per_ton:.2f}" if op.price_per_ton else "",  # سعر الطن
                f"{op.gross_weight:.2f}" if op.gross_weight else "",    # الوزن قبل
                f"{op.net_weight:.2f}" if op.net_weight else "",        # الوزن بعد
                f"{op.supplier_amount:,.2f}" if op.supplier_amount else "0.00",  # مدين
                f"{op.payment:,.2f}" if op.payment else "0.00",         # دائن
                f"{running_balance:,.2f}",                               # الرصيد
                "",                                                      # ملاحظات
            ]

            for col, val in enumerate(row_data):
                cell = QTableWidgetItem(val)
                cell.setTextAlignment(Qt.AlignCenter)
                cell.setFont(QFont("Segoe UI", 10))

                # Color debit column (green)
                if col == 7 and val != "0.00":
                    cell.setBackground(QColor("#ECFDF5"))
                    cell.setForeground(QColor("#10B981"))

                # Color credit column (blue)
                if col == 8 and val != "0.00":
                    cell.setBackground(QColor("#EFF6FF"))
                    cell.setForeground(QColor("#0369A1"))

                # Color balance column
                if col == 9:
                    try:
                        balance = float(val.replace(",", ""))
                        if balance > 0:
                            cell.setBackground(QColor("#FEE2E2"))
                            cell.setForeground(QColor("#DC2626"))
                        elif balance < 0:
                            cell.setBackground(QColor("#ECFDF5"))
                            cell.setForeground(QColor("#10B981"))
                    except:
                        pass

                self.table.setItem(i, col, cell)

        # Update summary
        closing_balance = running_balance
        self.summary_labels['opening'].setText(f"{opening_balance:,.2f}")
        self.summary_labels['debit'].setText(f"{total_debits:,.2f}")
        self.summary_labels['credit'].setText(f"{total_credits:,.2f}")
        self.summary_labels['closing'].setText(f"{closing_balance:,.2f}")

    def _add_opening_balance_row(self, opening_balance):
        """Add opening balance row"""
        opening_item = QTableWidgetItem("رصيد أول المدة")
        opening_item.setTextAlignment(Qt.AlignCenter)
        opening_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
        opening_item.setBackground(QColor("#FEF3C7"))
        opening_item.setForeground(QColor("#9333EA"))
        self.table.setItem(0, 0, opening_item)

        # Balance in column 9
        balance_item = QTableWidgetItem(f"{opening_balance:,.2f}")
        balance_item.setTextAlignment(Qt.AlignCenter)
        balance_item.setFont(QFont("Segoe UI", 11, QFont.Bold))
        balance_item.setBackground(QColor("#FEF3C7"))
        self.table.setItem(0, 9, balance_item)

        # Rest of opening balance row
        for col in range(1, 9):
            if col != 9:
                cell = QTableWidgetItem("")
                cell.setBackground(QColor("#FEF3C7"))
                self.table.setItem(0, col, cell)
