from __future__ import print_function
import argparse
import cv2 as cv

class Trackbar:
    max_value = 255
    max_value_H = 360//2
    low_H = 15
    low_S = 100
    low_V = 100
    high_H = 50
    high_S = max_value
    high_V = max_value
    window_capture_name = 'Video Capture'
    window_detection_name = 'Object Detection'
    low_H_name = 'Low H'
    low_S_name = 'Low S'
    low_V_name = 'Low V'
    high_H_name = 'High H'
    high_S_name = 'High S'
    high_V_name = 'High V'

    def __init__(self):
        pass

    def getLowH(self):
        return self.low_H

    def getLowS(self):
        return self.low_S

    def getLowV(self):
        return self.low_V

    def getHighH(self):
        return self.high_H

    def getHighS(self):
        return self.high_S

    def getHighV(self):
        return self.high_V

    def on_low_H_thresh_trackbar(self, val):
        low_H = val
        self.low_H = min(self.high_H, low_H)
        cv.setTrackbarPos(self.low_H_name, self.window_detection_name, self.low_H)

    def on_high_H_thresh_trackbar(self, val):
        high_H = val
        self.high_H = max(high_H, self.low_H)
        cv.setTrackbarPos(self.high_H_name, self.window_detection_name, self.high_H)

    def on_low_S_thresh_trackbar(self, val):
        low_S = val
        self.low_S = min(self.high_S, low_S)
        cv.setTrackbarPos(self.low_S_name, self.window_detection_name, self.low_S)

    def on_high_S_thresh_trackbar(self, val):
        high_S = val
        self.high_S = max(high_S, self.low_S)
        cv.setTrackbarPos(self.high_S_name, self.window_detection_name, self.high_S)

    def on_low_V_thresh_trackbar(self, val):
        low_V = val
        self.low_V = min(self.high_V, low_V)
        cv.setTrackbarPos(self.low_V_name, self.window_detection_name, self.low_V)

    def on_high_V_thresh_trackbar(self, val):
        high_V = val
        self.high_V = max(high_V, self.low_V)
        cv.setTrackbarPos(self.high_V_name, self.window_detection_name, self.high_V)

    def setTrackbar(self):
        print("Max Value H: ", self.max_value_H)
        parser = argparse.ArgumentParser(description='Code for Thresholding Operations using inRange tutorial.')
        parser.add_argument('--camera', help='Camera divide number.', default=0, type=int)
        cv.namedWindow(self.window_detection_name)

        cv.createTrackbar(self.low_H_name, self.window_detection_name, self.low_H, self.max_value_H, self.on_low_H_thresh_trackbar)
        cv.createTrackbar(self.high_H_name, self.window_detection_name, self.high_H, self.max_value_H, self.on_high_H_thresh_trackbar)
        cv.createTrackbar(self.low_S_name, self.window_detection_name, self.low_S, self.max_value, self.on_low_S_thresh_trackbar)
        cv.createTrackbar(self.high_S_name, self.window_detection_name, self.high_S, self.max_value, self.on_high_S_thresh_trackbar)
        cv.createTrackbar(self.low_V_name, self.window_detection_name, self.low_V, self.max_value, self.on_low_V_thresh_trackbar)
        cv.createTrackbar(self.high_V_name, self.window_detection_name, self.high_V, self.max_value, self.on_high_V_thresh_trackbar)