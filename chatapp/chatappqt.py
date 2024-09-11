from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap
import sys

class Window(QWidget):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("imagelabel")
		self.setGeometry(200,200, 500,400)

		label = QLabel("this is the QLabel")


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())