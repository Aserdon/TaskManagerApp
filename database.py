import sqlite3
import os
from utils import get_base_path

def get_db_connection():
    """
    Establishes and returns a connection to the SQLite database.
    Ensures the database directory exists before connecting.
    
    Returns:
        sqlite3.Connection: A connection object with row factory set to sqlite3.Row.
    Raises:
        sqlite3.Error: If there's an issue connecting to the database.
    """
    try:
        db_path = os.environ.get("FLASK_DATABASE", os.path.join(get_base_path(), 'instance/tasks.db'))
        # Debugging: Uncomment for troubleshooting database path issues
        # print(f"Database path being used: {db_path}")

        # Ensure the instance directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error when connecting to the database: {e}")
        raise
    

def init_db(schema_file='schema.sql'):
    """
    Initializes the database using the provided schema file.

    Args:
        schema_file (str): The filename of the schema script (default: 'schema.sql').

    Raises:
        FileNotFoundError: If the schema file does not exist.
        sqlite3.Error: If there's an issue executing the schema script.
    """
    try:
        base_path = get_base_path()
        schema_path = os.path.join(base_path, schema_file)

        if not os.path.exists(schema_path):
            raise FileNotFoundError(f"Schema file not found: {schema_path}")
        
        conn = get_db_connection()
        with open(schema_path) as f:
            conn.executescript(f.read())
        conn.close()
    except FileNotFoundError as e:
        print(f"File error: {e}")
        raise
    except sqlite3.Error as e:
        print(f"Error initializing the database: {e}")
        raise
