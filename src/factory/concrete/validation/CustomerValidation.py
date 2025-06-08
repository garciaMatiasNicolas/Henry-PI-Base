import pandas as pd
from ....database.DataBase__singleton import MySQLConnector
from ...abstract.DataValidation import DataValidation


class CustomerValidation(DataValidation):

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.expected_columns = ["CustomerID", "FirstName", "MiddleInitial", "LastName", "CityID", "Address"]

    def _clean_data(self) -> None:
        self.data["FirstName"] = (
            self.data["FirstName"]
            .astype(str)
            .str.replace(r"[\r\n\t]", "", regex=True)
            .str.strip()
            .str.title()
        )
        
        self.data["LastName"] = (
            self.data["LastName"]
            .astype(str)
            .str.replace(r"[\r\n\t]", "", regex=True)
            .str.strip()
            .str.title()
        )

        self.data["MiddleInitial"] = (
            self.data["MiddleInitial"]
            .astype(str)
            .str.strip()
            .str.upper()
            .replace(["", "NULL", "NONE", "NAN", "NA"], None)
        )

        self.data["MiddleInitial"] = self.data["MiddleInitial"].where(
            self.data["MiddleInitial"].str.len() == 1, None
        )

        self.data["Address"] = (
            self.data["Address"]
            .astype(str)
            .str.replace(r"[\r\n\t]", " ", regex=True)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )

        self.data["CityID"] = pd.to_numeric(self.data["CityID"], errors="coerce").astype("Int64")

    def validate(self, db: MySQLConnector) -> pd.DataFrame:
        print("Validating Customers CSV file...")

        super()._validate_columns("Customers", self.data, self.expected_columns)
        self.data = super()._validate_duplicate_ids(self.data, "CustomerID")
        self._clean_data()

        self.data.dropna(subset=["CustomerID", "FirstName", "LastName", "CityID", "Address"], inplace=True)

        self.data.rename(columns={
            "CustomerID": "customer_id",
            "FirstName": "first_name",
            "MiddleInitial": "middle_initial",
            "LastName": "last_name",
            "CityID": "city_id",
            "Address": "address",
        }, inplace=True)

        print("Customers validation passed.")
        return self.data