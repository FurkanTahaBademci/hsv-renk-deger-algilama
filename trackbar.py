from PyQt5.QtWidgets import*
from arayüz import Ui_MainWindow
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import cv2
import numpy as np

class untitled_python(QMainWindow):
    
    def __init__(self):
    
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.ui.pushButton_2.setEnabled(False)

        self.lower_h = 0
        self.lower_s = 0
        self.lower_v = 0
        self.upper_h = 180
        self.upper_s = 255
        self.upper_v = 255
        self.a = 0
        self.hassasiyet = 500
    
    #------- LOWER ---------#
    def lower_1(self,lower_h): 
        self.lower_h = lower_h

    def lower_2(self,lower_s):
        self.lower_s = lower_s

    def lower_3(self,lower_v): 
        self.lower_v = lower_v
    
    #------- UPPER ---------#
    def upper_1(self,upper_h):
        self.upper_h = upper_h

    def upper_2(self,upper_s): 
        self.upper_s = upper_s
        
    def upper_3(self,upper_v): 
        self.upper_v = upper_v

    def hassasiyet(self,index):
        self.hassasiyet = index
    

    def kamera_ac(self): 

        self.a = 1     
        self.ui.pushButton_2.setEnabled(True)
        self.ui.pushButton.setEnabled(False)
        self.kamera()
        print(self.a)


    def kamera(self):

        capture = cv2.VideoCapture(0)

        while self.a == 1:

            ret, frame = capture.read()
    
            if ret:


                image = cv2.flip(frame,1)
                image_copy = image.copy()


                en_boy = self.ui.FeedLabel.geometry()
                w,h = en_boy.getRect()[2:]

                
                image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        
                image_orjinal = cv2.resize(image,(w+5,h))
                ConvertToFormat = QImage(image_orjinal.data, image_orjinal.shape[1], image_orjinal.shape[0], QImage.Format_RGB888)
                self.ui.FeedLabel.setPixmap(QPixmap.fromImage(ConvertToFormat))
                cv2.waitKey(0)
            
                #-----------------------------------------------------------------
                
                hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
                lower_color = np.array([self.lower_h, self.lower_s, self.lower_v]) 
                upper_color = np.array([self.upper_h, self.upper_s, self.upper_v])

                mask = cv2.inRange(hsv,lower_color,upper_color)
                mask = cv2.dilate(mask,(5,5),iterations=7)
                mask = cv2.erode(mask,(5,5),iterations=7)

                mask_orjinal = cv2.resize(mask,(480,310))
                pic2 = QImage(mask_orjinal.data, mask_orjinal.shape[1], mask_orjinal.shape[0], QImage.Format_Grayscale8)
                self.ui.FeedLabel_2.setPixmap(QPixmap.fromImage(pic2))
             
                #------------------------------------------------------------------
                
                bitwise = cv2.bitwise_and(image,image,mask=mask)
                bitwise_orjinal = cv2.resize(bitwise,(480,310))
                pic3 = QImage(bitwise_orjinal.data, bitwise_orjinal.shape[1], bitwise_orjinal.shape[0], QImage.Format_RGB888)

                self.ui.FeedLabel_3.setPixmap(QPixmap.fromImage(pic3))
                


                #-------------------------------------------------------------------

                conturs,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                image_copy = cv2.cvtColor(image_copy,cv2.COLOR_BGR2RGB)

                for cnt in conturs:
                    area = cv2.contourArea(cnt)
                    if area > self.hassasiyet:

                        (x,y,w,h) = cv2.boundingRect(cnt)   # değerleri çekmemizi sağlıyor
                        cv2.rectangle(image_copy,(x,y),(x+w, y+h),(255,0,0),3)  

                copy_orjinal = cv2.resize(image_copy,(480,310))
                pic4 = QImage(copy_orjinal.data, copy_orjinal.shape[1], copy_orjinal.shape[0], QImage.Format_RGB888)
                self.ui.FeedLabel_4.setPixmap(QPixmap.fromImage(pic4))

                if self.a == 0:
                    
                    self.ui.FeedLabel.clear()
                    self.ui.FeedLabel_2.clear()
                    self.ui.FeedLabel_3.clear()
                    self.ui.FeedLabel_4.clear()


    def kamera_kapat(self):
        
        print("kapatma tuşuna basıldıı")
        self.a = 0
        self.ui.pushButton.setEnabled(True)
        self.ui.pushButton_2.setEnabled(False)


def arayuz_ac():

    uygulama = QApplication([])
    pencere = untitled_python()
    pencere.show()
    uygulama.exec_()

arayuz_ac()
    








