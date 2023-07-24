import os, sys, copy
from PyQt5 import QtCore, uic, QtWidgets, QtGui
import textwrap
import json
import urllib.request

class NewsWithImageWidget(QtWidgets.QWidget):

    alreadyRead = QtCore.pyqtSignal(int, bool)
    
    def __init__(self, 
            newsData,
            alreadyRead,
            parent=None
        ):
        super(NewsWithImageWidget, self).__init__(parent=parent)
        uic.loadUi(self.getUIPath(), self)
        self.currentId = None
        self.linkLb.setOpenExternalLinks(True)
        self.imgLb.setScaledContents(True)
        self.imgLb.setFixedSize(QtCore.QSize(200, 200))
        self.alreadyReadCkb.setChecked(alreadyRead)
        self.loadData(newsData)
        
    def getUIPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '..',
            'uis',
            'newsWithImageWidget.ui'
        )

    def loadData(self, data):
        self.currentId = data['id']
        self.titleLb.setText("<b>{} - {}</b>".format(data['categoria'], data['titulo']))
        self.dateLb.setText('<span style="color: #A8A196;">{}</span>'.format(data['data']))
        self.textLb.setText(data['descricao'])
        self.linkLb.setText("<a href=\"{0}\">{1}</a>".format(data['link'], 'link')) if data['link'] else ''
        self.loadImage(data['image_url'])
        self.alreadyReadCkb.stateChanged.connect(lambda state, newsId=data['id']: self.alreadyRead.emit(newsId, state == QtCore.Qt.CheckState.Checked))

    def loadImage(self, url):
        data = urllib.request.urlopen(url).read()
        image = QtGui.QImage()
        image.loadFromData(data)
        pixmap = QtGui.QPixmap(image)

        w = min(pixmap.width(),  self.imgLb.maximumWidth())
        h = min(pixmap.height(), self.imgLb.maximumHeight())

        pixmap.scaled(QtCore.QSize(w, h), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.imgLb.setPixmap(pixmap)                