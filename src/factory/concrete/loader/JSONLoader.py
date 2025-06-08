from ...abstract.DataLoader import DataLoader
import pandas as pd


class JSONLoader(DataLoader):
    def __init__(self, filepath: str):
        self.filepath: str = filepath

    def load(self):
        print("Loading CSV file...")
        return pd.read_json(self.filepath)