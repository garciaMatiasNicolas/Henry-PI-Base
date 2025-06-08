import pandas as pd
from ....database.DataBase__singleton import MySQLConnector
from ...abstract.DataValidation import DataValidation


class EmployeeValidation(DataValidation):

    def __init__(self, data: pd.DataFrame):
        self.data: pd.DataFrame = data
        self.expected_columns = [
            "EmployeeID", "FirstName", "MiddleInitial", "LastName",
            "BirthDate", "Gender", "CityID", "HireDate"
        ]

    def _clean_data(self) -> None:
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

    def validate(self, db: MySQLConnector) -> pd.DataFrame:
        print("Validating Employees CSV file...")

        super()._validate_columns(model="Employees", data=self.data, expected_columns=self.expected_columns)
        self.data = super()._validate_duplicate_ids(data=self.data, id_column="EmployeeID")
        self._clean_data()

        self.data.dropna(subset=[
            "EmployeeID", "FirstName", "LastName", "BirthDate",
            "Gender", "CityID", "HireDate"
        ], inplace=True)

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
