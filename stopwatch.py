import time
import threading

from PyQt5 import uic
from PyQt5.QtWidgets import *


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("stopwatch.ui", self)
        self.show()


        self.running = False #is it running currently
        self.started = False #did the stopwatch even start

        self.passed = 0 #seconds passed
        self.previous_passed = 0
        self.lap = 1

        self.Start.clicked.connect(self.start_stop)
        self.Lap.clicked.connect(self.lap_reset)
        self.label.setStyleSheet("border: 10px solid transparent")


    def start_stop(self):
        if self.running:
            self.running = False
            self.Start.setText("Resume")
            self.Lap.setText("Reset")
        else:
            self.running = True
            self.Start.setText("Stop")
            self.Lap.setText("Lap")
            self.Lap.setEnabled(True)
            threading.Thread(target=self.stopwatch).start()

    def lap_reset(self):
        if self.running:
            self.label.setText(self.label.text() + f"(Lap {self.lap} - Passed: {self.format_time_string(self.passed)}" f" - Difference: {self.format_time_string(self.passed - self.previous_passed)})") 
            self.lap += 1
            self.prevous_passed = self.passed
        else:
            self.Start.setText("Start")
            self.Lap.setText("Lap")
            self.Lap.setEnabled(False)
            self.label_2.setText("00:00:00:00")
            self.label.setText("Laps: ")
            self.lap = 1
            self.passed = 0
            self.previous_passed = 0

    def format_time_string(self, time_passed):
        secs = time_passed % 60
        mins = time_passed // 60
        hours = mins // 60
        return f"{int(hours):02d}:{int(mins):02d}:{int(secs):02d}:{int((self.passed%1) * 100):02d}"



    def stopwatch(self):
        start = time.time()
        if self.started:
            until_now = self.passed
        else: #started for first time
            until_now = 0
            self.started = True
        
        while self.running:
            self.passed = time.time() - start + until_now
            self.label_2.setText(self.format_time_string(self.passed))



def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()


if __name__ == "__main__":
    main()
