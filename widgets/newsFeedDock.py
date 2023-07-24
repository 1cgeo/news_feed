import os, sys, copy
from PyQt5 import QtCore, uic, QtWidgets, QtGui
import textwrap
import json
from news_feed.config import Config
from news_feed.api import API
from .newsWithImageWidget import NewsWithImageWidget
from .newsWithoutImageWidget import NewsWithoutImageWidget
from datetime import datetime
from news_feed.timer import Timer

class NewsFeedDock(QtWidgets.QDockWidget):

    dataVersion = 'v4'
    
    def __init__(self, 
            parent=None
        ):
        super(NewsFeedDock, self).__init__(parent=parent)
        uic.loadUi(self.getUIPath(), self)
        self.config = Config()
        self.api = API()
        self.api.setServer(self.config.SERVER)
        self.setupFilters()
        self.fetchData()
        self.setLastRefreshDate()
        self.autoFetch = Timer()
        self.autoFetch.addCallback(self.fetchData)
        self.autoFetch.start(1000*60*30)
        
    def setupFilters(self):
        filters = self.getFilters()
        for setup in [
                {
                    'checkBox': self.toolFilterCkb,
                    'id': 'Ferramentas'
                },
                {
                    'checkBox': self.sapFilterCkb,
                    'id': 'SAP'
                },
                {
                    'checkBox': self.docFilterCkb,
                    'id': 'Metodologia'
                },
                {
                    'checkBox': self.bugFixFilterCkb,
                    'isChecked': filters['BugFix'],
                    'id': 'BugFix'
                },
                {
                    'checkBox': self.alreadyReadFilterCkb,
                    'id': 'Lidas'
                }
            ]: 
            setup['checkBox'].setChecked(filters[setup['id']])
            setup['checkBox'].stateChanged.connect( lambda state, filterId=setup['id']: self.applyFilters(filterId, state == QtCore.Qt.CheckState.Checked) )

    def applyFilters(self, filterId, state):
        filters = self.getFilters()
        filters[filterId] = state
        self.setSettingsVariable('newsFeed:filters:{}'.format(self.dataVersion), json.dumps(filters))
        self.fetchData()

    def getFilters(self):
        filters = self.getSettingsVariable('newsFeed:filters:{}'.format(self.dataVersion))
        if filters:
            return json.loads(filters)
        return {
            'Ferramentas': self.toolFilterCkb.isChecked(),
            'SAP': self.sapFilterCkb.isChecked(),
            'Metodologia': self.docFilterCkb.isChecked(),
            'BugFix': self.bugFixFilterCkb.isChecked(),
            'Lidas': self.alreadyReadFilterCkb.isChecked()
        }

    def setSettingsVariable(self, key, value):
        qsettings = QtCore.QSettings()
        qsettings.setValue(key, value)

    def getSettingsVariable(self, key):
        qsettings = QtCore.QSettings()
        return qsettings.value(key)
        
    def fetchData(self):
        self.cleanNews()
        self.loadNews(self.api.getNews())

    def setLastRefreshDate(self):
        currentDateTime = datetime.now()
        self.lastRefreshLb.setText('Última atualização: {}-{}-{} {}:{}:{}'.format(
            currentDateTime.year,
            currentDateTime.month,
            currentDateTime.day,
            currentDateTime.hour,
            currentDateTime.minute,
            currentDateTime.second
        ))
        
    def getUIPath(self):
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '..',
            'uis',
            'newsFeedDock.ui'
        )

    def loadNews(self, news):
        filters = self.getFilters()
        news = filter(lambda n, filters=filters: self.filterNews(n, filters), news) 
        news = sorted(news, key=lambda k: datetime.strptime(k['data'], '%Y-%m-%d')) 
        for n in news:
            alreadyRead = bool(self.getSettingsVariable('newsFeed:read:{}:{}'.format(self.dataVersion, n['id'])))
            if n['imagem']:
                n['image_url'] = '{}{}'.format(self.api.getServer(), n['imagem']['url'])
                newsWidget = NewsWithImageWidget(
                    n,
                    alreadyRead,
                    self
                )
            else:
                newsWidget = NewsWithoutImageWidget(
                    n,
                    alreadyRead,
                    self
                )
            newsWidget.alreadyRead.connect(self.setAlreadyRead)
            self.newsScrollArea.layout().insertWidget(0, newsWidget)
        self.newsScrollArea.layout().addItem(
            QtWidgets.QSpacerItem(0,10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        )
        self.setLastRefreshDate()

    def filterNews(self, news, filters):
        hasFilter = filters[news['categoria']] if news['categoria'] in filters else False
        hasFilterAlreadyRead = filters['Lidas']
        if not( hasFilter or hasFilterAlreadyRead ):
            return False
        alreadyRead = self.getSettingsVariable('newsFeed:read:{}:{}'.format(self.dataVersion, news['id']))
        if hasFilterAlreadyRead and not alreadyRead:
            return False
        if not hasFilterAlreadyRead and alreadyRead:
            return False
        if hasFilterAlreadyRead and alreadyRead and not hasFilter:
            return False
        if not hasFilter:
            return False
        return True
            
    def setAlreadyRead(self, newsId, state):
        self.setSettingsVariable('newsFeed:read:{}:{}'.format(self.dataVersion, newsId), state)
        self.fetchData()

    def cleanNews(self):
        layout = self.newsScrollArea.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is None:
                continue
            widget.deleteLater()

    @QtCore.pyqtSlot(bool)
    def on_fetchBtn_clicked(self):
        self.fetchData()