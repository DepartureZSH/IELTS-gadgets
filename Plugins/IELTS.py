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
    from IELTS1 import Demo as IELTS1_Demo
except:
    from .Public.Transformer import transformer
    from .Public.Player import player
    from .Public.Cleaner import Cleaner
    from .IELTS1 import Demo as IELTS1_Demo


class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.setWindowTitle("IELTS Test")
        self.resize(600, 600)
        self.Constants()
        self.widgets()
        self.style()

    def Constants(self):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.IELTS1 = IELTS1_Demo()
        self.temp_path = self.dir_path + f"\\Public\\Temps\\"
        self.Part = 0

    def widgets(self):
        self.trans = transformer()
        self.Cleaner = Cleaner()
        self.IELTS2_VIEW = QWidget()
        self.IELtSPart2 = QTextBrowser()
        self.trans.duration_signal.connect(self.set_duration)

    def show(self):
        self.IELTS1.show()
        self.Part = 1
        self.IELTS1.close_Signal.connect(self.showIELTS2)
        self.IELTS2_3 = os.listdir(self.dir_path + f"\\public\\corpus\\IELTS2\\")
        random.shuffle(self.IELTS2_3)
        self.IELTS2_path = self.dir_path + f"\\public\\corpus\\IELTS2\\{self.IELTS2_3[0]}"
        self.IELTS3_path = self.dir_path + f"\\public\\corpus\\IELTS3\\{self.IELTS2_3[0]}"
        self.QuickTest_path = self.dir_path + f"\\public\\corpus\\IELTS1\\Test.txt"


    def showIELTS2(self):
        print("showIELTS2  self.Part:", self.Part)
        self.IELTS1.close_Signal.disconnect(self.showIELTS2)
        self.clear_Temp()
        self.IELTS2_3 = os.listdir(self.dir_path + f"\\Public\\corpus\\IELTS2\\")
        random.shuffle(self.IELTS2_3)
        self.IELTS2_path = self.dir_path + f"\\Public\\corpus\\IELTS2\\{self.IELTS2_3[0]}"
        self.IELTS3_path = self.dir_path + f"\\Public\\corpus\\IELTS3\\{self.IELTS2_3[0]}"
        self.raw_msgs = []
        self.duration = []
        with open(self.IELTS2_path, "r", encoding='gb18030', errors='ignore') as f:
            self.raw_msgs = f.readlines()

        msgs = ["""Now in this second part I’m going to give you a topic and I’d like you to talk about it for one to two minutes. 
        Before you talk you’ll have one minute to think about what you’re going to say you can make some notes if you wish.
        Do you understand? So here’s pen and paper for making notes,here’s your topic. {}
                """.format(self.raw_msgs[0]), "Time is up. Can you start speaking now, please?", "Now you have one minute left."]
        self.trans.set_Property(msgs)
        self.trans.start()
        print("showIELTS2 down self.Part:", self.Part)

    def showIELTS3(self):
        self.player.close_Signal.disconnect(self.showIELTS3)
        self.IELTS2_VIEW.close()
        self.clear_Temp()
        msgs = ["""Now in the third part I’m going to give you several topics and I’d like you to talk about them, each of them for about half a minute. 
        Here is the first question. """]
        with open(self.IELTS3_path, "r", encoding='gb18030', errors='ignore') as f:
            self.raw_msgs = f.readlines()
        random.shuffle(self.raw_msgs)
        msgs[0] = msgs[0] + self.raw_msgs[0]
        msgs.extend(self.raw_msgs[1:])
        self.trans.set_Property(msgs)
        self.trans.start()

    def set_duration(self, duration):
        print("set_duration self.Part:", self.Part)
        self.duration = duration
        wav_list = [self.dir_path + "\\Public\\Temps\\" + file for file in os.listdir(self.temp_path)]
        if self.Part == 1:
            self.player = player("IELTS2", wav_list, 60)
            self.player.close_Signal.connect(self.showIELTS3)
            for each in self.raw_msgs:
                self.IELtSPart2.append(each)
            self.HBox = QHBoxLayout()
            self.HBox.addWidget(self.player)
            self.HBox.addWidget(self.IELtSPart2)
            self.IELTS2_VIEW.setLayout(self.HBox)
            self.IELTS2_VIEW.setWindowTitle("IELTS Test")
            self.IELTS2_VIEW.resize(1200, 600)
            self.IELTS2_VIEW.setWindowIcon(QIcon(self.dir_path + '\\Public\\images\\title.png'))
            self.IELTS2_VIEW.show()
            self.Part = 2
        elif self.Part == 2:
            self.player3 = player("IELTS3", wav_list, 30)
            self.player3.close_Signal.connect(self.exit)
            self.player3.show()
            self.Part = 3

    def exit(self):
        self.close()

    def clear_Temp(self):
        self.Cleaner.start()

    def style(self):
        qssStyle = '''
            *{
                border: none;
                background-color:rgb(225,225,225);
            }
            QWidget[name='menu'] {
                border:none; 
                border-radius:10px; 
                background-color:rgb(225,225,225);
            }
            QPushButton {
              display: inline-block;
              padding: 10px 10px;
              border-radius: 8px;
              background-color:rgb(255,255,255);
              font-size: 16px;
              font-weight: bold;
              text-align: center;
              text-decoration: none;
              text-transform: uppercase;
              box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
              transition: background-color 0.3s ease;
            }
            QPushButton:hover {
                background-color: rgb(235,235,235);
            }
        '''
        self.setStyleSheet(qssStyle)
        self.center(self)

    # 居中
    def center(self, widget):
        screen = QDesktopWidget().screenGeometry()
        size = widget.geometry()
        widget.move((screen.width() - size.width()) / 2,
                    (screen.height() - size.height()) / 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
