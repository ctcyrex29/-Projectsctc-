from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QPixmap

window = QWidget()

label = QLabel(window)
label.setClickable(true)
label.setPixmap(QPixmap("CLIENTBUTTON.png"))
label.setBorderlmage(QPixmap(Qlmage(200, 200)))