import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow

from database.db import create_database


def main():

    create_database()

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()