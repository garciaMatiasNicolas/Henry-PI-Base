import pandas as pd
from ..database.DataBase__singleton import MySQLConnector 


class Customer:
    
    def __init__(self, data: pd.DataFrame, database: MySQLConnector):
        self.data = data
        self.expected_columns = ["CustomerID", "FirstName", "MiddleInitial", "LastName", "CityID", "Address"]
        self.db: MySQLConnector = database 
    
    def _validate_duplicate_ids(self):
        """
        Internal method to check for duplicate CustomerIDs within the incoming DataFrame.
        Raises a ValueError if duplicates are found.
        """
        self.data["CustomerID"] = pd.to_numeric(self.data["CustomerID"], errors="coerce").astype("Int64")
        duplicate_ids = self.data[self.data.duplicated(subset=['CustomerID'], keep=False)]

        if not duplicate_ids.empty:
            duplicate_category_ids = duplicate_ids['CustomerID'].unique().tolist()
            raise ValueError(f"ERROR: Duplicate CustomerIDs found in the input data: {duplicate_category_ids}. Please ensure all CustomerIDs are unique.")

    def _clean_data(self):
        """
        Internal method to clean and standardize various customer-related columns.
        It processes names, middle initial, address, and converts CityID to numeric.
        """
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

    def validate(self):
        """
        Validates and cleans the input DataFrame for customer data.
        It checks columns, validates unique IDs, cleans various data fields,
        removes rows with missing essential data, and renames columns for database insertion.
        """
        if list(self.data.columns) != self.expected_columns:
            raise ValueError(f"ERROR: Customer DataFrame must have exactly these columns: {self.expected_columns}")
        
        self._validate_duplicate_ids()
        self._clean_data()

        self.data.dropna(subset=["CustomerID", "FirstName", "LastName", "CityID", "Address"], inplace=True)

        self.data.rename(columns={
            "CityID": "city_id",
            "CustomerID": "customer_id",
            "FirstName": "first_name",
            "LastName": "last_name",
            "Address": "address",
            "MiddleInitial": "middle_initial"
        }, inplace=True)

        print("Customers validation passed.")

        return self.data

