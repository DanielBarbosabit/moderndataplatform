import psycopg2

class PostgresConnector(object):
    def __init__(self, host, port, dbname, user, password):
        """
        Initialize the connection parameters.
        """
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        """
        Establish a connection to the PostgreSQL database.
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            print("Connection to the database established successfully.")
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            raise

    def execute_query(self, query, params=None):
        """
        Execute a query on the database.
        :param query: SQL query to execute
        :param params: Parameters for the SQL query
        :return: Query result
        """
        if not self.connection:
            raise Exception("Connection is not established. Call the `connect` method first.")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if query.strip().lower().startswith("select"):
                    result = cursor.fetchall()
                    return result
                else:
                    self.connection.commit()
                    print("Query executed successfully.")
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            raise

    def close(self):
        """
        Close the connection to the database.
        """
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def get_tables(self, schema_name):
        """
        Get the list of tables in a specific schema.
        """
        query = """
        SELECT table_name 
        FROM information_schema.tables
        WHERE table_schema = %s AND table_type = 'BASE TABLE';
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, (schema_name,))
            tables = [row[0] for row in cursor.fetchall()]
        return tables

    def fetch_first_rows(self, schema_name, table_name, row_count=2):
        """
        Fetch the first `row_count` rows from a specific table.
        """
        query = f"SELECT * FROM {schema_name}.{table_name} LIMIT {row_count};"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            columns = [desc[0] for desc in cursor.description]  # Get column names
            rows = cursor.fetchall()
        return columns, rows
