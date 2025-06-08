class CRUDQueryBuilder:

    def __init__(
        self, 
        table: str, 
        query_type: str = "READ", 
        filters: list = [], 
        values: dict = {},
        aggregates: list = []
    ):
        self.table = table
        self.query_type = query_type.upper()
        self.filters = filters  
        self.values = values    
        self.aggregates = aggregates
        self.query = ""

        if self.query_type == "READ":
            self.build_select()
        elif self.query_type == "CREATE":
            self.build_insert()
        elif self.query_type == "UPDATE":
            self.build_update()
        elif self.query_type == "DELETE":
            self.build_delete()
        else:
            raise ValueError("ERROR: Query type not supported")

    def build_where_clause(self):
        if not self.filters:
            return ""
        
        conditions = [f"{col} {op} {repr(val) if isinstance(val, str) else val}" for col, op, val in self.filters]
        return " WHERE " + " AND ".join(conditions)

    def build_select(self):
        if self.aggregates:
            select_clause = ", ".join(self.aggregates)
        else:
            select_clause = "*"
        self.query = f"SELECT {select_clause} FROM {self.table}" + self.build_where_clause() + ";"

    def build_insert(self):
        if not self.values:
            raise ValueError("INSERT operation requires values.")
        
        columns = ", ".join(self.values.keys())
        vals = ", ".join([repr(val) if isinstance(val, str) else str(val) for val in self.values.values()])
        self.query = f"INSERT INTO {self.table} ({columns}) VALUES ({vals});"

    def build_update(self):
        if not self.values:
            raise ValueError("UPDATE operation requires values.")
        
        set_clause = ", ".join(
            [f"{col} = {repr(val) if isinstance(val, str) else val}" for col, val in self.values.items()]
        )
        self.query = f"UPDATE {self.table} SET {set_clause}" + self.build_where_clause() + ";"

    def build_delete(self):
        self.query = f"DELETE FROM {self.table}" + self.build_where_clause() + ";"

    def get_query(self):
        return self.query
