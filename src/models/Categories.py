import pandas as pd
from ..database.DataBase__singleton import MySQLConnector 
from pydantic import BaseModel


class Category:
    
    def __init__(self, data: pd.DataFrame, database: MySQLConnector):
        self.data = data
        self.expected_columns = ["CategoryID", "CategoryName"]
        self.db: MySQLConnector = database 
    
    def _clean_data(self):
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

        if not self.data["CategoryName"].map(lambda x: isinstance(x, str)).all():
            raise ValueError("ERROR: All CategoryName values must be strings.")
    
    def _validate_duplicate_ids(self):
        """
        Internal method to check for duplicate CategoryIDs within the incoming DataFrame.
        Raises a ValueError if duplicates are found.
        """
        self.data["CategoryID"] = pd.to_numeric(self.data["CategoryID"], errors="coerce").astype("Int64")
        duplicate_ids = self.data[self.data.duplicated(subset=['CategoryID'], keep=False)]

        if not duplicate_ids.empty:
            duplicate_category_ids = duplicate_ids['CategoryID'].unique().tolist()
            raise ValueError(f"ERROR: Duplicate CategoryIDs found in the input data: {duplicate_category_ids}. Please ensure all CategoryIDs are unique.")

    def validate(self):
        """
        Validates and cleans the input DataFrame for categories.
        It performs the following steps:
        1. Checks if the DataFrame has the expected columns.
        2. Cleans and standardizes the 'CategoryName' column.
        3. Validates for duplicate 'CategoryID' values within the input data.
        4. Filters out categories that already exist in the database.
        5. Renames columns to match the database schema.

        Returns:
            pd.DataFrame: The validated and cleaned DataFrame ready for insertion.
        Raises:
            ValueError: If column names are incorrect, data types are invalid,
            duplicate IDs exist, or other validation/cleaning issues occur.
        """

        if list(self.data.columns) != self.expected_columns:
            raise ValueError(f"ERROR: Categories DataFrame must have exactly these columns: {self.expected_columns}")

        self._clean_data()
        self._validate_duplicate_ids()

        categories_saved = [cat[0].lower().strip() for cat in self.db.query_select(query='SELECT DISTINCT(category_name) FROM categories;')]
        self.data = self.data[~self.data["CategoryName"].isin(categories_saved)].copy()

        self.data.rename(columns={
            "CategoryID": "category_id",
            "CategoryName": "category_name"
        }, inplace=True)

        print("Category validation passed.")

        return self.data


    