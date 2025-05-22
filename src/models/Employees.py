from datetime import date

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

