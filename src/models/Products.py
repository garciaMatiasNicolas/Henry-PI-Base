from datetime import date
import pandas as pd

class Product:

    def __init__(
        self, 
        id: int,
        name: str, 
        price: float, 
        category: int, 
        class_type: str, 
        modify_date: date,
        is_allergic: bool,
        vitality_days: int
    ):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.class_type = class_type
        self.modify_date = modify_date
        self.is_allergic = is_allergic
        self.vitality_days = vitality_days

    @classmethod
    def from_db_row(cls, row: tuple):
        return cls(
            id=row[0],
            name=row[1],
            price=row[2],
            category=row[3],
            class_type=row[4],
            modify_date=row[5],
            is_allergic=bool(row[6]),
            vitality_days=row[7]
        )

    @classmethod
    def from_pandas_row(cls, row: pd.Series):
        return cls(
            id=int(row["id"]),
            name=row["name"],
            price=float(row["price"]),
            category=int(row["category"]),
            class_type=row["class_type"],
            modify_date=pd.to_datetime(row["modify_date"]).date(),
            is_allergic=bool(row["is_allergic"]),
            vitality_days=int(row["vitality_days"])
        )