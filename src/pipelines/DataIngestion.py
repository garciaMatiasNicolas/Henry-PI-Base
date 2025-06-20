import os
import warnings
import pandas as pd
from ..database.DataBase__singleton import MySQLConnector 
from ..models.Categories import Category
from ..models.Cities import City
from ..models.Customers import Customer
from ..models.Countries import Country
from ..models.Employees import Employee
from ..models.Products import Product
from ..factory.DataLoaderFactory import DataLoaderFactory
from ..factory.DataValidationFactory import DataValidationFactory
from ..models.Sales import Sale
from dotenv import load_dotenv
load_dotenv()


class DataIngestion:

    def __init__(self, model_class: type, loader_type: str, database: MySQLConnector):
        self.table_map: dict = {
            Category: "categories",
            City: "cities",
            Customer: "customers",
            Country: "countries",
            Employee: "employees",
            Product: "products",
            Sale: "sales"
        }
        self.model_class: type = model_class
        self.loader_type: str = loader_type
        
        allowed_models = list(self.table_map.keys())
        if model_class not in allowed_models:
            raise ValueError("ERROR: Model class not allowed.")
        
        self.db: MySQLConnector = database
        self.db.connect()
        
    @staticmethod
    def generate_sql_path(script_name: str) -> str: 
        '''
            This method returns the file path of the sql script
        '''
        actual_dir = os.path.dirname(os.path.abspath(__file__))
        sql_route = os.path.join(actual_dir, "..", "..", "sql", script_name)
        return os.path.normpath(sql_route)
    
    def generate_externaldata_path(self) -> str: 
        '''
            This method returns the file path of the .csv 
            with the data to upload according to the model
        '''
        actual_dir = os.path.dirname(os.path.abspath(__file__))
        csv_route = os.path.join(actual_dir, "..", "..", "data", f"{self.table_map[self.model_class]}.csv")
        return os.path.normpath(csv_route) 
    
    def load_external_data(self) -> pd.DataFrame:
        '''
            This method use the data loader factory to load the external data
            You can load JSON data or CSV data
        '''
        path = self.generate_externaldata_path() 
        loader = DataLoaderFactory.create_loader(source=self.loader_type, filepath=path)
        data = loader.load()
        return data

    def upload_data(self):
        '''
            This method upload the data to the correct model in the database
            with a previous validation that depends on every model
        '''
        self.db.create_tables_from_sql_file(path=self.generate_sql_path(script_name="create_tables.sql"))
        table_name = self.table_map[self.model_class]
        external_data = self.load_external_data()

        validation_class = DataValidationFactory.get_validation_class(model=self.table_map[self.model_class], data=external_data) 
        validated_data = validation_class.validate(db=self.db)     

        file_path = os.path.join(os.getenv("LOAD_DATA_INFILE_DIR"), 'data.csv')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  

        validated_data.to_csv(file_path, index=False, encoding='utf-8')
        temp_file_name = file_path.replace("\\", "/")

        self.db.load_data_infile(temp_file_name=temp_file_name, table=table_name, data=validated_data)

