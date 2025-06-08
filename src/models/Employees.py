from datetime import date
import pandas as pd


class Employee:

    def __init__(
        self, 
        employee_id: int, 
        first_name: str, 
        middle_initial: str,
        last_name: str, 
        birth_date: date, 
        gender: str, 
        city_id: int,
        hire_date: date
    ):
        self.employee_id = employee_id
        self.first_name = first_name
        self.middle_initial = middle_initial
        self.last_name = last_name
        self.birth_date = birth_date
        self.gender = gender
        self.city_id = city_id
        self.hire_date = hire_date

    @classmethod
    def from_db_row(cls, row: tuple):
        return cls(
            employee_id=row[0],
            first_name=row[1],
            middle_initial=row[2],
            last_name=row[3],
            birth_date=row[4],
            gender=row[5],
            city_id=row[6],
            hire_date=row[7]
        )

    @classmethod
    def from_pandas_row(cls, row: pd.Series):
        return cls(
            employee_id=row["employee_id"],
            first_name=row["first_name"],
            middle_initial=row["middle_initial"],
            last_name=row["last_name"],
            birth_date=row["birth_date"],
            gender=row["gender"],
            city_id=row["city_id"],
            hire_date=row["hire_date"]
        )