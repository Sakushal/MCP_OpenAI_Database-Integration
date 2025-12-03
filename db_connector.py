import sqlite3
import pandas as pd

# Name of database file
DATABASE_FILE = "life_insurance.db" 

def execute_db_query(query: str) -> str:
    """
    Connects to the SQLite database and executes a read-only SQL query.

    Args:
        query: The SQL query to execute (e.g., "SELECT * FROM my_table").

    Returns:
        A string representation of the query results (e.g., JSON or formatted text).
    """
    conn = None
    try:
        # 1. Connecting to the SQLite database
        conn = sqlite3.connect(DATABASE_FILE)
        
        # 2. Execute the query
        df = pd.read_sql_query(query, conn)
        
        # 3. Format the results as a clean JSON string for the LLM
        # Limiting to the first 10 rows to prevent excessively long responses
        if len(df) > 10:
            result = df.head(10).to_json(orient='records', indent=2)
            result = f"NOTE: Results truncated to 10 rows. Total rows found: {len(df)}\n\n{result}"
        else:
            result = df.to_json(orient='records', indent=2)
            
        return result
        
    except sqlite3.Error as e:
        return f"Database Error: {e}"
    except pd.io.sql.DatabaseError as e:
        return f"Query Error: The provided SQL query failed. Error: {e}"
    finally:
        if conn:
            conn.close()


def get_db_schema() -> str:
    """Retrieves the DDL (Data Definition Language) for all tables in the database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)


        cursor = conn.cursor()
        
        # Query to get the schema for all tables
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema = ""
        for name, sql in tables:
            schema += f"Table: {name}\nSQL: {sql}\n---\n"
            
        return schema.strip()
        
    except sqlite3.Error as e:
        return f"Database Error while fetching schema: {e}"
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
   
    schema = get_db_schema()
    print("--- Database Schema ---")
    print(schema)
    print("\n--- Test Query ---")
    
