import pandas as pd
from ....database.DataBase__singleton import MySQLConnector
from ...abstract.DataValidation import DataValidation


class CategoryValidation(DataValidation):
    
    def __init__(self, data: pd.DataFrame):
        self.data: pd.DataFrame = data
        self.expected_columns = ["CategoryID", "CategoryName"]
    
    def _clean_data(self) -> None:
        """
        Internal method to clean and standardize the 'CategoryName' column.
        It converts names to string, removes special characters, strips whitespace,
        converts to lowercase, and validates that all resulting values are strings.
        Raises a ValueError if 'CategoryName' values are not strings after cleaning.
        """
        self.data["CategoryName"] = (
            self.data["CategoryName"]
            .astype(str)
            .str.replace(r"[\r\n\t]", "", regex=True)
            .str.strip()
            .str.lower()
        )

    def validate(self, db: MySQLConnector) -> pd.DataFrame:
        print("Validating Categories CSV file...")
        
        super()._validate_columns(model="Categories", data=self.data, expected_columns=self.expected_columns)
        self.data = super()._validate_duplicate_ids(data=self.data, id_column="CategoryID")
        self._clean_data()

        categories_saved = [cat[0].lower().strip() for cat in db.query_select(query='SELECT DISTINCT(category_name) FROM categories;')]
        self.data = self.data[~self.data["CategoryName"].isin(categories_saved)].copy()

        self.data.rename(columns={
            "CategoryID": "category_id",
            "CategoryName": "category_name"
        }, inplace=True)

        print("Category validation passed.")
        return self.data