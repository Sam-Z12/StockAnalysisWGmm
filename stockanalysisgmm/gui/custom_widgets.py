from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen

import pyqtgraph as pg
from pyqtgraph import QtCore, QtGui

from datetime import datetime


GREEN = QColor(11, 147, 0)
RED = QColor(147, 0, 0)
MIDNIGHT_PURPLE = QColor(40,9,46)
# alpha has a max val of 255
BLUE = QColor(65, 42, 212, 150)
PURPLE = QColor(172, 0, 156, 150)
YELLOW = QColor(214, 203, 4, 150)
ORANGE = QColor(202, 82, 0, 150)

PEN_WIDTH_VIEW_AREA_RATIO = 113483568/0.02

class TimeAxisItem(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value).strftime("%Y-%m-%d") for value in values]

class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data, pen_width):
        pg.GraphicsObject.__init__(self)
        pg.setConfigOptions(antialias=True)
        
        self.data = data  ## data must have fields: open, high, low, close, label, timestamp
        self.pen_width = pen_width
        
        self.generatePicture()
          
    def generatePicture(self, ):
        ## pre-computing a QPicture object allows paint() to run much more quickly, 
        ## rather than re-drawing the shapes every time
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        #print(self.data)
        if len(self.data) >= 2:
            w = (self.data[1][5] - self.data[0][5])/3
        else:
            w = self.data[0][5]/47280

        for (open, high, low, close, label, t) in self.data:
            if open > close:
                top = open
                bottom = close
                c = RED
            else:
                top = close
                bottom = open
                c=GREEN

            #Create pens for wicks and body border 
            big_pen = QPen(c, self.pen_width)
            pen = QPen(c, self.pen_width)
            p.setPen(pen)
            #print(f"Top: {top} Bottom: {bottom} High: {high} Low: {low} w: {t/w}")

            #Draw the top and bottom wicks
            p.drawLine(QtCore.QPointF(t, high), QtCore.QPointF(t, top))
            p.drawLine(QtCore.QPointF(t, low), QtCore.QPointF(t, bottom))

            #Shade in the body of the candle 
            p.setPen(Qt.PenStyle.NoPen)
            self.color_dict = {'low_label':       BLUE,
                            'low_mid_label':  PURPLE,
                            'high_mid_label': YELLOW,
                            'high_label':     ORANGE}
            color = self.color_dict[label]
            brush = QBrush(color)
            p.fillRect(QtCore.QRectF(t-w+self.pen_width, bottom, w*2-(self.pen_width*2), top-bottom), brush)

            #draw the rectangle around the body of the candle 
            p.setPen(pen)
            p.drawRect(QtCore.QRectF(t-w, bottom, w*2, top-bottom)) 
        p.end()
    
    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)
    
    def boundingRect(self):
        ## boundingRect _must_ indicate the entire area that will be drawn on
        ## or else we will get artifacts and possibly crashing.
        ## (in this case, QPicture does all the work of computing the bouning rect for us)
        return QtCore.QRectF(self.picture.boundingRect())