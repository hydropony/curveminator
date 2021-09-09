# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication

from main_widget import MainWidget


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    widget = MainWidget()
    sys.exit(app.exec_())
    widget = widget

if __name__ == '__main__':
    main()
