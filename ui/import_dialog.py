from PyQt5.QtWidgets import QDialog, QFileDialog, QVBoxLayout, QPushButton, QLabel
from modules.import_module import DataManager

class ImportDialog(QDialog):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Import File')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('No file selected', self)
        layout.addWidget(self.label)

        importButton = QPushButton('Select File', self)
        importButton.clicked.connect(self.selectFile)
        layout.addWidget(importButton)

        self.setLayout(layout)

    def selectFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Import File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
        if fileName:
            try:
                data = self.data_manager.import_file(fileName)
                self.label.setText(f"File selected: {fileName}")
                self.parent().data = data  # Storing data for further processing
            except Exception as e:
                self.label.setText(f"Error: {e}")
