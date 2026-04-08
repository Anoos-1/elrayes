APP_STYLE = """
/* ===== Global ===== */
QWidget {
    background-color: #f5f6fa;
    font-family: Arial;
    font-size: 14px;
    color: #2c3e50;
}

/* ===== Labels ===== */
QLabel {
    color: #2c3e50;
    font-weight: bold;
}

/* ===== LineEdits & Combo ===== */
QLineEdit, QComboBox, QDateEdit {
    background-color: #ffffff;
    color: #2c3e50;
    border: 1px solid #dcdde1;
    border-radius: 6px;
    padding: 6px;
    min-height: 28px;
}

/* ===== GroupBox ===== */
QGroupBox {
    font-size: 14px;
    font-weight: bold;
    color: #2c3e50;
    border: 2px solid #c0392b;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 18px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 6px;
    color: #c0392b;
}

/* ===== Buttons ===== */
QPushButton {
    background-color: #c0392b;
    color: white;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #a93226;
}

QPushButton:pressed {
    background-color: #7b241c;
}

QPushButton#saveBtn {
    background-color: #27ae60;
}

QPushButton#saveBtn:hover {
    background-color: #1e874b;
}

/* ===== Table ===== */
QTableWidget {
    background-color: white;
    alternate-background-color: #fef9e7;
    gridline-color: #dcdde1;
    border: 1px solid #dcdde1;
    color: #2c3e50;
}

QTableWidget::item {
    padding: 6px;
}

QHeaderView::section {
    background-color: #c0392b;
    color: white;
    padding: 8px;
    font-weight: bold;
    border: none;
}

/* ===== Tab Widget ===== */
QTabWidget::pane {
    border: 1px solid #bdc3c7;
}

QTabBar::tab {
    background: #ecf0f1;
    color: #2c3e50;
    padding: 8px 18px;
    margin-right: 2px;
    font-weight: bold;
    border: 1px solid #bdc3c7;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
}

QTabBar::tab:selected {
    background: white;
    color: #c0392b;
    border-bottom: 2px solid #c0392b;
}

/* ===== Combo Arrow ===== */
QComboBox QAbstractItemView {
    background-color: white;
    color: #2c3e50;
    selection-background-color: #c0392b;
    selection-color: white;
}
"""
