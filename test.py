import sys
from PyQt5 import QtCore, uic, QtWidgets, QtGui
import urllib.request

class Example(QtWidgets.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def initUI(self):
        hbox = QtWidgets.QHBoxLayout(self)

        url = 'http://www.google.com/images/srpr/logo1w.png'
        data = urllib.request.urlopen(url).read()

        image = QtGui.QImage()
        image.loadFromData(data)

        lbl = QtWidgets.QLabel(self)
        lbl.setPixmap(QtGui.QPixmap(image))

        hbox.addWidget(lbl)
        self.setLayout(hbox)

        self.show()

def main():

    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
