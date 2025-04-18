import sqlite3
import csv
import sys
def main(csv_path: str, db_path: str = "./3241.db"):
    """
    Reads data from `csv_path` and inserts into an SQLite database at `db_path`.
    """
    isbns :set = set()
    author_ids : dict = {}
    publisher_ids : dict = {}
    curr_publisher_id : int = 1
    curr_author_id : int = 1
    # 1. Connect to (or create) the SQLite database.
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    #Resest database
    drop_tables(cur)
    create_tables(cur)
    

    # 3. Read your CSV file. 
    #    We'll assume the CSV has headers that match the dictionary keys below.
    with open(csv_path, mode="r", encoding='latin-1', errors='replace') as f:
        reader = csv.DictReader(f)
        product_id : int = 0
        publisher_id : int = 1
        for row in reader:
            price = row["Price"].replace("$", "")
            quantity = 1
            title = row["Title"]
            year_published = row["Year"]

            isbn = row["ISBN"]
            #if there is a row with an isbn 
            if(isbn):
                if (isbn not in isbns):
                    isbns.add(isbn)
                else:
                    cur.execute("""
                        UPDATE PRODUCT SET Quantity = Quantity + 1 WHERE Item_ID = :id
                    """, {"id": product_id})
                    continue
                product_id += 1
                
                #Add data to the product table
                cur.execute("""
                    INSERT OR IGNORE INTO PRODUCT (Item_ID, Price, Quantity, Title, Year_Published)
                    VALUES (?, ?, ?, ?, ?)
                """, (product_id, price, quantity, title, year_published))

                #Add data to the Book table
                cur.execute("""
                    INSERT OR IGNORE INTO BOOK(Item_ID, ISBN)
                    VALUES (?, ?)
                """, (product_id, isbn))

                publisher = row["Publisher"].strip()
                publisher_id : int = 0
                #If this publisher has not been seen yet
                if(publisher not in publisher_ids.keys()):
                    publisher_ids[publisher] = curr_publisher_id
                    publisher_id = curr_publisher_id

                    #Add the publisher to the Publisher table
                    cur.execute("""
                        INSERT OR IGNORE INTO PUBLISHER(Publisher_ID, Name)
                        VALUES (?, ?)
                    """, (publisher_id, publisher))
                    curr_publisher_id += 1
                else:
                    publisher_id = publisher_ids[publisher]

                # Add the data to the PUBLISHED_PRODUCT table
                cur.execute("""
                    INSERT OR IGNORE INTO PUBLISHED_PRODUCT(Item_ID, Publisher_ID)
                    VALUES(?, ?)
                """, (product_id, publisher_id))

                genres = row["Category"].split(" & ")
                for genre in genres:
                    # Add the Genre(s) associated with each book
                    cur.execute("""
                        INSERT OR IGNORE INTO PRODUCT_GENRE(Item_ID, Genre)
                        VALUES(?, ?)
                    """, (product_id, genre))

            # Get entire author name
            author = row["Author(s)"].strip()
            # Split the entire name based on " "
            names = author.split(" ")
            author_id : int = 0
            # If this author has not been encountered yet
            if (author not in author_ids.keys()):
                author_ids[author] = curr_author_id
                author_id = curr_author_id
                curr_author_id += 1
                
                # Add the new author to the authors table
                if len(names) >= 3:
                    #Get the first name
                    first_index = author.index(" ")
                    first_name = author[0: first_index]
                    # Get the last name
                    last_index = author.rindex(" ") + 1
                    last_name = author[last_index:]
                    middle_name = author[first_index: last_index].strip()
                    cur.execute("""
                        INSERT OR IGNORE INTO CREATOR(Creator_ID, First_Name, Middle_Name, Last_Name)
                           VALUES(?, ?, ?, ?)
                    """, (author_id, first_name, middle_name, last_name))
                else:
                    cur.execute("""
                            INSERT OR IGNORE INTO CREATOR(Creator_ID, First_Name, Last_Name)
                               VALUES(?, ?, ?)
                        """, (author_id, names[0], names[1]))
            else:
                author_id = author_ids[author]

            # Associate the author with the book they have created
            cur.execute("""
                INSERT OR IGNORE INTO CREATED_PRODUCT(Item_ID, Creator_ID)
                VALUES(?, ?)
            """, (product_id, author_id))

    #Populate the rest of the tables by reading their respective data files
    populate_customers(cur)
    populate_orders(cur)
    populate_records(cur, product_id, publisher_ids, curr_publisher_id, author_ids, curr_author_id)
    populate_ordered_product(cur)
    populate_reviews(cur)
    populate_songs(cur)
    populate_songs_records(cur)

    # Set Names that are empty to null
    cur.execute("""
    UPDATE Creator SET Middle_Name=null WHERE Middle_Name = "";
    """)
    cur.execute("""
    UPDATE Creator SET Last_Name=null WHERE Last_Name = "";
    """)
    # Create the indicies implemented on this database
    cur.execute("""
        CREATE INDEX Creator_Name ON Creator(First_Name, Middle_Name, Last_Name);
    """)
    cur.execute("""
        CREATE INDEX Product_Title ON Product(Title);
    """)

    # Create the views used within the database
    cur.execute("""CREATE VIEW Highly_Rated_Products AS
        SELECT P.Title, R.Score
        FROM Product AS P, Review AS R
        WHERE P.Item_ID = R.Item_ID
        AND R.Score >= (
            SELECT AVG(R.Score) as avg_score
            FROM Review AS R);
    """)

    cur.execute("""
    CREATE VIEW Number_Of_Products AS
    SELECT Product.Title, CONCAT(Creator.First_Name, ' ', Creator.Middle_Name, ' ', Creator.Last_Name) as Creator_Name, products_created
    FROM Creator,Product, Created_Product, (
        SELECT Creator.Creator_ID, Count(*) as products_created
        FROM Created_Product, Creator
        WHERE Creator.Creator_ID = Created_Product.Creator_ID
        GROUP BY Creator.Creator_ID) AS Counts
    WHERE Creator.Creator_ID = Counts.Creator_ID
    AND Creator.Creator_ID = Created_Product.Creator_ID
    AND Product.Item_ID = Created_Product.Item_ID;
    """)
    # 4. Commit changes and close connection.
    conn.commit()
    conn.close()

