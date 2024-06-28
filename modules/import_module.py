import pandas as pd

class DataManager:
    def __init__(self):
        self.data = None

    def import_file(self, file_path):
        if file_path.endswith('.csv'):
            self.data = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            self.data = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format")
        return self.data

    def get_data(self):
        return self.data

    def store_data(self, data):
        self.data = data
