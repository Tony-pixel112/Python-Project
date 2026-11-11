import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.resize(800, 600)
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.png")
        self.setWindowIcon(QIcon(icon_path))

        label = QLabel("Hello World", self)
        label.setFont(QFont("Arial", 30))
        label.setGeometry(0, 0, 500, 100)
        label.setStyleSheet("color: red;"
                            "background-color: #d4814e;"
                            "font-weight: bold;"
                            "font-style: italic;"
                            "text-decoration: underline;")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()