def drop_tables(cur: sqlite3.Cursor):
    cur.execute("""
        DROP VIEW IF EXISTS Highly_Rated_Products;
    """)
    cur.execute("""
        DROP VIEW IF EXISTS Number_Of_Products;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Songs_On_Records;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Song;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Published_Product;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Created_Product;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Record;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Book;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Product_Genre;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Review;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Publisher;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Creator;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Ordered_Product;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS "Order";
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Product;
    """)
    cur.execute("""
        DROP TABLE IF EXISTS Customer;
    """)

def populate_songs(cur: sqlite3.Cursor):
    with open(r"data\song_data.csv", mode = "r", encoding = 'latin-1', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT OR IGNORE INTO Song
                VALUES(?, ?)
            """, (row["SongID"], row["Name"]))

def populate_records(cur: sqlite3.Cursor, product_id : int, publisher_ids: dict, curr_publisher_id: int, author_ids : dict, curr_author_id: int):
    item_id : int = product_id
    record_id : int = 1
    with open(r"data\record_data.csv", mode = "r", encoding='latin-1', errors='replace' ) as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row["Title"]
            if (title):
                item_id += 1
                cur.execute("""
                    INSERT OR IGNORE INTO PRODUCT
                    VALUES(?, ?, ?, ?, ?)
                """, (item_id, row["Price"], 1, row["Title"], row["Year"]))
                
                cur.execute("""
                    INSERT OR IGNORE INTO RECORD
                    VALUES(?, ?)
                """, (item_id, row["Catalog#"]))

                publisher = row["Publisher"]
                if (publisher not in publisher_ids.keys()):
                    publisher_ids[publisher] = curr_publisher_id
                    curr_publisher_id += 1

                cur.execute("""
                    INSERT OR IGNORE INTO PUBLISHER(Publisher_id, Name)
                    VALUES(?, ?)
                """, (publisher_ids[publisher], publisher))

                cur.execute("""
                    INSERT OR IGNORE INTO PUBLISHED_PRODUCT
                    VALUES (?, ?)
                """, (item_id, publisher_ids[publisher]))

                genres = row["Genre"].split(" & ")
                for genre in genres:
                    # Add the Genre(s) associated with each record
                    cur.execute("""
                        INSERT OR IGNORE INTO PRODUCT_GENRE(Item_ID, Genre)
                        VALUES(?, ?)
                    """, (item_id, genre))

            first_name = row["First_Name"]
            middle_name = row["Middle_Name"]
            last_name = row["Last_Name"]
            creator = first_name + middle_name + last_name
            if (creator not in author_ids.keys()):
                author_ids[creator] = curr_author_id
                curr_author_id += 1

            cur.execute("""
                INSERT OR IGNORE INTO CREATOR(Creator_ID, First_Name, Middle_Name, Last_Name)
                VALUES(?, ?, ?, ?)
            """, (author_ids[creator], first_name, middle_name, last_name))

            cur.execute("""
                INSERT OR IGNORE INTO CREATED_PRODUCT
                VALUES(?, ?)
            """, (item_id, author_ids[creator]))

def populate_songs_records(cur: sqlite3.Cursor):
    with open(r"data\songs_on_albums_data.csv", mode ="r", encoding='latin-1', errors = 'replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT OR IGNORE INTO "Songs_On_Records"
                VALUES(?, ?)
            """, (row["ItemID"], row["SongID"]))

