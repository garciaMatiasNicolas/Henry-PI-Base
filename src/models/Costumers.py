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
