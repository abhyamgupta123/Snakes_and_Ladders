# import notify2

# notify2.init("testing")
# notificationobj = notify2.Notification(None)
# notificationobj.set_urgency(notify2.URGENCY_NORMAL)
# notificationobj.set_timeout(10000)

# notificationobj.update("title", "body")
# notificationobj.show()
# import time


#!/usr/bin/python

'''
ZetCode Advanced PyQt5 tutorial 

This program animates the size of a
widget with QPropertyAnimation.

Author: Jan Bodnar
Website: zetcode.com 
'''

from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QPushButton
from PyQt5.QtCore import QRect, QPropertyAnimation
import sys
             
             
class Example(QWidget):

    def __init__(self):
        super().__init__()
        
        
        self.initUI()
        
    def initUI(self):
        
        self.button = QPushButton("Start", self)
        self.button.clicked.connect(self.doAnim)
        self.button.move(30, 30)
        
        self.frame = QFrame(self)
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.frame.setGeometry(150, 30, 100, 100)
        
        self.setGeometry(300, 300, 380, 300)
        self.setWindowTitle('Animation')
        self.show()        
        

    def doAnim(self):

        self.anim = QPropertyAnimation(self.frame, b"geometry")
        self.anim.setDuration(1000)
        self.anim.setStartValue(QRect(150, 30, 100, 100))
        self.anim.setEndValue(QRect(150, 30, 200, 200))
        self.anim.start()

if __name__ == "__main__":
    
    app = QApplication([])
    ex = Example()
    ex.show()
    app.exec_()