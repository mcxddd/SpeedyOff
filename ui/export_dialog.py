from PyQt5.QtWidgets import QDialog, QFileDialog, QVBoxLayout, QPushButton, QLabel
from modules.import_module import DataManager

class ExportDialog(QDialog):
    def __init__(self, data_manager, parent=None):
        super().__init__(parent)
        self.data_manager = data_manager
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Export File')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel('No file selected', self)
        layout.addWidget(self.label)

        exportButton = QPushButton('Select Export Location', self)
        exportButton.clicked.connect(self.selectFile)
        layout.addWidget(exportButton)

        self.setLayout(layout)

    def selectFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Export File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
        if fileName:
            try:
                self.export_file(fileName)
                self.label.setText(f"File exported: {fileName}")
            except Exception as e:
                self.label.setText(f"Error: {e}")

    def export_file(self, file_path):
        data = self.data_manager.get_data()
        if data is not None:
            if file_path.endswith('.csv'):
                data.to_csv(file_path, index=False)
            elif file_path.endswith('.xlsx'):
                data.to_excel(file_path, index=False)
            else:
                raise ValueError("Unsupported file format")
        else:
            raise ValueError("No data available to export")
