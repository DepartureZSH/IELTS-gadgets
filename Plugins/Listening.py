import os
import time
import random
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
try:
    from Public.ListeningPlayer import player
except:
    from .Public.ListeningPlayer import player

class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.Constants()
        self.widgets()

    def Constants(self):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.Listening = os.listdir(self.dir_path + f"\\Public\\corpus\\Listening\\")
        self.duration = []

    def widgets(self):
        wav_list = [self.dir_path + f"\\Public\\corpus\\Listening\\" + each for each in self.Listening]
        self.player = player("Listening", wav_list)

    def show(self):
        self.player.show()

    def closeEvent(self, a0: QCloseEvent) -> None:
        super().closeEvent(a0)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
