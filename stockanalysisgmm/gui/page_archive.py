from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .simulation import GmmSim
from PyQt5.QtChart import QChartView
from .custom_widgets import GuiCandleChart, MyChart


class SimPage(QtWidgets.QFrame):
    def __init__(self, ):
        super().__init__()

        self.setStyleSheet("Background-color: rgb(24, 19, 36)")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.candle_chart = GuiCandleChart(parent=self)
        layout.addWidget(self.candle_chart)
        #layout.setAlignment(self.candle_chart, Qt.AlignmentFlag.AlignCenter)

        self.gmm_sim = GmmSim()
        self.start_sim_button = QtWidgets.QPushButton("Start Simulation")
        self.start_sim_button.clicked.connect(self.gmm_sim.start)
        self.start_sim_button.setFixedSize(100, 50)
        self.start_sim_button.setStyleSheet(
            "*{background-color: rgb(5,5,5);"
            "color: rgb(245,245,245);"
            "border-style: inset;}"
            "*:hover{background-color: rgb(50,50,50);}")

        layout.addWidget(self.start_sim_button)

        self.gmm_sim.sig.connect(self.candle_chart._trigger_refresh)
        layout.setAlignment(self.start_sim_button, Qt.AlignmentFlag.AlignHCenter)


class ChartPage(QtWidgets.QFrame):
    def __init__(self,):
        super().__init__()

        self.setStyleSheet("Background-color: rgb(24, 19, 36)")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.gmm_sim = GmmSim()

        self.gmm_sim.run()

        self.chart = MyChart(p=self)
        
        self.chart.createDefaultAxes()
        self.chart_view = QChartView(self.chart)
        layout.addWidget(self.chart_view)
       
        #layout.setAlignment(self.candle_chart, Qt.AlignmentFlag.AlignCenter)

        
        # self.start_sim_button = QtWidgets.QPushButton("Start Simulation")
        # self.start_sim_button.clicked.connect(self.gmm_sim.start)
        # self.start_sim_button.setFixedSize(100, 50)
        # self.start_sim_button.setStyleSheet(
        #     "*{background-color: rgb(5,5,5);"
        #     "color: rgb(245,245,245);"
        #     "border-style: inset;}"
        #     "*:hover{background-color: rgb(50,50,50);}")

        # layout.addWidget(self.start_sim_button)

        # self.gmm_sim.sig.connect(self.refresh)
        # layout.setAlignment(self.start_sim_button, Qt.AlignmentFlag.AlignHCenter)

    def refresh(self):
        self.chart.refresh()
        #self.chart_view = QChartView(self.chart)
        #self.update()
        print("refresh")