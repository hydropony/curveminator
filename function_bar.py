# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QPushButton,
                             QFrame, QLabel, QLineEdit,
                             QHBoxLayout, QVBoxLayout, QSplitter,
                             QCheckBox, QComboBox)
from PyQt5.QtGui import (QFont, QColor)

from drawing_board import DrawingBoard
from param_frame import ParamFrame
from PyQt5.QtCore import QObject


class FunctionBar(QFrame):
    def __init__(self, parent, curves, board):
        super().__init__(parent)
        self.initUI()
        self.c = None
        self.curves = curves
        self.selpoint = 0
        self.activeCurve = None
        # self.activeIndex = 0
        self.prevpointsnum = None
        self.b = board

    def connectEvents(self, c):
        self.c = c

    def updateSelectedPoint(self, id, x, y):
        self.pointIdField.setText(id)
        self.xFrame.textField.setText(str((float(x) - 0.5) * 144.0))
        self.yFrame.textField.setText(str(-(float(y) - 0.5) * 144.0))
        self.update()

    def initUI(self):
        phButton = QPushButton('Placeholder', self)
        phButton.setFont(QFont('Lato', 12))
        phButton.resize(phButton.sizeHint())
        self.cname = QLineEdit(self)
        self.cname.textChanged.connect(self.renameCurve)
        self.cbox = QComboBox(self)
        self.hullBox = QCheckBox('Show hull', self)
        self.guideBox = QCheckBox('Show guide', self)
        lineLayout = QVBoxLayout()
        lineLayout.addWidget(phButton)
        lineLayout.addWidget(self.cbox)
        lineLayout.addWidget(self.cname)
        lineLayout.addWidget(self.hullBox)
        lineLayout.addWidget(self.guideBox)
        self.cbox.activated[str].connect(self.selectCurve)
        self.hullBox.stateChanged.connect(self.toggleHull)
        self.guideBox.stateChanged.connect(self.toggleGuide)
        lineZone = QFrame()
        lineZone.setLayout(lineLayout)

        centeredLabel = QFrame()
        centeredLayout = QHBoxLayout()
        centeredLayout.addStretch(1)
        cycleLabel = QLabel("Cycle points")
        cycleLabel.setFont(QFont('Lato', 12))
        centeredLayout.addWidget(cycleLabel)
        centeredLayout.addStretch(1)
        centeredLabel.setLayout(centeredLayout)

        self.prevPoint = QPushButton("<")
        self.prevPoint.setFixedWidth(23)
        self.prevPoint.resize(self.prevPoint.sizeHint())
        self.pointIdField = QLineEdit("1000", self)
        self.pointIdField.setStyleSheet("QWidget { background-color: %s }" %
                                        QColor(255, 255, 255).name())
        self.nextPoint = QPushButton(">")
        self.nextPoint.setFixedWidth(23)

        self.deleteButton = QPushButton('Delete point')
        self.deleteButton.setFont(QFont('Lato', 12))

        pointCyclerLayout = QHBoxLayout()
        pointCyclerLayout.addWidget(self.deleteButton)
        pointCyclerLayout.addWidget(self.prevPoint)
        pointCyclerLayout.addWidget(self.pointIdField)
        pointCyclerLayout.addWidget(self.nextPoint)

        pointCyclerFrame = QFrame()
        pointCyclerFrame.setLayout(pointCyclerLayout)
        self.pointIdField.textEdited.connect(self.gotoPoint)
        self.prevPoint.clicked.connect(self.cyclePrev)
        self.nextPoint.clicked.connect(self.cycleNext)
        self.deleteButton.clicked.connect(self.deletePoint)

        weightLayout = QVBoxLayout()
        self.weightCheck = QCheckBox("Weights?")
        self.weightField = QLineEdit("1.0")
        weightLayout.addWidget(self.weightCheck)
        weightLayout.addWidget(self.weightField)
        weightFrame = QFrame()
        weightFrame.setLayout(weightLayout)

        self.xFrame = ParamFrame(self, "X:")
        self.xFrame.textField.returnPressed.connect(self.changeX)
        self.xFrame.plus1.clicked.connect(self.increaseX)
        self.xFrame.minus1.clicked.connect(self.reduceX)
        self.yFrame = ParamFrame(self, "Y:")
        self.yFrame.textField.returnPressed.connect(self.changeY)
        self.yFrame.plus1.clicked.connect(self.increaseY)
        self.yFrame.minus1.clicked.connect(self.reduceY)

        pointLayout = QVBoxLayout()
        pointLayout.addStretch(1)
        pointLayout.addWidget(centeredLabel)
        pointLayout.addWidget(pointCyclerFrame)
        pointLayout.addWidget(self.xFrame)
        pointLayout.addWidget(self.yFrame)
        pointLayout.addWidget(weightFrame)
        pointZone = QFrame()
        pointZone.setLayout(pointLayout)

        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(lineZone)
        splitter.addWidget(pointZone)
        vbox = QVBoxLayout()
        vbox.addWidget(splitter)
        self.setLayout(vbox)
        self.show()

    def reduceX(self):
        self.c.moveXPoint.emit(-1 / 144.0)
        self.update()

    def increaseX(self):
        self.c.moveXPoint.emit(1 / 144.0)
        self.update()

    def changeX(self):
        text = self.xFrame.textField.text()
        self.c.moveXPointTo.emit(0.0 if text == '' else float(text) / 144.0 + 0.5)
        self.update()

    def reduceY(self):
        self.c.moveYPoint.emit(-1 / 144.0)
        self.update()

    def increaseY(self):
        self.c.moveYPoint.emit(1 / 144.0)
        self.update()

    def changeY(self):
        text = self.yFrame.textField.text()
        self.c.moveYPointTo.emit(0 if text == '' else -int(text) / 144.0 + 0.5)
        self.update()

    def gotoPoint(self, text):
        self.c.gotoPoint.emit(0 if text == '' else int(text))
        self.update()

    def renameCurve(self, text):
        self.removeCurve(self.cbox.currentIndex())
        self.addCurve(text)
        self.c.renameCurve.emit(text)
        self.update()

    def cyclePrev(self):
        self.c.cyclePoint.emit(-1)
        self.selpoint = self.b.cyclePoint(0)
        print('selpoint: ', self.selpoint)
        self.update()

    def cycleNext(self):
        self.c.cyclePoint.emit(1)
        self.selpoint = self.b.cyclePoint(0)
        print('selpoint: ', self.selpoint)
        self.update()

    def toggleHull(self, state):
        is_hull = True if state == Qt.Checked else False
        self.c.toggleHull.emit(is_hull)
        self.update()

    def toggleGuide(self, state):
        is_guide = True if state == Qt.Checked else False
        self.c.toggleGuide.emit(is_guide)
        self.update()

    def selectCurve(self, cname):
        self.c.selectCurve.emit(cname)
        self.update()
        self.activeCurve = cname
        print(self.activeCurve, "sel")
        print('selected')

    def addCurve(self, cname):
        self.cbox.addItem(cname)
        self.activeCurve = cname
        print(self.activeCurve, "sel")
        self.update()

    def removeCurve(self, cname):
        self.cbox.removeItem(cname)
        self.update()

    def selectedCurveName(self, cname):
        self.cbox.setCurrentText(cname)
        self.update()

    def deletePoint(self):
        self.selpoint = self.b.cyclePoint(0)
        if (self.selpoint != 0):
            print('selpoint: ', self.selpoint)
            print('activeCurve: ', self.activeCurve)
            print(self.curves[int(self.activeCurve)])
            self.curves[int(self.activeCurve)].del_point(int(self.selpoint))
            self.cyclePrev()
