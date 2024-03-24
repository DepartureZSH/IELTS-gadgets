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
        self.style()

    def Constants(self):
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.IELTS2 = os.listdir(self.dir_path + f"\\Public\\corpus\\IELTS2\\")
        random.shuffle(self.IELTS2)
        self.IELTS2_path = self.dir_path + f"\\Public\\corpus\\IELTS2\\{self.IELTS2[0]}"
        self.temp_path = self.dir_path + f"\\Public\\Temps\\"
        self.raw_msgs = []
        self.duration = []
        with open(self.IELTS2_path, "r", encoding='gb18030', errors='ignore') as f:
            self.raw_msgs = f.readlines()

    def shuffle(self):
        msgs = ["""
            Now in this second part I’m going to give you a topic and I’d like you to talk about it for one to two minutes. 
            Before you talk you’ll have one minute to think about what you’re going to say you can make some notes if you wish.
            Do you understand? So here’s pen and paper for making notes,here’s your topic. {}
            """.format(self.raw_msgs[0]), "Time is up. Can you start speaking now, please?", "Now you have one minute left."]
        self.trans.set_Property(msgs)
        self.clear_Temp()

    def widgets(self):
        self.trans = transformer()
        self.trans.duration_signal.connect(self.set_duration)
        self.Cleaner = Cleaner()
        self.IELTS2_VIEW = QWidget()
        self.IELtSPart2 = QTextBrowser()

    def show(self):
        self.shuffle()
        self.trans.start()

    def set_duration(self, duration):
        self.duration = duration
        wav_list = [self.dir_path + "\\Public\\Temps\\" + file for file in os.listdir(self.temp_path)]
        self.player = player("IELTS2", wav_list, 60)

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

    def clear_Temp(self):
        self.Cleaner.start()
        # for outfile in os.listdir(self.temp_path):
        #     try:
        #         if os.path.exists("{}\\{}".format(self.temp_path, outfile)):
        #             os.remove("{}\\{}".format(self.temp_path, outfile))
        #     except Exception as e:
        #         print(str(e))
        # print("文件删除完毕")

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
        '''
        self.setStyleSheet(qssStyle)
        title = QFont()
        title.setPointSize(15)
        title.setBold(True)
        self.IELtSPart2.setFont(title)
        self.center(self)

    # 居中
    def center(self, widget):
        screen = QDesktopWidget().screenGeometry()
        size = widget.geometry()
        widget.move((screen.width() - size.width()) / 2,
                    (screen.height() - size.height()) / 2)

    def closeEvent(self, a0: QCloseEvent) -> None:
        super().closeEvent(a0)
        self.clear_Temp()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
