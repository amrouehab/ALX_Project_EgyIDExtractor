import pyodbc

class SQLDatabase:
    def __init__(self, server, database, username=None, password=None):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection = None

    def connect(self):
        try:
            if self.username and self.password:
                # SQL Server Authentication
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"UID={self.username};"
                    f"PWD={self.password}"
                )
            else:
                # Integrated Security (Windows Authentication)
                conn_str = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"Trusted_Connection=yes;"
                )
            self.connection = pyodbc.connect(conn_str)
        except pyodbc.Error as e:
            print("Error: Failed to connect to the database:", e)
            raise

    def execute_query(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                self.connection.commit()
        except pyodbc.Error as e:
            print("Error: Failed to execute query:", e)
            self.connection.rollback()
            raise

    def create_table(self, table_name, columns):
        print("Creating Table")
        # Assuming columns is a dictionary with column names and data types
        column_defs = ', '.join([f"{column} {data_type}" for column, data_type in columns.items()])
        query = f"CREATE TABLE {table_name} ({column_defs})"
        self.execute_query(query)
        print(f"Table {table_name} created with columns: {column_defs}")

    def insert_record(self, table_name, record):
        column_names = ', '.join(record.keys())
        placeholders = ', '.join(['?'] * len(record))
        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        self.execute_query(query, tuple(record.values()))

    def database_exists(self):
        query = f"SELECT name FROM sys.databases WHERE name = '{self.database}'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone() is not None

    def table_exists(self, table_name):
        query = f"SELECT OBJECT_ID('{table_name}', 'U')"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone() is not None

    def close_connection(self):
        if self.connection:
            self.connection.close()
            self.connection = None
