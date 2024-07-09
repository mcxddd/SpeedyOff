import pandas as pd
from models.data_model import DataModel


class DataController:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_file(self, file_path):
        self.model(file_path)

    def load_data(self, file_path: str):
        try:
            if file_path.endswith('.csv'):
                self.data = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                self.data = pd.read_excel(file_path)
        except Exception as e:
            raise ValueError(f"Error loading CSV: {e}")

    def save_file(self, file_path):
        data = self.get_data()
        if not data.empty:
            data.to_csv(file_path, index=False)

    def analyze_data(self, data):
        # Perform data analysis using pandas
        print(data.describe())
