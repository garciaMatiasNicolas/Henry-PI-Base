import pandas as pd
from ....database.DataBase__singleton import MySQLConnector
from ...abstract.DataValidation import DataValidation


class CityValidation(DataValidation):
    
    def __init__(self, data: pd.DataFrame):
        self.data: pd.DataFrame = data
        self.expected_columns = ["CityID", "CityName", "Zipcode", "CountryID"]
    
    def _clean_data(self) -> None:
        """
        Internal method to clean and standardize the 'CityName' column.
        It converts names to string, removes special characters, strips whitespace,
        converts to lowercase, and validates that all resulting values are strings.
        Raises a ValueError if 'CityName' values are not strings after cleaning.
        """
        self.data["CityName"] = (
            self.data["CityName"]
            .astype(str)
            .str.replace(r"[\r\n\t]", "", regex=True)
            .str.strip()
            .str.lower()
        )
        self.data["CountryID"] = pd.to_numeric(self.data["CountryID"], errors="coerce").astype("Int64")

    def validate(self, db: MySQLConnector) -> pd.DataFrame:
        print("Validating City CSV file...")
        
        super()._validate_columns(model="Cities", data=self.data, expected_columns=self.expected_columns)
        self.data = super()._validate_duplicate_ids(data=self.data, id_column="CityID")
        self._clean_data()

        cities_saved = [city[0].lower().strip() for city in db.query_select(query='SELECT DISTINCT(city_name) FROM cities;')]
        self.data = self.data[~self.data["CityName"].isin(cities_saved)].copy()

        self.data.rename(columns={
            "CityID": "city_id",
            "CityName": "city_name",
            "Zipcode": "zipcode",
            "CountryID": "country_id"
        }, inplace=True)

        print("City validation passed.")
        return self.data