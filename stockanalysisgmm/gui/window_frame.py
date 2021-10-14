from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon

WINDOW_SIZE = 0

class TitleBar(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.setStyleSheet("*{background-color: rgb(10, 10, 10);"
                                     "padding: 0px;"
                                     "margin: 0px;}")
        self.title_bar_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.title_bar_layout)
        self.title_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.title_bar_layout.setSpacing(1)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)




        # Minimize Window Button
        self.min_btn = QtWidgets.QPushButton()
        self.min_btn.clicked.connect(self.parent.showMinimized)
        self.min_btn.setStyleSheet(
            "*{background-color: rgb(10,10,10);"
            "color: rgb(245,245,245);"
            "border-style: inset;}"
            "*:hover{background-color: rgb(50,50,50);}"

        )
        self.min_btn.setIcon(QIcon(r"C:\Users\Zands\PycharmProjects\AlgoTradingBot\Gui\Gui_Images\MinButton.png"))
        self.min_btn.setIconSize(QSize(35,35))
        self.title_bar_layout.addWidget(self.min_btn)
        self.min_btn.setFixedSize(35, 35)
        self.title_bar_layout.setAlignment(self.min_btn, Qt.AlignRight)
        # self.min_btn.setFlat(True)

        # Maximize Window Button
        self.max_btn = QtWidgets.QPushButton()
        self.max_btn.clicked.connect(self.max_btn_func)
        self.max_btn.setStyleSheet(
            "*{background-color: rgb(10,10,10);"
            "color: rgb(245,245,245);"
            "border-style: inset}"
            "*:hover{background-color: rgb(50,50,50);}"
        )
        self.max_btn.setIcon(QIcon(r"C:\Users\Zands\PycharmProjects\AlgoTradingBot\Gui\Gui_Images\MaxButton2.png"))
        self.max_btn.setIconSize(QSize(35,35))
        self.max_btn.setFixedSize(35, 35)
        self.title_bar_layout.addWidget(self.max_btn)
        # self.max_btn.setFlat(True)

        # Close Window Button
        
        self.close_btn = QtWidgets.QPushButton()
        
        
        self.close_btn.clicked.connect(self.parent.close)
        self.close_btn.setStyleSheet(
            "*{background-color: rgb(10,10,10);"
            "color: rgb(245,245,245);"
            "border-style: inset}"
            "*:hover{background-color: rgb(220,0,0);}")
        self.close_btn.setIcon(QIcon(r"C:\Users\Zands\PycharmProjects\AlgoTradingBot\Gui\Gui_Images\CloseButton4.png"))
        self.close_btn.setIconSize(QSize(35,35))

        

        self.title_bar_layout.addWidget(self.close_btn)
        self.close_btn.setFixedSize(35, 35)


    def max_btn_func(self):
        global WINDOW_SIZE
        window_status = WINDOW_SIZE
        self.parent.last_window_size = self.parent.geometry()

        if WINDOW_SIZE == 0:
            self.max_btn.setIcon(QIcon(r"C:\Users\Zands\PycharmProjects\AlgoTradingBot\Gui\Gui_Images\RestoreButton2.png"))
            self.max_btn.setIconSize(QSize(35,35))
            WINDOW_SIZE = 1
            self.parent.showMaximized()

        else:
            self.max_btn.setIcon(QIcon(r"C:\Users\Zands\PycharmProjects\AlgoTradingBot\Gui\Gui_Images\MaxButton2.png"))
            self.max_btn.setIconSize(QSize(35,35))
            WINDOW_SIZE = 0
            self.parent.showNormal()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.parent.press_control == 0:
                self.pos = e.pos()
                self.main_pos = self.parent.pos()
        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if self.parent.cursor().shape() == Qt.ArrowCursor:
            self.last_pos = e.pos() - self.pos
            self.main_pos += self.last_pos
            self.parent.move(self.main_pos)
        super(TitleBar, self).mouseMoveEvent(e)

class CornerGrips(QtWidgets.QWidget):
    def __init__(self, parent, corner):
        QtWidgets.QWidget.__init__(self, parent)
        if corner == Qt.BottomRightCorner:
            self.setCursor(Qt.SizeFDiagCursor)
            self.resizeFunc = self.resizeBR

        elif corner == Qt.BottomLeftCorner:
            self.setCursor(Qt.SizeBDiagCursor)
            self.resizeFunc = self.resizeBL

        elif corner == Qt.TopRightCorner:
            self.setCursor(Qt.SizeBDiagCursor)
            self.resizeFunc = self.resizeTR

        elif corner == Qt.TopLeftCorner:
            self.setCursor(Qt.SizeFDiagCursor)
            self.resizeFunc = self.resizeTL

        self.mousePos = 0

    def resizeBR(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(width, height)

    def resizeBL(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        height = max(window.minimumHeight(), window.height() + delta.y())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)
        window.resize(window.width(), height)

    def resizeTR(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)
        window.resize(width, window.height())

    def resizeTL(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None


class SideGrip(QtWidgets.QWidget):
    def __init__(self, parent, edge):
        QtWidgets.QWidget.__init__(self, parent)
        if edge == Qt.LeftEdge:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeLeft

        elif edge ==Qt.TopEdge:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeTop


        elif edge == Qt.RightEdge:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeRight

        elif edge == Qt.BottomEdge:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeBottom


        self.mousePos = 0

    def resizeLeft(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right()-width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None
