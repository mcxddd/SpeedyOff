from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class ChartDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Generate Chart')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.label = QLabel('Select Chart Type', self)
        layout.addWidget(self.label)

        self.chartTypeComboBox = QComboBox(self)
        self.chartTypeComboBox.addItems(['Line Chart', 'Bar Chart', 'Pie Chart'])
        layout.addWidget(self.chartTypeComboBox)

        generateButton = QPushButton('Generate Chart', self)
        generateButton.clicked.connect(self.generateChart)
        layout.addWidget(generateButton)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def generateChart(self):
        chart_type = self.chartTypeComboBox.currentText()
        self.figure.clear()

        if chart_type == 'Line Chart':
            self.data.plot(ax=self.figure.add_subplot(111), kind='line')
        elif chart_type == 'Bar Chart':
            self.data.plot(ax=self.figure.add_subplot(111), kind='bar')
        elif chart_type == 'Pie Chart':
            self.data.iloc[0].plot.pie(ax=self.figure.add_subplot(111))

        self.canvas.draw()