def populate_orders(cur: sqlite3.Cursor):
    with open("data\order_data.csv", mode = "r", encoding='latin-1', errors='replace' ) as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT OR IGNORE INTO "ORDER"
                VALUES (?, ?, ?, ?, ?)
            """, (row["Order_ID"], row["Delivery_Status"], row["Payment_Info"], row["Date_Of_Purchase"], row["Customer_ID"]))
            
def populate_customers(cur: sqlite3.Cursor):
     customer_id : int = 1
     with open("data\customer_data.csv", mode="r", encoding='latin-1', errors='replace') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT OR IGNORE INTO CUSTOMER(Customer_ID, Name, Address)
                VALUES (?, ?, ?)
            """, (customer_id, row["Name"], row ["Address"]))
            customer_id += 1

def create_tables(cur: sqlite3.Cursor):
    """
    Creates the tables in the database. Make sure this matches your schema exactly.
    If your tables are already created, comment these out.
    """

    # Customer table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Customer (
            Customer_ID   INTEGER NOT NULL,
            Name         VARCHAR(30) NOT NULL,
            Address      VARCHAR(30),
            PRIMARY KEY(Customer_ID)
        );
    """)
   
    # Product table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Product (
            Item_ID         INTEGER NOT NULL,
            Price           DECIMAL(5,2) NOT NULL,
            Quantity        INTEGER NOT NULL,
            Title           VARCHAR(50) NOT NULL,
            Year_Published  INTEGER,
            PRIMARY KEY(Item_ID)
        );
    """)

    # Order table
    cur.execute("""
        CREATE TABLE if Not EXISTS "Order" (
	        "Order_ID"	INTEGER NOT NULL,
	        "Delivery_Status"	VARCHAR(10) NOT NULL,
	        "Payment_Info"	VARCHAR(20) NOT NULL,
	        "Date_of_Purchase"	DATE NOT NULL,
	        "Customer_ID"	INTEGER NOT NULL,
	        PRIMARY KEY("Order_ID"),
	        FOREIGN KEY("Customer_ID") REFERENCES "Customer"("Customer_ID")
        );
    """)

    # Ordered_Product table
    cur.execute("""
        CREATE TABLE if Not EXISTS "Ordered_Product" (
	        "Order_ID"	INTEGER NOT NULL,
	        "Item_ID"	INTEGER NOT NULL,
            "Quantity" INTEGER NOT NULL,
	        PRIMARY KEY("Order_ID","Item_ID"),
	        FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID"),
	        FOREIGN KEY("Order_ID") REFERENCES "Order"("Order_ID")
        );
    """)

    # Creator table
    cur.execute("""
        CREATE TABLE if Not EXISTS "Creator" (
	        "Creator_ID" INTEGER NOT NULL,
	        "First_Name" VARCHAR(30) NOT NULL,
            "Middle_Name" VARCHAR(15),
            "Last_Name" VARCHAR(15),
	        "DOB"	DATE,
	        PRIMARY KEY("Creator_ID")
        );
    """)

    # Publisher table
    cur.execute("""
        CREATE TABLE if Not EXISTS "Publisher" (
	        "Publisher_ID"	INTEGER NOT NULL,
	        "Name"      VARCHAR(30) NOT NULL,
	        "Address"	VARCHAR(30),
	        PRIMARY KEY("Publisher_ID")
        );
    """)

    # Review table
    cur.execute("""
        CREATE TABLE if Not EXISTS "Review" (
	        "Review_ID"	INTEGER NOT NULL,
	        "Text"	VARCHAR(100),
	        "Date" DATE,
	        "Score"	INTEGER NOT NULL CHECK(Score >= 0 and Score <= 10),
	        "Customer_ID"	INTEGER NOT NULL,
	        "Item_ID"	INTEGER NOT NULL,
	        PRIMARY KEY("Review_ID"),
	        FOREIGN KEY("Customer_ID") REFERENCES "Customer"("Customer_ID"),
	        FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID")
        );
    """)

    # Product_Genre table
    cur.execute("""
        CREATE TABLE if Not EXISTS "Product_Genre" (
	        "Item_ID"	INTEGER NOT NULL,
	        "Genre"	VARCHAR(15) NOT NULL,
	        PRIMARY KEY("Item_ID","Genre"),
	        FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID")
        );
    """)

    # Book table
    cur.execute("""
        CREATE TABLE if Not EXISTS "Book" (
	        "Item_ID"	INTEGER NOT NULL,
	        "ISBN"	CHAR(10) NOT NULL,
	        PRIMARY KEY("Item_ID"),
	        FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID")
        );
    """)

    # Record Table
    cur.execute("""
        CREATE TABLE if Not EXISTS "Record" (
	        "Item_ID"	INTEGER NOT NULL,
	        "Catalog#"	VARCHAR(15) NOT NULL,
	        PRIMARY KEY("Item_ID"),
	        FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID")
        );
    """)

    # Created_Product table
    cur.execute("""
        CREATE TABLE if Not EXISTS "Created_Product" (
	        "Item_ID"	INTEGER NOT NULL,
	        "Creator_ID" INTEGER NOT NULL,
	        PRIMARY KEY("Item_ID","Creator_ID"),
	        FOREIGN KEY("Creator_ID") REFERENCES "Creator"("Creator_ID"),
	        FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID")
        );
    """)

    # Published_Product table
    cur.execute("""
        CREATE TABLE if Not EXISTS "Published_Product" (
	        "Item_ID"	INTEGER NOT NULL,
	        "Publisher_ID"	INTEGER NOT NULL,
	        PRIMARY KEY("Item_ID","Publisher_ID"),
	        FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID"),
	        FOREIGN KEY("Publisher_ID") REFERENCES "Publisher"("Publisher_ID")
        );
    """)
    # Songs Table
    cur.execute("""
        CREATE TABLE if Not EXISTS "Song" (
            "Song_ID"   INTEGER NOT NULL,
            "Name"      VARCHAR(30) NOT NULL,
            PRIMARY KEY("Song_ID")
        );
    """)
    # Song_On_Records Relation Table
    cur.execute("""
        CREATE TABLE if Not EXISTS "Songs_On_Records" (
        "Item_ID" INTEGER   NOT NULL,
        "Song_ID"   INTEGER NOT NULL,
        PRIMARY KEY("Item_ID", "Song_ID")
        FOREIGN KEY("Song_ID") REFERENCES "Song"("Song_ID")
        FOREIGN KEY("Item_ID") REFERENCES "Record"("Item_ID")
    );
    """)

def populate_ordered_product(cur: sqlite3.Cursor):
    with open(r"data\ordered_product_data.csv", mode = "r", encoding='latin-1', errors='replace' ) as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""
                INSERT OR IGNORE INTO Ordered_Product
                VALUES(?, ?, ?)
            """, (row["Order_ID"], row["Product_ID"], row["Quantity"]))
    
def populate_reviews(cur: sqlite3.Cursor):
    with open(r"data\review_data.csv", mode="r", encoding='latin-1', errors='replace') as f:
        reader = csv.DictReader(f)
        review_id : int = 1
        for row in reader:
            cur.execute("""
                INSERT OR IGNORE INTO Review
                VALUES(?, ?, ?, ?, ?, ?)
            """, (review_id, row["Text"], row["Date"], row["Score"], row["Customer_ID"], row["Item_ID"]))
            review_id += 1

if __name__ == "__main__":
    # Usage example:
    #   python script_name.py data.csv my_db.db
    # If no arguments are given, it defaults to ./data/data.csv and 3241.db.
    csv_file = "data/proj_data.csv"
    db_file = "final_version3241.db"

    if len(sys.argv) >= 2:
        db_file = sys.argv[1]

    main(csv_file, db_file)
