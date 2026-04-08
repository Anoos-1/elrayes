import sys
from PySide6.QtWidgets import QApplication
from db import Base, engine
from ui.main_window import MainWindow
from ui.style import APP_STYLE

# Import models to register them with SQLAlchemy
from models import *

# Create tables
Base.metadata.create_all(engine)

app = QApplication(sys.argv)
app.setStyleSheet(APP_STYLE)

window = MainWindow()
window.show()

sys.exit(app.exec())