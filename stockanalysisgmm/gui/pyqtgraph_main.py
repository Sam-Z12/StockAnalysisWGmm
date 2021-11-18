import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .window_frame import TitleBar, SideGrip, CornerGrips
from .sim_page import GSChartPage

TITLE_BAR_HEIGHT = 35


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, live):
        super().__init__()

        self.setStyleSheet("*{background-color: rgb(10, 10, 10)}")
        self.setMouseTracking(True)
        self.press_control = 0
        self._gripSize = 8
        self.grip_value = 0
        self.last_window_size = None
        #self.setMinimumSize(300, 220)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(800, 650)

        """MainBody"""
        self.central_frame = QtWidgets.QStackedWidget(self)
        self.main_page = GSChartPage(live=live)
        self.central_frame.addWidget(self.main_page)

        self.title_bar = TitleBar(self)
        self.title_bar.setGeometry(0, 0, self.width(), TITLE_BAR_HEIGHT)

        self.corner_grips = [
            CornerGrips(self, Qt.BottomRightCorner),
            CornerGrips(self, Qt.BottomLeftCorner),
            CornerGrips(self, Qt.TopRightCorner),
            CornerGrips(self, Qt.TopLeftCorner)
        ]

        self.sideGrips = [
            SideGrip(self, Qt.LeftEdge),
            SideGrip(self, Qt.TopEdge),
            SideGrip(self, Qt.RightEdge),
            SideGrip(self, Qt.BottomEdge)
        ]

    @property
    def gripSize(self):
        return self._gripSize

    def updateGrips(self):
        """Resizes the side and corner grips to the edges of the window"""
        out_rect = self.rect()
        inRect = out_rect.adjusted(
            self.gripSize, self.gripSize, -self.gripSize, -self.gripSize)
        width = self.width()
        height = self.height()
        non_titlebar_window = out_rect.adjusted(0, TITLE_BAR_HEIGHT, 0, 0)

        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())
        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(), inRect.top(), self.gripSize, inRect.height())
        self.sideGrips[3].setGeometry(self.gripSize, inRect.top(
        ) + inRect.height(), inRect.width(), self.gripSize)
        self.corner_grips[0].setGeometry(
            inRect.right(), inRect.bottom(), self.gripSize, self.gripSize)
        self.corner_grips[1].setGeometry(
            out_rect.left(), inRect.bottom(), self.gripSize, self.gripSize)
        self.corner_grips[2].setGeometry(
            inRect.right(), out_rect.top(), self.gripSize, self.gripSize)
        self.corner_grips[3].setGeometry(
            out_rect.left(), out_rect.top(), self.gripSize, self.gripSize)
        self.central_frame.setGeometry(non_titlebar_window)
        self.title_bar.setGeometry(0, 0, width, TITLE_BAR_HEIGHT)

    def resizeEvent(self, event):
        QtWidgets.QWidget.resizeEvent(self, event)
        self.updateGrips()


# if __name__ == "__main__":
def start_window(live=False):
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow(live=live)
    mw.show()
    sys.exit(app.exec())
