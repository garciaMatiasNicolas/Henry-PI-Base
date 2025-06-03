import pandas as pd
from ..database.DataBase__singleton import MySQLConnector 


class Product:
    
    def __init__(self, data: pd.DataFrame, database: MySQLConnector):
        self.data = data
        self.db = database
        self.expected_columns = [
            "ProductID", "ProductName", "Price", "CategoryID", "Class",
            "ModifyDate", "Resistant", "IsAllergic", "VitalityDays"
        ]
    
    def _validate_duplicate_ids(self):
        """
        Internal method to check for duplicate ProductIDs within the incoming DataFrame.
        Raises a ValueError if duplicates are found.
        """
        self.data["ProductID"] = pd.to_numeric(self.data["ProductID"], errors="coerce").astype("Int64")
        duplicate_ids = self.data[self.data.duplicated(subset=['ProductID'], keep=False)]

        if not duplicate_ids.empty:
            duplicate_category_ids = duplicate_ids['ProductID'].unique().tolist()
            raise ValueError(f"ERROR: Duplicate ProductIDs found in the input data: {duplicate_category_ids}. Please ensure all ProductIDs are unique.")
    
    def _clean_data(self):
        self.data["ProductName"] = (
            self.data["ProductName"]
            .astype(str)
            .str.replace(r"[\r\n\t]", "", regex=True)
            .str.strip()
            .str.title()
        )

        self.data["Class"] = (
            self.data["Class"]
            .astype(str)
            .str.replace(r"[\r\n\t]", "", regex=True)
            .str.strip()
            .str.title()
        )

        self.data["IsAllergic"] = (
            self.data["IsAllergic"]
            .astype(str)
            .str.upper()  
            .map({
                "TRUE": 1,
                "FALSE": 0,
                "UNKNOWN": None
            })
        )

        self.data["Price"] = pd.to_numeric(self.data["Price"], errors="coerce")
        self.data["CategoryID"] = pd.to_numeric(self.data["CategoryID"], errors="coerce").astype("Int64")
        self.data["VitalityDays"] = pd.to_numeric(self.data["VitalityDays"], errors="coerce").astype("Int64")
        self.data["ModifyDate"] = pd.to_datetime(self.data["ModifyDate"], errors="coerce")

    def validate(self):
        if list(self.data.columns) != self.expected_columns:
            raise ValueError(f"ERROR: Products DataFrame must have exactly these columns: {self.expected_columns}")

        self._validate_duplicate_ids()
        self._clean_data()

        self.data.dropna(subset=["ProductID", "ProductName", "Price", "CategoryID", "ModifyDate", "IsAllergic", "VitalityDays"], inplace=True)

        self.data.rename(columns={
            "ProductID": "id",
            "ProductName": "name",
            "Price": "price",
            "CategoryID": "category",
            "Class": "class_type",
            "ModifyDate": "modify_date",
            "Resistant": "resistant",
            "IsAllergic": "is_allergic",
            "VitalityDays": "vitality_days"
        }, inplace=True)

        print("Product validation passed.")
        return self.data
