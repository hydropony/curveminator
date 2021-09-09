# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject


class Communications(QObject):
    updateStatusBar = pyqtSignal(str)
    updateSelectedPoint = pyqtSignal(str, str, str)
    cyclePoint = pyqtSignal(int)
    gotoPoint = pyqtSignal(int)
    reorderPoint = pyqtSignal(int)
    moveXPoint = pyqtSignal(float)
    moveXPointTo = pyqtSignal(float)
    moveYPoint = pyqtSignal(float)
    moveYPointTo = pyqtSignal(float)
    toggleHull = pyqtSignal(bool)
    toggleGuide = pyqtSignal(bool)
    addCurve = pyqtSignal(str)
    removeCurve = pyqtSignal(str)
    selectCurve = pyqtSignal(str)
    selectedCurveName = pyqtSignal(str)
    renameCurve = pyqtSignal(str)
