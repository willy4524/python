import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import numpy as np


class MainWindow(QWidget):
    A = np.zeros((500,2))
    index = 0
    pause = 0
    starFlag = False
    finishFlag = False
    def __init__(self):
        super(MainWindow, self).__init__()
        self.tracing_xy = []
        self.lineHistory = []
        self.pen = QPen(Qt.black)
        super().__init__()
        self.initUI()
    
    def initUI(self):
        global index, A, pause, starFlag, finishFlag, ball, removeFlag, outball
        index = 0
        pause = 0
        starFlag = False
        removeFlag = False
        finishFlag = 1
        ball = 0
        outball = 0
        A = np.zeros((500,2))

        self.resize(500, 500)
        self.setWindowTitle('發球機落點測試 ver 1.1.3')
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(palette)
        

        self.lbl1 = QLabel('發球球數 :', self)
        self.lbl2 = QLabel('狀態 :', self)
        self.lbl3 = QLabel('框內 :', self)
        self.lbl4 = QLabel('框外 :', self)
        self.lbl5 = QLabel('指定範圍內 :', self)
        self.lbl6 = QLabel('等待發球', self)
        self.lbl7 = QLabel('00', self)
        self.lbl8 = QLabel('00', self)
        self.lbl9 = QLabel('00', self)
        self.lbl10 = QLabel('框內 % :', self)
        self.lbl11 = QLabel('框外 % :', self)
        self.lbl12 = QLabel('指定範圍內 % :', self)
        self.lbl13 = QLabel('00 %', self)
        self.lbl14 = QLabel('00 %', self)
        self.lbl15 = QLabel('00 %', self)
        self.lbl16 = QLabel('觸網球數 :', self)
        self.lbl17 = QLabel('觸網球數 :', self)
        self.lbl18 = QLabel('觸網球數 % :', self)
        self.lbl19 = QLabel('00', self)
        self.lbl20 = QLabel('00 %', self)

        self.lineedit1 = QLineEdit(self) 
        self.lineedit1.setValidator(QIntValidator())
        self.lineedit2 = QLineEdit(self) 
        self.lineedit2.setValidator(QIntValidator())

        self.mybutton1 = QPushButton('開始', self)
        self.mybutton1.setObjectName('btn_1')
        self.mybutton1.clicked.connect(self.onButtonClick)

        self.mybutton2 = QPushButton('暫停', self)
        self.mybutton2.setObjectName('btn_2')
        self.mybutton2.clicked.connect(self.onButtonClick)

        self.mybutton3 = QPushButton('結算', self)
        self.mybutton3.setObjectName('btn_3')
        self.mybutton3.clicked.connect(self.onButtonClick)

        self.mybutton4 = QPushButton('清除', self)
        self.mybutton4.setObjectName('btn_4')
        self.mybutton4.clicked.connect(self.onButtonClick)
        self.mybutton1.move(10, 0)
        self.mybutton2.move(110, 0)
        self.mybutton3.move(210, 0)
        self.mybutton4.move(310, 0)
        
        self.lbl1.move(10, 53)
        self.lbl2.move(10, 103)
        self.lbl3.move(10, 153)
        self.lbl4.move(10, 203)
        self.lbl5.move(10, 253)
        self.lbl6.move(110, 103)
        self.lbl7.move(110, 153)
        self.lbl8.move(110, 203)
        self.lbl9.move(110, 253)
        self.lbl10.move(210, 153)
        self.lbl11.move(210, 203)
        self.lbl12.move(210, 253)
        self.lbl13.move(310, 153)
        self.lbl14.move(310, 203)
        self.lbl15.move(310, 253)
        self.lbl16.move(250, 53)
        self.lbl17.move(10, 303)
        self.lbl18.move(210, 303)
        self.lbl19.move(110, 303)
        self.lbl20.move(310, 303)

        self.lineedit1.move(70, 50)
        self.lineedit2.move(310, 50)

    def onButtonClick(self):
        global index, pause, starFlag, finishFlag, ball, removeFlag, outball
        sender = self.sender()
        print('objectName = ' + sender.objectName())
        if sender == self.mybutton1:
            if finishFlag == True:
                if self.lineedit1.text() == '':
                    self.information1_msg()
                else:
                    print('button 1 click')
                    self.lbl6.setText('計數中')
                    starFlag = True
                    pause = False
                    finishFlag = False
                    ball = int(self.lineedit1.text())
        elif sender == self.mybutton2:
            print('button 2 click')
            if pause == False and finishFlag == False:
                self.lbl6.setText('暫停')
                pause = True
            elif pause == True and finishFlag == False:
                self.lbl6.setText('計數中')
                pause = False
        elif sender == self.mybutton3:
            if self.lineedit1.text() == '' or self.lineedit2.text() == '':
                self.information2_msg()
            else:
                if starFlag == True:
                    self.lbl6.setText('結算')
                    outball = int(self.lineedit2.text())
                    starFlag = False
                    finishFlag = True
                    pause = False
                    self.lbl19.setText(f'{outball}')
                    self.lbl20.setText(f'{int((outball / ball)*100)}' + '%')
                    self.counter()
                    print('button 3 click')
        elif sender == self.mybutton4 and finishFlag == True:
            finishFlag = True
            removeFlag = True
            pause = False
            self.lbl6.setText('等待發球')
            self.lbl7.setText('00')
            self.lbl8.setText('00')
            self.lbl9.setText('00')
            self.lbl19.setText('00')
            self.lbl13.setText('00 %')
            self.lbl14.setText('00 %')
            self.lbl15.setText('00 %')
            self.lbl20.setText('00 %')
            self.lineedit2.setText('')
            self.update()
            index = 0
        else:
            print('? click')

    def information1_msg(self):
        reply = QMessageBox.information(self, '錯誤','請輸入球數',QMessageBox.Cancel)
    def information2_msg(self):
        reply = QMessageBox.information(self, '錯誤','請輸入觸網球數',QMessageBox.Cancel)

    def paintEvent(self, QPaintEvent):
        global index, A, removeFlag
        self.painter = QPainter()
        self.painter.begin(self)
        self.pen1 = QPen(Qt.black)
        self.painter.setPen(self.pen1)
        
        self.pixmap = QPixmap("images/01.jpg")
        self.painter.drawPixmap(self.rect(), self.pixmap)

        if removeFlag == True:
            removeFlag = False
            self.painter.eraseRect(self.rect())
            self.lineHistory = []
            self.pixmap = QPixmap("images/01.jpg")
            self.painter.drawPixmap(self.rect(), self.pixmap)
        else:
            start_x_temp = 0
            start_y_temp = 0
            if self.lineHistory:
                for line_n in range(len(self.lineHistory)):
                    for point_n in range(1, len(self.lineHistory[line_n])):
                        start_x, start_y = self.lineHistory[line_n][point_n-1][0], self.lineHistory[line_n][point_n-1][1]
                        end_x, end_y = self.lineHistory[line_n][point_n][0], self.lineHistory[line_n][point_n][1]
                        self.painter.drawEllipse(start_x, start_y, 20, 20)

            for x, y in self.tracing_xy:
                if start_x_temp == 0 and start_y_temp == 0:
                    self.painter.drawEllipse(self.start_xy[0][0], self.start_xy[0][1], 20, 20)

                start_x_temp = x
                start_y_temp = y
        self.painter.end()

    def mousePressEvent(self, QMouseEvent):
        global index, A, pause, starFlag
        if starFlag == True and pause == False:
            A[index][0] = QMouseEvent.pos().x()
            A[index][1] = QMouseEvent.pos().y()
            index += 1
            self.counter()
            self.tracing_xy.append((QMouseEvent.pos().x(), QMouseEvent.pos().y()))
        self.start_xy = [(QMouseEvent.pos().x(), QMouseEvent.pos().y())]
        self.update()
        print(QMouseEvent.pos().x(), QMouseEvent.pos().y())
        
    def mouseReleaseEvent(self, QMouseEvent):
        self.lineHistory.append(self.start_xy+self.tracing_xy)
        self.tracing_xy = []

    def counter(self):
        global index, ball, outball
        self.lbl7.setText(f'{index}')
        self.lbl8.setText(f'{ball - index - outball}')
        self.lbl9.setText(f'{index}')
        self.lbl13.setText(f'{int((index / ball)*100)}''%')
        self.lbl14.setText(f'{int((int(ball - index - outball) / ball)*100)}' + '%')
        self.lbl15.setText(f'{int((index / ball)*100)}' + '%')
    
if __name__ == '__main__':
     app = QApplication([])
     window = MainWindow()
     window.show()
     sys.exit(app.exec_())