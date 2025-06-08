import pandas as pd
from ....database.DataBase__singleton import MySQLConnector
from ...abstract.DataValidation import DataValidation


class CountryValidation(DataValidation):

    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.expected_columns = ["CountryID", "CountryName", "CountryCode"]

    def _clean_data(self) -> None:
        self.data["CountryName"] = (
            self.data["CountryName"]
            .astype(str)
            .str.replace(r"[\r\n\t]", "", regex=True)
            .str.strip()
            .str.lower()
        )

    def validate(self, db: MySQLConnector) -> pd.DataFrame:
        print("Validating Countries CSV file...")

        super()._validate_columns("Countries", self.data, self.expected_columns)
        self.data = super()._validate_duplicate_ids(self.data, "CountryID")
        self._clean_data()

        existing_names = [
            row[0].lower().strip()
            for row in db.query_select("SELECT DISTINCT(country_name) FROM countries;")
        ]

        self.data = self.data[~self.data["CountryName"].isin(existing_names)].copy()

        self.data.rename(columns={
            "CountryID": "country_id",
            "CountryName": "country_name",
            "CountryCode": "country_code",
        }, inplace=True)

        print("Country validation passed.")
        return self.data