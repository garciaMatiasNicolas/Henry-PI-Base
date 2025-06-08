import pandas as pd
from ....database.DataBase__singleton import MySQLConnector
from ...abstract.DataValidation import DataValidation
from datetime import time


class SaleValidation(DataValidation):

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.expected_columns = [
            "SalesID", "SalesPersonID", "CustomerID", "ProductID",
            "Quantity", "Discount", "TotalPrice", "SalesDate", "TransactionNumber"
        ]
    
    def _clean_data(self) -> None:
        self.data["TransactionNumber"] = (
            self.data["TransactionNumber"]
            .astype(str)
            .str.replace(r"[\r\n\t]", "", regex=True)
            .str.strip()
            .str.title()
        )

        self.data["SalesPersonID"] = pd.to_numeric(self.data["SalesPersonID"], errors="coerce").astype(int)
        self.data["CustomerID"] = pd.to_numeric(self.data["CustomerID"], errors="coerce").astype(int)
        self.data["ProductID"] = pd.to_numeric(self.data["ProductID"], errors="coerce").astype(int)
        self.data["Quantity"] = pd.to_numeric(self.data["Quantity"], errors="coerce").astype(int)
        self.data["Discount"] = pd.to_numeric(self.data["Discount"], errors="coerce").astype(float)
        self.data["TotalPrice"] = pd.to_numeric(self.data["TotalPrice"], errors="coerce").astype(float)
        #self.data["SalesDate"] = pd.to_datetime(self.data["SalesDate"], format="%I:%M:%S %p", errors="coerce").dt.time

    def validate(self, db: MySQLConnector):
        print("Validating Sales CSV file...")

        super()._validate_columns("Sales", self.data, self.expected_columns)
        self.data = super()._validate_duplicate_ids(self.data, "SalesID")
        self._clean_data()

        self.data.dropna(subset=[
            "SalesID", "SalesPersonID", "CustomerID", "ProductID",
            "Quantity", "Discount", "TotalPrice", "SalesDate", "TransactionNumber"
        ], inplace=True)

        self.data.rename(columns={
            "SalesID": "sales_id",
            "SalesPersonID": "sales_person_id",
            "CustomerID": "customer_id",
            "ProductID": "product_id",
            "Quantity": "quantity",
            "Discount": "discount",
            "TotalPrice": "total_price",
            "SalesDate": "sales_date",
            "TransactionNumber": "transaction_number"
        }, inplace=True)

        print("Sales validation passed.")
        return self.data