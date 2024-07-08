from PyQt5.QtWidgets import QFileDialog
import pandas as pd


class ToDoAppLogic:
    def __init__(self, ui):
        self.ui = ui
        self.ui.importButton.clicked.connect(self.import_file)

    def import_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Import File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
        if file_path:
            data = self.load_data(file_path)
            self.analyze_data(data)

    def load_data(self, file_path):
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            return pd.read_excel(file_path)

    def analyze_data(self, data):
        # Perform data analysis using pandas
        print(data.describe())
