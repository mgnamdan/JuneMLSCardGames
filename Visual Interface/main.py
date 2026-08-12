# This file contains the application startup for the visual card games
import sys

from PyQt6.QtWidgets import QApplication

from interface import CardGameWindow, setApplicationFont


def main():
    app = QApplication(sys.argv)
    setApplicationFont(app)
    window = CardGameWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
