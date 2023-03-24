import sys

from PyQt6.QtWidgets import QApplication

from src.data import session
from src.interface import dashboard

if __name__ == "__main__":
    app = QApplication(sys.argv)

    session = session.Session("BS220 - Integrated Project")
    window = dashboard.Main(session)

    window.show()
    app.exec()
