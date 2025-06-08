import pandas as pd


class Country:
    
    def __init__(
        self, 
        country_id: int, 
        country_name: str, 
        country_code: str
    ):
        self.country_id = country_id
        self.country_name = country_name
        self.country_code = country_code
    
    @classmethod
    def from_db_row(cls, row: tuple):
        return cls(
            country_id=row[0],
            country_name=row[1],
            country_code=row[2]
        )

    @classmethod
    def from_pandas_row(cls, row: pd.Series):
        return cls(
            country_id=row["country_id"],
            country_name=row["country_name"],
            country_code=row["country_code"]
        )