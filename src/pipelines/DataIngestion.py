import os
import warnings
import pandas as pd
from database.db_engine import cursor, conn
from models.Categories import Category
from models.Cities import City
from models.Costumers import Customer
from models.Countries import Country
from models.Employees import Employee
from models.Products import Product
from models.Sales import Sale
from dotenv import load_dotenv
load_dotenv()


class DataIngestion:

    def __init__(self, model_class: type):
        allowed_models = [Category, City, Customer, Country, Employee, Product, Sale]
        
        if model_class not in allowed_models:
            raise ValueError("ERROR: Model class not allowed.")
        
        self.model_class = model_class
        self.table_map = {
            Category: "categories",
            City: "cities",
            Customer: "customers",
            Country: "countries",
            Employee: "employees",
            Product: "products",
            Sale: "sales"
        }

    @staticmethod
    def generate_sql_path(script_name: str):
        actual_dir = os.path.dirname(os.path.abspath(__file__))
        sql_route = os.path.join(actual_dir, "..", "..", "sql", script_name)
        return os.path.normpath(sql_route)
    
    def generate_externaldata_path(self):
        actual_dir = os.path.dirname(os.path.abspath(__file__))
        csv_route = os.path.join(actual_dir, "..", "..", "data", f"{self.table_map[self.model_class]}.csv")
        return os.path.normpath(csv_route) 

    def create_tables_from_sql_file(self):
        '''
            This method verify if the tables are created in the database. 
            In case that the tables were not created before, it creates all the tables missing
        '''
        path = self.generate_sql_path(script_name='create_tables.sql')

        if not os.path.exists(path):
            raise FileNotFoundError(f"SQL file not found: {path}")

        with open(path, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]

        for statement in statements:
            try:
                cursor.execute(statement)
            
            except Exception as e:
                print(f"Error al ejecutar la sentencia:\n{statement}\nError: {e}")

        conn.commit()
        print("All tables were successfully created")
    
    def load_external_data(self):
        try:
            csv_path = self.generate_externaldata_path()
            df = pd.read_csv(csv_path)
            print("External data was successfuly loaded")

            return df

        except Exception as e:
            raise ValueError(f"ERROR getting external data: {e}")

    def upload_data(self):
        self.create_tables_from_sql_file()
        table_name = self.table_map[self.model_class]
        external_data = self.load_external_data()

        model_instance = self.model_class(data=external_data)  
        validated_data = model_instance.validate()        
        
        if validated_data.empty:
            warnings.warn(f"WARNING: All categories provided already existed in the database. No data was uploaded.")
            return

        file_path = os.path.join(os.getenv("LOAD_DATA_INFILE_DIR"), 'data.csv')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  

        validated_data.to_csv(file_path, index=False, encoding='utf-8')
        temp_file_name = file_path.replace("\\", "/")

        try:
            sql = f"""
                LOAD DATA INFILE '{temp_file_name}'
                INTO TABLE {table_name}
                FIELDS TERMINATED BY ',' 
                ENCLOSED BY '"'
                LINES TERMINATED BY '\n'
                IGNORE 1 ROWS
                ({', '.join(validated_data.columns)});
            """
            cursor.execute(sql)
            conn.commit()
            print(f"Data uploaded successfully into '{table_name}'.")

        except Exception as e:
            conn.rollback()
            print(f"ERROR uploading data to table '{table_name}': {e}")


