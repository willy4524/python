from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import threading
import sys
import MetaTrader5 as mt5

import time

mt5.initialize()

ticket_info = mt5.symbol_info_tick("EURUSD")._asdict()
bid_usd = mt5.symbol_info_tick("EURUSD").bid

def applecation():
    app = QApplication(sys.argv)
    window = QMainWindow()

    window.setWindowTitle('Test Programm')
    window.setGeometry(300, 250, 350, 200)


    main_text = QtWidgets.QLabel(window)
    main_text.move(100,100)
    main_text.adjustSize()

    def update_text():
        while True:
            main_text.setText(str(bid_usd))
            time.sleep(0.2)

    t1 = threading.Thread(target = update_text())
    t1.start()


    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    applecation()