import pandas as pd


class City:
    
    def __init__(
        self, 
        city_id: int, 
        city_name: str, 
        zipcode: int, 
        country_id: int
    ):
        self.city_id = city_id
        self.city_name = city_name
        self.zipcode = zipcode
        self.country_id = country_id
    
    @classmethod
    def from_db_row(cls, row: tuple):
        return cls(
            city_id=row[0],
            city_name=row[1],
            zipcode=row[2],
            country_id=row[3]
        )

    @classmethod
    def from_pandas_row(cls, row: pd.Series):
        return cls(
            city_id=int(row["city_id"]),
            city_name=row["city_name"],
            zipcode=int(row["zipcode"]),
            country_id=int(row["country_id"])
        )

