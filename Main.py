import os

import time
import random
from threading import Thread
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

import numpy as np
import cv2
import json
import wave

from importlib import import_module
from functools import partial

class CameraPageWindow(QWidget):
    def __init__(self, parent=None):
        super(CameraPageWindow, self).__init__(parent)
        self.setWindowTitle("Oral Test")
        self.resize(1000, 700)
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.timer_camera = QTimer()  # 初始化定时器
        self.timer_Player = QTimer()  # 初始化定时器
        self.cap = cv2.VideoCapture()  # 初始化摄像头
        self.constants()
        self.setupUi()
        self.plugins()
        self.initUI()
        self.slot_init()
        self.style_init()

    ####################################################################################
    def constants(self):
        self.CAM_NUM = 0
        self.delay = [5, 30, 60, 30, 30]

    def plugins(self):
        self.Plugin_Buttons = []
        with open("settings/Plugins.json", 'r', encoding='utf-8') as f:
            settings = json.load(f)
            for key, value in settings.items():
                try:
                    exec("self.%s = getattr(import_module(name='.%s', package='Plugins'), '%s')()" % (value["Name"], key, value["Module"]))
                    exec("self.%s = QPushButton('%s')" % (value["Button_name"], value["Button_text"]))
                    exec("self.%s.clicked.connect(partial(self.btn_func, '%s'))" % (value["Button_name"], value["Name"]))
                    self.Plugin_Buttons.append(value["Button_name"])
                except Exception as e:
                    print(str(e))

    def setupUi(self):
        self.ButtonList = QWidget()
        self.ButtonList_init()
        self.cameraLabel1 = QLabel()
        self.cameraLabel1.setPixmap(QPixmap(self.dir_path + "\images\Examer.jpg"))
        self.cameraLabel1.resize(QSize(480, 320))
        self.cameraLabel1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cameraLabel2 = QLabel()
        self.cameraLabel2.setPixmap(QPixmap(self.dir_path + "\images\Examee.jpg"))
        self.cameraLabel2.resize(QSize(480, 320))
        self.cameraLabel2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 退出界面
        self.message_box = QMessageBox()
        self.message_box.setText("确认退出?")
        self.message_box.addButton("Yes", QMessageBox.YesRole)
        self.message_box.addButton("No", QMessageBox.NoRole)

    def ButtonList_init(self):
        self.plugins()
        VBox = QVBoxLayout()
        for Button in self.Plugin_Buttons:
            exec("VBox.addWidget(self.%s)" % Button)
        vSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        VBox.addItem(vSpacer)
        self.cameraButton = QPushButton("打开摄像头")
        self.exitButton = QPushButton("退出")
        VBox.addWidget(self.cameraButton)
        VBox.addWidget(self.exitButton)
        self.ButtonList.setLayout(VBox)
        self.ButtonList.setContentsMargins(0, 0, 0, 0)

    def initUI(self):
        HBox = QHBoxLayout()
        HBox.addWidget(self.ButtonList)
        HBox.addWidget(self.cameraLabel1)
        HBox.addWidget(self.cameraLabel2)
        self.setLayout(HBox)

    def slot_init(self):
        self.timer_camera.timeout.connect(self.show_camera)
        self.cameraButton.clicked.connect(self.slotCameraButton)
        self.exitButton.clicked.connect(self.exit)

    ####################################################################################
    def show_camera(self):
        flag, self.image = self.cap.read()
        self.cameraLabel1.resize(QSize(self.image.shape[1], self.image.shape[0]))
        show = self.image
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        show = cv2.flip(show, 1)
        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        self.cameraLabel1.setPixmap(QPixmap.fromImage(showImage))

    # 打开关闭摄像头控制
    def slotCameraButton(self):
        if not self.timer_camera.isActive():
            # 打开摄像头并显示图像信息
            self.openCamera()
        else:
            # 关闭摄像头并清空显示信息
            self.closeCamera()

    # 打开摄像头
    def openCamera(self):
        flag = self.cap.open(self.CAM_NUM)
        if not flag:
            msg = QMessageBox.warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
                                      buttons=QMessageBox.Ok,
                                      defaultButton=QMessageBox.Ok)
        else:
            self.timer_camera.start(30)
            self.cameraButton.setText('关闭摄像头')

    # 关闭摄像头
    def closeCamera(self):
        self.timer_camera.stop()
        self.cap.release()
        self.cameraLabel1.clear()
        self.cameraButton.setText('打开摄像头')
        self.cameraLabel1.setPixmap(QPixmap(self.dir_path + "\images\Examer.jpg"))

    ####################################################################################

    def btn_func(self, btn):
        try:
            exec("self.%s.show()" % btn)
        except Exception as e:
            print(str(e))

    def exit(self):
        res = self.message_box.exec_()
        if res == 0:
            self.close()

    def style_init(self):
        self.setWindowIcon(QIcon(self.dir_path + "\images/title.png"))
        self.center(self)

    # 居中
    def center(self, widget):
        screen = QDesktopWidget().screenGeometry()
        size = widget.geometry()
        widget.move((screen.width() - size.width()) / 2,
                    (screen.height() - size.height()) / 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = CameraPageWindow()
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
          padding: 10px 10px;
          border-radius: 8px;
          background-color:rgb(255,255,255);
          font-size: 16px;
          font-weight: bold;
          text-align: center;
          text-decoration: none;
          text-transform: uppercase;
        }
        QPushButton:hover {
            background-color: rgb(235,235,235);
        }
    '''
    # """
    #     display: inline-block;
    #     box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
    #     transition: background-color 0.3s ease;
    # """
    demo.setStyleSheet(qssStyle)
    demo.show()
    sys.exit(app.exec_())
