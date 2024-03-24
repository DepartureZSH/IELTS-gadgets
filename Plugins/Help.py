import pyttsx3
import time
import random
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.setWindowTitle("Help")
        self.resize(600, 600)
        self.helpBrowser = QTextBrowser()
        Vbox = QVBoxLayout()
        Vbox.addWidget(self.helpBrowser)
        self.setLayout(Vbox)
        content = """本桌面旨在模拟雅思或其他口语考试，以下是相关QA：
Q1. 如何进行一场IELTS口语模拟考试？
A1. step1点击打开摄像头按钮，step2点击IELTS口语考试按钮，step3进入IELTS口语考试流程。

Q2. 如何进行专项口语模拟训练？
A2. 本程序设计了四种专项口语训练：即IELTS Part1-3和一问一答快速测试。IELTS Part1-3按钮分别对应雅思口语第1-3部分；一问一答快速测试按钮对应“自定义文件”中的题目。

需要注意的是，每次训练过程中，IELTS Part1会随机抽取10道题，IELTS Part2-3会在同一类题目下随机出题，而一问一答快速测试会随机地在“自定义文件”中选择一题。

Q3. 题库在哪里？
A3. 题库在本文件夹的 corpus/ 目录中。IELTS1文件夹对应IELTS Part1，依此类推；而QuickTest文件夹对应一问一答快速测试题库。

Tips: 如非专业人员，请勿更改以上文件目录和文件名！可以在txt文件中进行增删改查。

Q4. 如何更换题库？
A4. 在对应文件目录的txt文件中进行增删改查。注意事项：
    1. 文本是否粘贴正确、是否有特殊符号；
    2. IELTS Part1、IELTS Part3和QuickTest保持每条问题占一行；
    3. 请仔细检查是否留有空行，如果存在空行，请删除；
    4. IELTS Part2、IELTS Part3文件名一一对应，如IELTS2/test1.txt与IELTS3/test1.txt都对应同一个问题；
QuickTest更换题库示例：
    step1 打开本文件夹相对路径corpus/QuickTest/Test.txt文件；
    step2 以原文件内容格式举一反三，更新题库内容；
    step3 保存文件，题库更新完毕。
IELTS Part2、IELTS Part3更换题库示例，以Test2.txt为例：
    step1 打开本文件夹相对路径corpus/IELTS2/Test1.txt文件；
    step2 以Test1.txt文件内容格式举一反三，在 corpus/IELTS2/ 目录下创建并更新Test2.txt文件；
    step3 保存文件，IELTS2题库更新完毕；
    step4 打开本文件夹相对路径corpus/IELTS3/Test1.txt文件；
    step5 以Test1.txt文件内容格式举一反三，在 corpus/IELTS2/ 目录下创建并更新对应Test2.txt文件；
    step6 保存文件，IELTS3题库更新完毕。

Q5 如何调整音量、语速和合成器？
A5  step1 打开本文件夹相对路径settings/speaker.json文件；
    step2 更改音量（volume）；更改语速 （rate）； 更改合成器 （voice）；
    step3 重启应用。

Tips：volume值在0.0-1.0，rate：200代表2倍速，合成器数量与配置各电脑不同，通常0-3
                """
        self.helpBrowser.append(content)
        self.style()

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

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     demo = Demo()
#     qssStyle = '''
#         *{
#             border: none;
#             background-color:rgb(225,225,225);
#         }
#         QWidget[name='menu'] {
#             border:none;
#             border-radius:10px;
#             background-color:rgb(225,225,225);
#         }
#         QPushButton {
#           display: inline-block;
#           padding: 10px 10px;
#           border-radius: 8px;
#           background-color:rgb(255,255,255);
#           font-size: 16px;
#           font-weight: bold;
#           text-align: center;
#           text-decoration: none;
#           text-transform: uppercase;
#           box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
#           transition: background-color 0.3s ease;
#         }
#         QPushButton:hover {
#             background-color: rgb(235,235,235);
#         }
#     '''
#     demo.setStyleSheet(qssStyle)
#     demo.show()
#     sys.exit(app.exec_())