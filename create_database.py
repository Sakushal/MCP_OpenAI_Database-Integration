import sqlite3
import pandas as pd


CSV_FILES = {
    "policies": "policies.csv",
    "customers": "customers.csv",
    "claims": "claims.csv",
    "payments": "payments.csv",
}

DB_FILE = "life_insurance.db"

def create_database():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    print(f"Creating database: {DB_FILE}")

    for table, file in CSV_FILES.items():
        print(f"Importing {file} -> {table}...")
        try:
            df = pd.read_csv(file)
            # Drop table if exists to avoid conflicts
            cur.execute(f"DROP TABLE IF EXISTS {table}")
            conn.commit()

            
            df.to_sql(table, conn, if_exists="replace", index=False)
            print(f"Imported {table} successfully!")
        except FileNotFoundError:
            print(f"ERROR: File {file} not found. Ensure all CSV files are present.")
            conn.close()
            return

    conn.close()
    print("Database creation completed!")

if __name__ == "__main__":
    create_database()
