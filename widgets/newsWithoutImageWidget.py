import os, sys, copy
from PyQt5 import QtCore, uic, QtWidgets, QtGui
import textwrap
import json
import urllib.request

class NewsWithoutImageWidget(QtWidgets.QWidget):

    alreadyRead = QtCore.pyqtSignal(int, bool)
    
    def __init__(self, 
            newsData,
            alreadyRead,
            parent=None
        ):
        super(NewsWithoutImageWidget, self).__init__(parent=parent)
        uic.loadUi(self.getUIPath(), self)
        self.currentId = None
        self.linkLb.setOpenExternalLinks(True)
        self.alreadyReadCkb.setChecked(alreadyRead)
        self.loadData(newsData)
        
    def getUIPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '..',
            'uis',
            'newsWithoutImageWidget.ui'
        )

    def loadData(self, data):
        self.currentId = data['id']
        self.titleLb.setText("<b>{} - {}</b>".format(data['categoria'], data['titulo']))
        self.dateLb.setText('<span style="color: #A8A196;">{}</span>'.format(data['data']))
        self.textLb.setText(data['descricao'])
        self.linkLb.setText("<a href=\"{0}\">{1}</a>".format(data['link'], 'link')) if data['link'] else ''
        self.alreadyReadCkb.stateChanged.connect(lambda state, newsId=data['id']: self.alreadyRead.emit(newsId, state == QtCore.Qt.CheckState.Checked))