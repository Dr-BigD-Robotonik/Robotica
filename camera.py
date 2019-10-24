from __future__ import print_function
import cv2 as cv
import numpy as np
import scipy.interpolate
from trackbar import Trackbar


#capture video 2 . Infatti lo usiamo per il comando cv.VideoCapture(numero_dispositivo)
#il numero del dispositivo possiamo andarcelo a cercare o potremmo fare un for che ci percorra tutti i dispositivi

class CameraImage:

    #Non credo di dove spiegare che e' sta classe
    def __init__(self, device_num):
        self.__devid = device_num
        self.dev = cv.VideoCapture(device_num)

    #Se la camera non e' aperta devo aprirla altrimenti non posso leggere quello che mi restituisce.
    def setup(self):
        if not self.dev.isOpened():
            self.dev.open(self.__devid)
            #Il doppio underscore serve per utilizzare un parametro "protetto"

    #Devo adesso quindi LEGGERE l'immagine che sta leggendo la camera.
    def get_image(self, gray=True):
        ret, frame = self.dev.read()
        #print("Il valore ret e': ", ret)
        #restituisce due valori: ... e il frame che dovremo leggere
        if ret:
            if gray:
                frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
                #lower_bound = np.array([20, 100, 100])
                #upper_bound = np.array([80, 255, 255])
                print("High H: ", trackbar.getHighH())
                print("High S: ", trackbar.getHighS())
                print("High V: ", trackbar.getHighV())
                print("Low H: ", trackbar.getLowH())
                print("Low S: ", trackbar.getLowS())
                print("Low V: ", trackbar.getLowV())
                frame = cv.inRange(frame, (trackbar.getLowH(), trackbar.getLowS(), trackbar.getLowV()),
                                   (trackbar.getHighH(), trackbar.getHighS(), trackbar.getHighV()))
                filtered_image = cv.medianBlur(frame, 9)
                #filtered_image = cv.GaussianBlur(frame, (5, 5), 0.0)
                contours, hierarchy = cv.findContours(filtered_image, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
                contours = sorted(contours, key=cv.contourArea, reverse=True)[:5]  # get largest five contour area
                rects = []

                for contour in contours:
                    perim = cv.arcLength(contour, True)
                    approx = cv.approxPolyDP(contour, 0.02 * perim, True)
                    x, y, w, h = cv.boundingRect(approx)  # Get the 4 points of the bounding rectangle
                    rect = (x, y, w, h)
                    rects.append(rect)
                    cv.rectangle(filtered_image, (x, y), (x + w, y + h), (255, 255, 255), 2)
                    c = max(contours, key=cv.contourArea)
                    area = cv.contourArea(c)
                    print("AREA: ", area)
                    distance = findDistance(area)
                    print("DISTANCE: ", distance)
                    cv.putText(filtered_image, "%.2fcm" % distance,
                                (filtered_image.shape[1] - 200, filtered_image.shape[0] - 20), cv.FONT_HERSHEY_SIMPLEX,
                                2.0, (128, 255, 128), 2)
            return filtered_image
        return None
        #None = null (NoneType) per ritornare il niente nel caso non sappiamo cosa ci sia li dentro.

#Per lanciare l'immagine potremo anche essere in grado di "aprire l'immagine"
#Per catturare un video dovremo utilizzare un While(true) che continua a prendere frame, ma dovremo inserire una cv.waitkey()
#Quest'ultimo o aspetta tempo o aspetta un tuo tastino e prende in considerazione quel tempo per prendere frame ed elaborarli cosi' da elaborare tanti frame uno dopo l'altro, con un ritardo cosi' piccolo da gestire un video.

    def show_image(self, title_i, frame):
        cv.imshow(title_i, frame)

    def show_video(self, title_v):
        try:
            while True:
                frame = self.get_image()
                if cv.waitKey(1) & 0xFF == ord('c'):
                    cv.destroyAllWindows()
                    cv.imshow(title_v, frame)
                    cv.waitKey(100000)
                    break
                if cv.waitKey(1) & 0xFF == ord('q'): #trasformo la prima e la seconda parte in caratteri ASCII
                    cv.destroyAllWindows()
                    self.dev.release()
                    break
                #temp = frame.copy()
                #temp = cv.cvtColor(temp, cv.COLOR_HSV2RGB)
                #cv.imshow('title_v', frame)
                self.show_image(title_v, frame)
        except KeyboardInterrupt:
            cv.destroyAllWindows()
            self.dev.release()

if __name__ == '__main__':
    cam = CameraImage(0)
    trackbar = Trackbar()
    trackbar.setTrackbar()
    distance_emp = np.array([30, 40, 50, 60, 70, 80, 90, 100, 110, 130, 150])
    area_emp = np.array([37767, 20907, 13212, 9058, 6647, 4994, 4029, 3208, 2586, 1785, 1313])
    findDistance = scipy.interpolate.interp1d(area_emp, distance_emp, fill_value='extrapolate')
    #cam.show_image('test', cam.get_image(1))
    cam.show_video('test')
