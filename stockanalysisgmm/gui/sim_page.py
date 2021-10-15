
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor

import pyqtgraph as pg
from pyqtgraph.functions import mkPen

from .simulation import GmmSim, ExampleSim, STOCK_TICKER
from .custom_widgets import  CandlestickItem, TimeAxisItem


BLUE = QColor(65, 42, 212, 150)
PURPLE = QColor(172, 0, 156, 150)
YELLOW = QColor(214, 203, 4, 150)
ORANGE = QColor(202, 82, 0, 150)
BACK_COLOR = QColor(2, 1, 25, 150)
PEN_WIDTH_VIEW_AREA_RATIO = 0.01/113483568
MAX_X_RANGE = 8611948
    

class GSChartPage(QtWidgets.QFrame):
    def __init__(self, live):
        super().__init__()

        # Set style of the page
        self.setStyleSheet("Background-color: rgb(2,1,25)")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

        #Add the chart to the page
        self.pw = pg.PlotWidget(name="A Plot", )
        self.pw.setTitle(STOCK_TICKER)
        self.date_axis = TimeAxisItem(orientation="bottom")
        self.pw.setAxisItems({'bottom': self.date_axis})
        self.pw.setBackground(BACK_COLOR)
        self.p1 = self.pw.plot()
        self.pw.setLabel('left', 'Price', units="$")
        self.pw.setLabel('bottom', 'Time', units="t")
        self.pw.showGrid(x=False, y=True)
        self.pw.addLegend()

        #Create plot legend
        s1 = pg.PlotDataItem(pen=mkPen(color=ORANGE, width=5))
        s2 = pg.PlotDataItem(pen=mkPen(color=YELLOW, width=5) )
        s3 = pg.PlotDataItem(pen=mkPen(color=PURPLE, width=5) )
        s4 = pg.PlotDataItem(pen=mkPen(color=BLUE, width=5) )
        self.pw.plotItem.legend.addItem(s1,"High Overbought")
        self.pw.plotItem.legend.addItem(s2,"Mid Overbought")
        self.pw.plotItem.legend.addItem(s3,"Mid Oversold")
        self.pw.plotItem.legend.addItem(s4,"Low Oversold")
        
        #Add plot to layout
        layout.addWidget(self.pw)
        
        
        #Init the smulation
        self.gmm_sim = ExampleSim(live=live)

        #Create button to start simulation
        self.start_sim_button = QtWidgets.QPushButton("Start Simulation")
        self.start_sim_button.setFixedSize(100, 50)
        self.start_sim_button.setStyleSheet(
            "*{background-color: rgb(2,1,25);"
            "color: rgb(245,245,245);"
            "border-style: inset;}"
            "*:hover{background-color: rgb(50,50,50);}")
        self.start_sim_button.clicked.connect(self.gmm_sim.start)
        layout.addWidget(self.start_sim_button)
        layout.setAlignment(self.start_sim_button, Qt.AlignmentFlag.AlignHCenter)

        #connect to signal emitted from the simulation everytime a new data point is made to the chart update func
        self.gmm_sim.sig.connect(self.update_data)
        self.pw.sigRangeChanged.connect(self.update_pen_width)

    def update_data(self):
        #Get candles from the simulation object and create a new graphics scene. Then add to plotWidget
        self.sim_gen_candles = self.gmm_sim.cans
        self.item = CandlestickItem(self.sim_gen_candles, 0.005)
        self.pw.clear()
        self.pw.addItem(self.item)

        #For auto scroll
        # w = self.item.viewRect().width()
        # t = self.gmm_sim.cans[-1][5]
        # print(f"w: {w} t: {t}")
        # if w >= MAX_X_RANGE:  
        #     xmin = t - MAX_X_RANGE
        #     self.pw.setRange(xRange=(xmin, t+50000), padding=0)
    
    def update_pen_width(self):
        rect = self.item.viewRect()
        view_area = (rect.width() * rect.height())
        pen_width = view_area * PEN_WIDTH_VIEW_AREA_RATIO
        if pen_width > 0.015:
            pen_width = 0.015
        elif pen_width < 0.0015:
            pen_width = 0.0015
        #print(f"Update Pen: area: {view_area} Pen: {pen_width}")
        self.sim_gen_candles = self.gmm_sim.cans
        self.item = CandlestickItem(self.sim_gen_candles, pen_width)
        self.pw.clear()
        self.pw.addItem(self.item)


   
   
        

