import pandas as pd
from ..database.DataBase__singleton import MySQLConnector 


class City:
    
    def __init__(self, data: pd.DataFrame, database: MySQLConnector):
        self.data = data
        self.expected_columns = ["CityID", "CityName", "Zipcode", "CountryID"]
        self.db: MySQLConnector = database 
    
    def _clean_data(self):
        """
        Internal method to clean and standardize city name and convert CountryID to numeric.
        """
        self.data["CityName"] = (
            self.data["CityName"]
            .astype(str)
            .str.replace(r"[\r\n\t]", "", regex=True)
            .str.strip()
            .str.lower()
        )

        self.data["CountryID"] = pd.to_numeric(self.data["CountryID"], errors="coerce").astype("Int64")
    
    def _validate_duplicate_ids(self):
        """
        Internal method to check for duplicate CityIDs within the incoming DataFrame.
        Raises a ValueError if duplicates are found.
        """
        self.data["CityID"] = pd.to_numeric(self.data["CityID"], errors="coerce").astype("Int64")
        duplicate_ids = self.data[self.data.duplicated(subset=['CityID'], keep=False)]

        if not duplicate_ids.empty:
            duplicate_category_ids = duplicate_ids['CityID'].unique().tolist()
            raise ValueError(f"ERROR: Duplicate CityIDs found in the input data: {duplicate_category_ids}. Please ensure all CityIDs are unique.")
        
    def validate(self):
        """
        Validates and cleans the input DataFrame for city data.
        It checks columns, validates unique IDs, cleans data, removes existing cities,
        and renames columns for database insertion.
        """
        if list(self.data.columns) != self.expected_columns:
            raise ValueError(f"ERROR: City DataFrame must have exactly these columns: {self.expected_columns}")
        
        self._validate_duplicate_ids()
        self._clean_data()

        cities_saved = [city[0].lower().strip() for city in self.db.query_select(query='SELECT DISTINCT(city_name) FROM cities;')]
        self.data = self.data[~self.data["CityName"].isin(cities_saved)].copy()

        self.data.rename(columns={
            "CityID": "city_id",
            "CityName": "city_name",
            "Zipcode": "zipcode",
            "CountryID": "country_id"
        }, inplace=True)

        print("City validation passed.")

        return self.data