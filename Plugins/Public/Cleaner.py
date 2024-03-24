import os
import pyttsx3
import time
import random
from threading import Thread
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

class Cleaner(QThread):
    status_signal = pyqtSignal(bool)

    def __init__(self):
        super(Cleaner, self).__init__()
        self.dir_path = os.path.dirname(os.path.abspath(__file__))

    def run(self):
        for file in os.listdir(self.dir_path + f"\\Temps\\"):
            try:
                if os.path.exists(self.dir_path + f"\\Temps\\{file}"):
                    os.remove(self.dir_path + f"\\Temps\\{file}")
            except Exception as e:
                print("run ", str(e))
        # print("文件删除完毕")
