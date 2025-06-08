from .concrete.validation import CategoryValidation, CityValidation, EmployeeValidation, ProductValidation, CountryValidation, CustomerValidation, SalesValidation
import pandas as pd


class DataValidationFactory:
    
    def get_validation_class(model: str, data: pd.DataFrame):
        if model == "categories":
            return CategoryValidation.CategoryValidation(data=data)
        elif model == "cities":
            return CityValidation.CityValidation(data=data)
        elif model == "employees":
            return EmployeeValidation.EmployeeValidation(data=data)
        elif model == "products":
            return ProductValidation.ProductValidation(data=data)
        elif model == "countries":
            return CountryValidation.CountryValidation(data=data)
        elif model == "customers":
            return CustomerValidation.CustomerValidation(data=data)
        elif model == "sales":
            return SalesValidation.SaleValidation(data=data)
        else:
            raise ValueError("Model not supported")