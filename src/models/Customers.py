import pandas as pd


class Customer:
    
    def __init__(self, 
        customer_id: int, 
        first_name: str, 
        middle_initial: str,
        last_name: str, 
        city_id: int, 
        address: str
    ):
        self.customer_id = customer_id
        self.first_name = first_name
        self.middle_initial = middle_initial
        self.last_name = last_name
        self.city_id = city_id
        self.address = address
    
    @classmethod
    def from_db_row(cls, row: tuple):
        return cls(
            customer_id=row[0],
            first_name=row[1],
            middle_initial=row[2],
            last_name=row[3],
            city_id=row[4],
            address=row[5]
        )

    @classmethod
    def from_pandas_row(cls, row: pd.Series):
        return cls(
            customer_id=row["customer_id"],
            first_name=row["first_name"],
            middle_initial=row["middle_initial"],
            last_name=row["last_name"],
            city_id=row["city_id"],
            address=row["address"]
        )