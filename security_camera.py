"""
camara.py

When motion is detected by web camera, post it to Slack channel.
"""

import datetime
import io
import os
import sys

import cv2
import numpy as np
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
import requests

import settings


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        exit_action = QtWidgets.QAction('&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(sys.exit)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(exit_action)

        self.statusBar().showMessage(
            'Push SPACE to register a background image.')


class VideoCaptureView(QtWidgets.QGraphicsView):
    repeat_interval = 33  # ms

    def __init__(self, parent=None):
        super(VideoCaptureView, self).__init__(parent)

        self.pixmap = None
        self.item = None
        self.background = None

        self.previous_detect_time = datetime.datetime(
            2000, 1, 1)  # For calc last detectin
        self.time_delta = datetime.timedelta(seconds=10)

        self.capture = cv2.VideoCapture(0)

        # Initialize drawing canvas
        self.scene = QtWidgets.QGraphicsScene()
        self.setScene(self.scene)

        self.set_video_image()

        # Update timer constantly
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.set_video_image)
        self.timer.start(self.repeat_interval)

    def set_video_image(self):
        status, self.frame = self.capture.read()

        if not status:
            print('Could not read frame.')
            sys.exit()

        if self.background is not None:
            if self.is_detect_background_subtraction():

                print('Detect motion!')
                self.now = datetime.datetime.now()
                if self.now - self.previous_detect_time > self.time_delta:
                    self.send_alert()
                    self.previous_detect_time = self.now

        height, width, dim = self.frame.shape
        bytes_per_line = dim * width

        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.image = QtGui.QImage(self.frame.data, width, height,
                                  bytes_per_line, QtGui.QImage.Format_RGB888)

        if self.pixmap is None:  # Fist, make instance.
            self.pixmap = QtGui.QPixmap.fromImage(self.image)
            self.item = QtWidgets.QGraphicsPixmapItem(self.pixmap)
            self.scene.addItem(self.item)  # Arrange on canvas
        else:
            # Second or later, change settings.
            self.pixmap.convertFromImage(self.image)
            self.item.setPixmap(self.pixmap)

    def is_detect_background_subtraction(self):
        """
        Extract the difference between the registered background image and the current frame.

        Returns:
            [bool]: Whether a difference was detected
        """

        fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
        fgmask = fgbg.apply(self.background)
        fgmask = fgbg.apply(self.frame)

        fgmask = fgmask / 255
        height, width = fgmask.shape

        threshold_rate = 0.1

        if fgmask.sum() > height * width * threshold_rate:
            return True
        else:
            return False

    def send_alert(self):
        """
        Executed when a difference is detected.
        Send alert with an image now on frame to Slack.
        """

        result, encimg = cv2.imencode(
            '.jpg', self.frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

        if result:
            files = {'file': io.BytesIO(encimg)}

            payload = {
                'token': settings.slack_api_token,
                'channels': settings.slack_channel_id,
                'initial_comment': 'Detect motion!' + ' ' + self.now.strftime('%H:%M:%S')}

            requests.post(
                url='https://slack.com/api/files.upload',
                params=payload,
                files=files)

    def keyPressEvent(self, event):
        """
        Override QtWidgets.QGraphicsView.keyPressEvent.
        If space key pushed, register a background image.
        """

        key = event.key()
        if key == QtCore.Qt.Key_Space:
            self.background = self.frame
            print('Successful registration of background image.')

        super(VideoCaptureView, self).keyPressEvent(event)


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)

    main_window = MainWindow()
    main_window.setWindowTitle('Security Camera')
    main_window.move(480, 270)

    video_capture_view = VideoCaptureView()

    main_window.setCentralWidget(video_capture_view)
    main_window.show()

    app.exec_()

    video_capture_view.capture.release()


if __name__ == '__main__':
    main()
