import pandas as pd


class Category:
    
    def __init__(
        self, 
        category_id: int, 
        category_name: str
    ):
        self.category_id = category_id
        self.category_name = category_name
    
    @classmethod
    def from_db_row(cls, row: tuple):
        return cls(
            category_id=row[0],
            category_name=row[1]
        )

    @classmethod
    def from_pandas_row(cls, row: pd.Series):
        return cls(
            category_id=int(row["category_id"]),
            category_name=row["category_name"]
        )


    