
import pandas as pd


class DataModel:
    def __init__(self):
        self.data = pd.DataFrame()

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
