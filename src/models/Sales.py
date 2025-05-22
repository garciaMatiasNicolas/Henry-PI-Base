from datetime import datetime

class Sale:

    def __init__(
        self, 
        sales_id: int, 
        sales_person_id: int, 
        customer_id: int, 
        product_id: int,
        quantity: int, 
        discount: float, 
        total_price: int, 
        sales_date: datetime,
        transaction_number: str
    ):
        self.sales_id = sales_id
        self.sales_person_id = sales_person_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity
        self.discount = discount
        self.total_price = total_price
        self.sales_date = sales_date  
        self.transaction_number = transaction_number
