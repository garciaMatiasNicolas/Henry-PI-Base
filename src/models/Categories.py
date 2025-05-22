import pandas as pd
from database.db_engine import conn, cursor

class Category:
    
    def __init__(self, 
        data: pd.DataFrame,
    ):
        # Initializes the Category instance with the given DataFrame.
        self.data = data

    @staticmethod
    def get_last_id():
        # Returns the highest existing category_id from the database.
        query = '''
            SELECT MAX(category_id) 
            FROM categories
        '''
        cursor.execute(query)
        result = cursor.fetchone() 
        return result[0] if result and result[0] is not None else 0

    @staticmethod
    def get_all_categories():
        # Returns all distinct category names from the database.
        query = '''
            SELECT DISTINCT(category_name) 
            FROM categories
        '''
        cursor.execute(query)
        return [category[0] for category in cursor.fetchall()]

    def validate(self):
        # Validates and cleans the input data, removing duplicates,
        # assigning new IDs, and standardizing category names.
        expected_columns = ["CategoryID", "CategoryName"]

        if list(self.data.columns) != expected_columns:
            raise ValueError(f"ERROR: DataFrame must have exactly these columns: {expected_columns}")

        self.data["CategoryName"] = (
            self.data["CategoryName"]
            .astype(str)
            .str.replace(r"[\r\n\t]", "", regex=True)
            .str.strip()
            .str.lower()
        )

        categories_saved = [cat.lower().strip() for cat in self.get_all_categories()]

        self.data = self.data[~self.data["CategoryName"].isin(categories_saved)].copy()

        last_id = self.get_last_id()
        self.data["CategoryID"] = range(last_id + 1, last_id + 1 + len(self.data))

        if not self.data["CategoryName"].map(lambda x: isinstance(x, str)).all():
            raise ValueError("ERROR: All CategoryName values must be strings.")

        self.data.rename(columns={
            "CategoryID": "category_id",
            "CategoryName": "category_name"
        }, inplace=True)

        print("Category validation passed.")

        return self.data


    