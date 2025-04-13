import psycopg2
from psycopg2 import sql
import json
from typing import List

class PostgresOperations:
    def __init__(self, host: str, database: str, user: str, password: str):
        """
        Initialize the database connection parameters.
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
    
    def _get_connection(self):
        """
        Establishes a connection to the PostgreSQL database.
        """
        conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        return conn
    
    def save_json_to_table(self, table_name: str, data: List[dict]):
        """
        Save a list of JSON objects into a PostgreSQL table.

        :param table_name: The table name to save the data.
        :param data: List of dictionaries representing the JSON data.
        """
        conn = None
        try:
            conn = self._get_connection()
            cur = conn.cursor()

            # Create an insert query dynamically based on the columns of the table
            columns = data[0].keys()  # Assuming all dictionaries have the same structure
            column_names = ', '.join(columns)
            values_placeholder = ', '.join([f"%({col})s" for col in columns])

            insert_query = sql.SQL(
                f"INSERT INTO {table_name} ({column_names}) VALUES ({values_placeholder})"
            )

            # Execute insert for each record in the data
            cur.executemany(insert_query, data)

            # Commit the transaction
            conn.commit()
            print(f"Successfully inserted {len(data)} records into {table_name}.")

        except Exception as e:
            print(f"Error occurred: {e}")
        finally:
            if conn:
                conn.close()
