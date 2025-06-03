import pandas as pd
from ..database.DataBase__singleton import MySQLConnector 


class Employee:

    def __init__(self, data: pd.DataFrame, database: MySQLConnector):
        self.data = data
        self.expected_columns = [
            "EmployeeID", "FirstName", "MiddleInitial", "LastName",
            "BirthDate", "Gender", "CityID", "HireDate"
        ]
        self.db: MySQLConnector = database
    
    def _validate_duplicate_ids(self):
        """
        Internal method to check for duplicate EmployeeIDs within the incoming DataFrame.
        Raises a ValueError if duplicates are found.
        """
        self.data["EmployeeID"] = pd.to_numeric(self.data["EmployeeID"], errors="coerce").astype("Int64")
        duplicate_ids = self.data[self.data.duplicated(subset=['EmployeeID'], keep=False)]

        if not duplicate_ids.empty:
            duplicate_category_ids = duplicate_ids['EmployeeID'].unique().tolist()
            raise ValueError(f"ERROR: Duplicate EmployeeIDs found in the input data: {duplicate_category_ids}. Please ensure all EmployeeIDs are unique.")
    
    def _clean_data(self):
        """
        Internal method to clean and standardize various employee-related columns.
        It processes names, middle initial, gender, and converts date/ID columns.
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

        self.data["Gender"] = (
            self.data["Gender"]
            .astype(str)
            .str.strip()
            .str.upper()
        )
        self.data["Gender"] = self.data["Gender"].where(
            self.data["Gender"].isin(["M", "F"]), None
        )

        self.data["BirthDate"] = pd.to_datetime(self.data["BirthDate"], errors='coerce')
        self.data["HireDate"] = pd.to_datetime(self.data["HireDate"], errors='coerce')
        self.data["CityID"] = pd.to_numeric(self.data["CityID"], errors='coerce').astype('Int64')

    def validate(self):
        """
        Validates and cleans the input DataFrame for employee data.
        It checks columns, validates unique IDs, cleans various data fields,
        removes rows with missing essential data, and renames columns for database insertion.
        """
        if list(self.data.columns) != self.expected_columns:
            raise ValueError(f"ERROR: Employees DataFrame must have exactly these columns: {self.expected_columns}")

        self._validate_duplicate_ids()
        self._clean_data()

        self.data.dropna(subset=["EmployeeID", "FirstName", "LastName", "BirthDate", "Gender", "CityID", "HireDate"], inplace=True)

        self.data.rename(columns={
            "EmployeeID": "employee_id",
            "FirstName": "first_name",
            "MiddleInitial": "middle_initial",
            "LastName": "last_name",
            "BirthDate": "birth_date",
            "Gender": "gender",
            "CityID": "city_id",
            "HireDate": "hire_date"
        }, inplace=True)

        print("Employee validation passed.")
        return self.data
