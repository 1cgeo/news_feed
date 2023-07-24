from qgis import utils
from qgis.utils import iface
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from .widgets.newsFeedDock import NewsFeedDock


class Main(object):
    def __init__(self, iface):
        self.plugin_dir = os.path.dirname(__file__)
        self.newsFeedAction = None
        self.newsFeedDock = None

    def initGui(self):
        self.newsFeedAction = self.createAction(
            'News Feed',
            os.path.join(
                os.path.abspath(os.path.join(
                    os.path.dirname(__file__)
                )),
                'icons',
                'phone.png'
            ),
            self.showNewsFeed
        )
        self.addActionDigitizeToolBar(self.newsFeedAction)

    def createAction(self, name, iconPath, callback):
        a = QtWidgets.QAction(
            QtGui.QIcon(iconPath),
            name,
            iface.mainWindow()
        )
        a.triggered.connect(callback)
        return a

    def showNewsFeed(self):
        self.removeDockWidget(self.newsFeedDock) if self.newsFeedDock else ''
        self.newsFeedDock = NewsFeedDock()
        self.addDockWidget(self.newsFeedDock, 'left')

    def addDockWidget(self, dockWidget, side):
        position = QtCore.Qt.RightDockWidgetArea if side == 'right' else QtCore.Qt.LeftDockWidgetArea
        dockers = iface.mainWindow().findChildren(QtWidgets.QDockWidget)
        tabify = [ d.objectName() for d in dockers ]
        iface.addTabifiedDockWidget(position, dockWidget, tabify, True)

    def removeDockWidget(self, dockWidget):
        iface.removeDockWidget(dockWidget)
        
    def addActionDigitizeToolBar(self, action):
        iface.digitizeToolBar().addAction(action)

    def removeActionDigitizeToolBar(self, action):
        iface.digitizeToolBar().removeAction(action)

    def unload(self):
        self.removeActionDigitizeToolBar(self.newsFeedAction)
        self.removeDockWidget(self.newsFeedDock) if self.newsFeedDock else ''