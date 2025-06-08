from abc import ABC, abstractmethod
import pandas as pd


class DataValidation(ABC):
    @abstractmethod
    def validate(self):
        pass

    @staticmethod
    def _validate_columns(model: str, data: pd.DataFrame, expected_columns: list) -> None:
        """
        Internal method to check the incoming DataFrame has the corresponding columns.
        """
        if list(data.columns) != expected_columns:
            raise ValueError(f"ERROR: {model} DataFrame must have exactly these columns: {expected_columns}")
    
    @staticmethod
    def _validate_duplicate_ids(data: pd.DataFrame, id_column: str) -> pd.DataFrame:
        """
        Internal method to check for duplicate IDs within the incoming DataFrame.
        Raises a ValueError if duplicates are found.
        """
        data[id_column] = pd.to_numeric(data[id_column], errors="coerce").astype("Int64")
        duplicate_ids = data[data.duplicated(subset=[id_column], keep=False)]

        if not duplicate_ids.empty:
            duplicate_ids = duplicate_ids[id_column].unique().tolist()
            raise ValueError(f"ERROR: Duplicate {id_column}s found in the input data: {duplicate_ids}. Please ensure all {id_column}s are unique.")
        
        return data