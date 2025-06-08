from mysql.connector import connect
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
load_dotenv()


class MySQLConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance =super(MySQLConnector, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.config = {
            "host": os.getenv("DB_HOST"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASS"),
            "database": os.getenv("DB_DATABASE"),
            "port": os.getenv('DB_PORT')
        }
        self.connection = None
        self.cursor = None
        self.engine = None
        self._initialized = True
    
    def connect(self):
        if self.connection is None:
            try:
                self.connection = connect(**self.config)
                self.cursor = self.connection.cursor()
                self.engine = create_engine(
                    f"mysql+mysqlconnector://{self.config['user']}:{self.config['password']}@"
                    f"{self.config['host']}:{self.config['port']}/{self.config['database']}"
                )

                print(f"Database {self.config['database']} connection was made successfully")

            except Exception as err:
                print(f"Error trying to connect to database: {err}")
                raise 
    
    def query_select(self, query: str):
        if self.cursor is None:
            raise Exception("Database not connected")

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def query_alchemy(self, query: str) -> pd.DataFrame:
        if self.engine is None:
            raise Exception("Database engine not initialized")
    
        return pd.read_sql_query(query, self.engine)
    
    def query_insert_delete_update_triggers_idxs(self, typeof: str, query: str):
        if self.cursor is None:
            raise Exception("Database not connected")
        
        try:
            self.cursor.execute(query)
            self.connection.commit()
            print(f"{typeof} creado exitosamente")
        except Exception as e:
            self.connection.rollback()
            print(f"Error executing query: {e}")
            raise
    
    def load_data_infile(self, temp_file_name: str, table: str, data: pd.DataFrame):
        if self.cursor is None:
            raise Exception("Database not connected")
        
        try:
            sql = f"""
                LOAD DATA INFILE '{temp_file_name}'
                INTO TABLE {table}
                FIELDS TERMINATED BY ',' 
                ENCLOSED BY '"'
                LINES TERMINATED BY '\n'
                IGNORE 1 ROWS
                ({', '.join(data.columns)});
            """
            self.cursor.execute(sql)
            self.connection.commit()
            print(f"Data uploaded successfully into '{table}'.")

        except Exception as e:
            self.connection.rollback()
            print(f"ERROR uploading data to table '{table}': {e}")
    
    def create_tables_from_sql_file(self, path: str) -> None: 
        '''
            This method creates all the tables in the database selected
            if didnt exists any of them
        '''

        if not os.path.exists(path):
            raise FileNotFoundError(f"SQL file not found: {path}")

        with open(path, 'r', encoding='utf-8') as file:
            sql_script = file.read()

        statements = [stmt.strip() for stmt in sql_script.split(';') if stmt.strip()]

        for statement in statements:
            try:
                self.cursor.execute(statement)
            
            except Exception as e:
                print(f"Error al ejecutar la sentencia:\n{statement}\nError: {e}")

        self.connection.commit()
        print("All tables were successfully created")
    

    

