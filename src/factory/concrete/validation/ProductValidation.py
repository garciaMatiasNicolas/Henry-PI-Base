import pandas as pd
from ....database.DataBase__singleton import MySQLConnector
from ...abstract.DataValidation import DataValidation


class ProductValidation(DataValidation):

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.expected_columns = [
            "ProductID", "ProductName", "Price", "CategoryID", "Class",
            "ModifyDate", "Resistant", "IsAllergic", "VitalityDays"
        ]
    
    def _clean_data(self) -> None:
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
    
    def validate(self, db: MySQLConnector) -> pd.DataFrame:
        print("Validating Products CSV file...")

        super()._validate_columns("Products", self.data, self.expected_columns)
        self.data = super()._validate_duplicate_ids(self.data, "ProductID")
        self._clean_data()

        existing_ids = [row[0] for row in db.query_select("SELECT id FROM products;")]
        self.data = self.data[~self.data["ProductID"].isin(existing_ids)].copy()

        self.data.dropna(subset=[
            "ProductID", "ProductName", "Price", "CategoryID",
            "ModifyDate", "IsAllergic", "VitalityDays"
        ], inplace=True)

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