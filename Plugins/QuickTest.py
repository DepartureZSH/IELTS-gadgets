import os
import time
import random
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
try:
    from Public.Transformer import transformer
    from Public.Player import player
    from Public.Cleaner import Cleaner
except:
    from .Public.Transformer import transformer
    from .Public.Player import player
    from .Public.Cleaner import Cleaner

class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.widgets()
        self.Constants()

    def Constants(self):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.QuickTest_path = self.dir_path + f"\\public\\corpus\\QuickTest\\Test.txt"
        self.temp_path = self.dir_path + f"\\public\\Temps\\"
        self.count = 1
        self.raw_msgs = []
        self.duration = []
        with open(self.QuickTest_path, "r", encoding='gb18030', errors='ignore') as f:
            self.raw_msgs = f.readlines()

    def shuffle(self):
        random.shuffle(self.raw_msgs)
        msgs = [self.raw_msgs[0]]
        self.trans.set_Property(msgs)
        self.clear_Temp()

    def widgets(self):
        self.trans = transformer()
        self.trans.duration_signal.connect(self.set_duration)
        self.Cleaner = Cleaner()

    def show(self):
        self.shuffle()
        self.trans.start()

    def set_duration(self, duration):
        self.duration = duration
        wav_list = [self.dir_path + "\\Public\\Temps\\" + file for file in os.listdir(self.temp_path)]
        self.player = player("IELTS1", wav_list, 30)
        self.player.show()

    def clear_Temp(self):
        for outfile in os.listdir(self.temp_path):
            try:
                if os.path.exists("{}\\{}".format(self.temp_path, outfile)):
                    os.remove("{}\\{}".format(self.temp_path, outfile))
            except Exception as e:
                print(str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
