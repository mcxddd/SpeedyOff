from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox
from modules.data_processing_module import DataProcessingModule

class ProcessingDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.data_processor = DataProcessingModule()
        self.data_processor.load_data(self.data)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Data Processing')
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel('Ready to process data', self)
        layout.addWidget(self.label)

        cleanButton = QPushButton('Clean Data', self)
        cleanButton.clicked.connect(self.cleanData)
        layout.addWidget(cleanButton)

        self.analysisTypeComboBox = QComboBox(self)
        self.analysisTypeComboBox.addItems(['Basic Analysis', 'Correlation', 'Covariance'])
        layout.addWidget(self.analysisTypeComboBox)

        analyzeButton = QPushButton('Analyze Data', self)
        analyzeButton.clicked.connect(self.analyzeData)
        layout.addWidget(analyzeButton)

        self.setLayout(layout)

    def cleanData(self):
        cleaned_data = self.data_processor.clean_data()
        self.label.setText("Data cleaned successfully.")
        self.parent().data_manager.store_data(cleaned_data)  # Store cleaned data for further processing

    def analyzeData(self):
        analysis_type = self.analysisTypeComboBox.currentText()
        if analysis_type == 'Basic Analysis':
            result = self.data_processor.analyze_data()
        else:
            result = self.data_processor.perform_advanced_analysis(analysis_type.lower())
        if result is not None:
            self.label.setText(f"Data analysis result:\n{result}")
        else:
            self.label.setText("Error in data analysis.")
