#!/usr/bin/env python3

import sqlite3
import csv
import sys

def main(csv_path: str, db_path: str = "./3241.db"):
    """
    Reads data from `csv_path` and inserts into an SQLite database at `db_path`.
    """



    # 1. Connect to (or create) the SQLite database.
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    create_tables(cur)

    # 3. Read your CSV file. 
    #    We'll assume the CSV has headers that match the dictionary keys below.
    with open(csv_path, mode="r", encoding='latin-1', errors='replace') as f:
        reader = csv.DictReader(f)

        for row in reader:
            # --- Insert into Customer table ---
            # Example CSV columns:
            # row["CustomerID"], row["CustomerName"], row["CustomerAddress"]
            ISBN = row["ISBN"]
            print(f"ISBN: {ISBN}")
            

            cur.execute("""
                INSERT OR IGNORE INTO Book (ISBN)
                VALUES (?);
            """, (ISBN,))

            # --- Insert into Product table ---
            # Example CSV columns:
            # row["Item_ID"], row["Price"], row["Quantity"], row["Title"], row["Year_Published"]
            
            price = row["Price"]
            
            title = row["Title"]
            year_published = row["Year"]

            cur.execute("""
                INSERT OR IGNORE INTO Product ( Price, Title, Year_Published)
                VALUES (?, ?, ?);
            """, ( price, title, year_published))



            # --- Insert into Product_Genre table (example) ---
            # CSV columns might be: row["Genre"]
            if "Category" in row and row["Category"]:
                genre = row["Category"]
                cur.execute("""
                    INSERT OR IGNORE INTO Product_Genre ( Genre)
                    VALUES (?);
                """, ( genre,))

            # --- Insert into Book table (example) ---
            # CSV columns might be: row["ISBN"]
            if "ISBN" in row and row["ISBN"]:
                isbn = row["ISBN"]
                # Book is identified by ISBN + references product
                cur.execute("""
                    INSERT OR IGNORE INTO Book (ISBN)
                    VALUES (?);
                """, (isbn,))




    # 4. Commit changes and close connection.
    conn.commit()
    conn.close()

def create_tables(cur: sqlite3.Cursor):
    """
    Creates the tables in the database. Make sure this matches your schema exactly.
    If your tables are already created, comment these out.
    """

    # Customer table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Customer (
            CustomerID   INTEGER PRIMARY KEY,
            Name         TEXT,
            Address      TEXT
        );
    """)

    # Product table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Product (
            Item_ID         INTEGER PRIMARY KEY,
            Price           REAL,
            Quantity        INTEGER,
            Title           TEXT,
            Year_Published  TEXT
        );
    """)

    # Order table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "Order" (
            Order_ID         INTEGER PRIMARY KEY,
            Delivery_Status  TEXT,
            Payment_Info     TEXT,
            Date_of_Purchase TEXT,
            CustomerID       INTEGER,
            FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
        );
    """)

    # Ordered_Product table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Ordered_Product (
            Order_ID  INTEGER,
            Item_ID   INTEGER,
            PRIMARY KEY (Order_ID, Item_ID),
            FOREIGN KEY (Order_ID) REFERENCES "Order"(Order_ID),
            FOREIGN KEY (Item_ID)  REFERENCES Product(Item_ID)
        );
    """)

    # Creator table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Creator (
            DOB        TEXT,
            FirstName  TEXT,
            MiddleName TEXT,
            LastName   TEXT,
            PRIMARY KEY (FirstName, MiddleName, LastName)
        );
    """)

    # Publisher table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Publisher (
            PublisherID INTEGER PRIMARY KEY,
            Address     TEXT
        );
    """)

    # Review table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Review (
            ReviewID   INTEGER PRIMARY KEY,
            Text       TEXT,
            Date       TEXT,
            Score      INTEGER,
            CustomerID INTEGER,
            ItemID     INTEGER,
            FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
            FOREIGN KEY (ItemID)    REFERENCES Product(Item_ID)
        );
    """)

    # Product_Genre table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Product_Genre (
            Item_ID INTEGER,
            Genre   TEXT,
            PRIMARY KEY (Item_ID, Genre),
            FOREIGN KEY (Item_ID) REFERENCES Product(Item_ID)
        );
    """)

    # Book table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Book (
            ISBN    TEXT,
            Item_ID INTEGER PRIMARY KEY,
            FOREIGN KEY (Item_ID) REFERENCES Product(Item_ID)
        );
    """)

    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Record (
            Track_List TEXT,
            Catalog_num  TEXT,
            Item_ID    INTEGER PRIMARY KEY,
            FOREIGN KEY (Item_ID) REFERENCES Product(Item_ID)
        );
    """)

    # Created_Product table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Created_Product (
            Item_ID    INTEGER,
            FirstName  TEXT,
            MiddleName TEXT,
            LastName   TEXT,
            PRIMARY KEY (Item_ID, FirstName, MiddleName, LastName),
            FOREIGN KEY (Item_ID)    REFERENCES Product(Item_ID),
            FOREIGN KEY (FirstName, MiddleName, LastName)
            REFERENCES Creator(FirstName, MiddleName, LastName)
        );
    """)

    # Published_Product table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Published_Product (
            Item_ID      INTEGER,
            Publisher_ID INTEGER,
            PRIMARY KEY (Item_ID, Publisher_ID),
            FOREIGN KEY (Item_ID)      REFERENCES Product(Item_ID),
            FOREIGN KEY (Publisher_ID) REFERENCES Publisher(PublisherID)
        );
    """)
    

if __name__ == "__main__":
    # Usage example:
    #   python script_name.py data.csv my_db.db
    #
    # If no arguments are given, it defaults to ./data/data.csv and 3241.db.
    csv_file = "./data/data.csv"
    db_file = "./3241.db"

    if len(sys.argv) >= 2:
        csv_file = sys.argv[1]
    if len(sys.argv) >= 3:
        db_file = sys.argv[2]

    main(csv_file, db_file)
