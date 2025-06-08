from .concrete.loader import CSVLoader, JSONLoader

class DataLoaderFactory:
    def create_loader(source: str, filepath: str):
        if source == "csv":
            return CSVLoader.CSVLoader(filepath=filepath)
        elif source == "json":
            return JSONLoader.JSONLoader(filepath=filepath)
        else:
            raise ValueError("Source not supported")
    