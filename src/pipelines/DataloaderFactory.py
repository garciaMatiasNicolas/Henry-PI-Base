from abc import ABC, abstractmethod
import pandas as pd

class DataLoader(ABC):
    @abstractmethod
    def load(self):
        pass

class CSVLoader(DataLoader):
    def __init__(self, filepath: str):
        self.filepath: str = filepath

    def load(self):
        print("Loading CSV file...")
        return pd.read_csv(self.filepath)


class JSONLoader(DataLoader):
    def __init__(self, filepath: str):
        self.filepath: str = filepath

    def load(self):
        print("Loading CSV file...")
        return pd.read_json(self.filepath)


class DataLoaderFactory:
    def create_loader(source: str, filepath: str):
        if source == "csv":
            return CSVLoader(filepath=filepath)
        elif source == "json":
            return JSONLoader(filepath=filepath)
        else:
            raise ValueError("Source not supported")
    



    
