from datetime import date

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

