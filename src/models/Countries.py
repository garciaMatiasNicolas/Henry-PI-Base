import pandas as pd
from ..database.DataBase__singleton import MySQLConnector 


class Country:
    
    def __init__(self, data: pd.DataFrame, database: MySQLConnector):
        self.data = data
        self.expected_columns = ["CountryID", "CountryName", "CountryCode"]
        self.db: MySQLConnector = database 
    
    def _clean_data(self):
        """
        Internal method to clean and standardize the 'CountryName' column.
        It converts names to string, removes special characters, strips whitespace,
        and converts to lowercase.
        """
        self.data["CountryName"] = (
            self.data["CountryName"]
            .astype(str)
            .str.replace(r"[\r\n\t]", "", regex=True)
            .str.strip()
            .str.lower()
        )

    def _validate_duplicate_ids(self):
        """
        Internal method to check for duplicate CountryIDs within the incoming DataFrame.
        Raises a ValueError if duplicates are found.
        """
        self.data["CountryID"] = pd.to_numeric(self.data["CountryID"], errors="coerce").astype("Int64")
        duplicate_ids = self.data[self.data.duplicated(subset=['CountryID'], keep=False)]

        if not duplicate_ids.empty:
            duplicate_category_ids = duplicate_ids['CountryID'].unique().tolist()
            raise ValueError(f"ERROR: Duplicate CountryIDs found in the input data: {duplicate_category_ids}. Please ensure all CountryIDs are unique.")

    def validate(self):
        """
        Validates and cleans the input DataFrame for country data.
        It checks columns, validates unique IDs, cleans data, removes existing countries,
        and renames columns for database insertion.
        """
        if list(self.data.columns) != self.expected_columns:
            raise ValueError(f"ERROR: Countries DataFrame must have exactly these columns: {self.expected_columns}")
        
        self._validate_duplicate_ids()
        self._clean_data()

        cities_saved = [country[0].lower().strip() for country in self.db.query_select(query='SELECT DISTINCT(country_name) FROM countries;')]
        self.data = self.data[~self.data["CountryName"].isin(cities_saved)].copy()

        self.data.rename(columns={
            "CountryID": "country_id",
            "CountryName": "country_name",
            "CountryCode": "country_code",
        }, inplace=True)

        print("Country validation passed.")

        return self.data

