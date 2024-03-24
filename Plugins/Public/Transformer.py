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

import numpy as np
import cv2
import json
import wave



class transformer(QThread):
    duration_signal = pyqtSignal(list)

    def __init__(self):
        super(transformer, self).__init__()
        self.speaker = pyttsx3.init()
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.speaker_json = self.dir_path + "/settings/speaker.json"

    def set_Property(self, msgs):
        self.msgs = msgs
        self.duration_time = []
        with open(self.speaker_json, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            voices = self.speaker.getProperty('voices')
            self.speaker.setProperty('voice', voices[settings['voice']].id)
            self.speaker.setProperty('rate', settings['rate'])
            self.speaker.setProperty('volume', settings['volume'])

    def run(self):
        try:
            for i in range(len(self.msgs)):
                outfile = self.dir_path + f"/Temps/temp{i}.wav"
                self.speaker.save_to_file(self.msgs[i], outfile)
                self.speaker.runAndWait()
                self.duration_time.append(int(self.get_duration_wave(outfile)))
            self.duration_signal.emit(self.duration_time)
        except Exception as e:
            print(str(e))
            return

    # 获得问题持续时间
    def get_duration_wave(self, file_path):
        with wave.open(file_path, 'r') as audio_file:
            frame_rate = audio_file.getframerate()
            n_frames = audio_file.getnframes()
            duration = n_frames / float(frame_rate)
            return duration
