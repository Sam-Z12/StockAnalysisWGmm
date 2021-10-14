import random
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QCandlestickSeries, QCandlestickSet, QCategoryAxis

GREEN = QColor(11, 147, 0)
RED = QColor(147, 0, 0)
BLUE = QColor(65, 42, 212, 150)
PURPLE = QColor(172, 0, 156, 150)
YELLOW = QColor(214, 203, 4, 150)
ORANGE = QColor(202, 82, 0, 150)
MIDNIGHT_PURPLE = QColor(40,9,46)

GRAPH_FLOOR = 400
PRICE_TO_PIXELS = 2
CANDLE_STRECH = 10
CANDLE_WIDTH = 10
CANDLE_SPACE = 10
CANDLES = 6
PEN_WIDTH = 0.02
CANDLE_BORDER_SIZE = 10



def random_color(a=150):
    rand_nums = [random.randint(0,255) for i in range(3)]
    return QColor(rand_nums[0], rand_nums[1], rand_nums[2], a)

class GuiCandleChart(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent=parent)
        
        #If you dont set fixed height and try to align the widget the widget doesnt appear.
        #self.setFixedSize(500, 500)
        self.setStyleSheet("*{background-color: rgb(5,5,5);}")
        self.color_dict = {'low_label': BLUE,
                            'low_mid_label': PURPLE,
                            'high_mid_label': YELLOW,
                            'high_label': ORANGE}

    def paintEvent(self, event):
        candle_x = 0
        self.candles = self.parent().gmm_sim.cans
        #print(self.candles)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for c in self.candles:
            open = c['open']
            close = c['close']
            low = c['low']
            high = c['high']
            label = c['label']
            #print(f"Open: {open} Close: {close} Low: {low}")

            if open <= close:
                candle_y = open
                pen = QPen(GREEN)

            else:
                candle_y = close
                pen = QPen(RED)

          
            candle_bottom = GRAPH_FLOOR - ((candle_y * 5))
            candle_height = (((-abs(close-open)) * PRICE_TO_PIXELS)) * CANDLE_STRECH

            color = self.color_dict[label]     
            brush = QBrush(color)
            painter.setBrush(brush)
            rect1 = QRect(candle_x, candle_bottom, CANDLE_WIDTH, candle_height)
            painter.drawRect(rect1)
            painter.setBrush(Qt.BrushStyle.NoBrush)

            pen.setWidth(PEN_WIDTH)
            painter.setPen(pen)
            rect = QRect(candle_x, candle_bottom, CANDLE_WIDTH,  candle_height)
            painter.drawRect(rect)
            
            # p1_tw = QPoint(candle_x + (0.5*CANDLE_WIDTH), candle_bottom + candle_height) 
            # p2_tw = QPoint(candle_x + (0.5*CANDLE_WIDTH), candle_bottom + candle_height -)
            # top_wick = QLine(p1_tw, p2_tw)
            # painter.drawLine(top_wick)

            # p1_bw = QPoint(candle_x + (0.5*CANDLE_WIDTH), GRAPH_FLOOR-(low*PRICE_TO_PIXELS) )
            # p2_bw = QPoint(candle_x + (0.5*CANDLE_WIDTH), (GRAPH_FLOOR - (candle_y * PRICE_TO_PIXELS)))
            # bottom_wick = QLine(p1_bw, p2_bw)
            # painter.drawLine(bottom_wick)

            candle_x += (CANDLE_WIDTH + CANDLE_SPACE)

        painter.end()

    def _trigger_refresh(self):
        self.update()

class MyChart(QChart):
    def __init__(self, p):
        super().__init__()
        self.p = p
        #Set background color
        background_brush = QBrush(MIDNIGHT_PURPLE)
        self.setBackgroundBrush(background_brush)
        
        #Set background series
        # self.candle_stick_series = GmmCandleSeries()
        # self.axisX = QCategoryAxis()
        # self.axisX.setRange(0, 1633928400000)
        # self.axisX.setGridLineVisible(False)
        # self.addAxis(self.axisX, Qt.AlignmentFlag.AlignBottom)

        # self.axisY = QCategoryAxis()
        # self.axisY.setRange(0, 200)
        # self.addAxis(self.axisY, Qt.AlignmentFlag.AlignLeft)
        #print(dir(p))
        self.candles = self.p.gmm_sim.cans
        print(self.candles)
        self.can_sets = [GmmCandlestickSet(open=c['open'],
                                        high=c['high'],
                                        low=c['low'],
                                        close=c['close'],
                                        timestamp=c['timestamp'],
                                        label=c['label'],
                                    ) for c in self.candles] 

        self.can_series = GmmCandleSeries(list_candle_stick_sets=self.can_sets)
        
        #self.series = self.create_series()
        self.addSeries(self.can_series)

        #Set animations
        self.setAnimationOptions(QChart.SeriesAnimations)


    

    def refresh(self):
        # self.removeSeries(self.series)
        # self.series = self.create_series()
        #self.can_series.append(self.create_sets()[-1])
        pass


class GmmCandleSeries(QCandlestickSeries):
    def __init__(self, list_candle_stick_sets):
        super().__init__()
        self.list_candle_stick_sets = list_candle_stick_sets
        # self.gmm_candle_sticks = [GmmCandlestickSet(20.00, 33.22, 15.33,30.24, 1, 'low_label'),
        #                         GmmCandlestickSet(25.55, 36.44, 22.23, 22.78, 100000, 'low_mid_label'),
        #                         GmmCandlestickSet(26.02, 30.44, 21.95, 28.78, 200000, 'high_mid_label'),
        #                         GmmCandlestickSet(21.75, 23.44, 20.10, 22.78, 300000, 'high_label')]
        

        self.color_dict = {'low_label':       BLUE,
                            'low_mid_label':  PURPLE,
                            'high_mid_label': YELLOW,
                            'high_label':     ORANGE}

        self.setDecreasingColor(RED)
        self.setIncreasingColor(GREEN)

        #Set candle border to a different color for each label
        for set in self.list_candle_stick_sets:
            label = set.label
            label_color = self.color_dict[label]
            pen = QPen(label_color, CANDLE_BORDER_SIZE)
            set.setPen(pen)
            
            self.append(set)


class GmmCandlestickSet(QCandlestickSet):
    # Got Deleted at somepoint, idk?
    pass