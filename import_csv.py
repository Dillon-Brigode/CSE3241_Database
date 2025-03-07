import sqlite3
import csv

# Connect to the database
conn = sqlite3.connect('3241.db')
cursor = conn.cursor()


#read the csv file and insert the data into the database.
with open("./data/data.csv", 'r', encoding='latin-1', errors='replace') as f:
    reader = csv.reader(f)
    # Skip the first couple of lines that are not valid data
    # ( e.g. "Books,,,,,,,,," and the column header row )
    header_skipped = False
    for row in reader:
        # Check if it's a header or blank line
        if not header_skipped:
            # Skip lines until we reach actual data
            if "ISBN" in row or "Books" in row:
                # skip this line, next iteration might be data
                continue
            else:
                header_skipped = True

        # Now row should look like: [ISBN, Title, Author(s), Publisher, Year, Price, Category, ...]
        if len(row) < 7:
            continue  # skip empty lines or anything that doesn't match

        isbn = row[0].strip()
        title = row[1].strip()
        authors = row[2].strip()
        publisher = row[3].strip()
        year = row[4].strip()
        price = row[5].strip().replace('$','')  # remove $ sign
        category = row[6].strip()

        # 1) Insert into Product table
        # We'll assume you auto-generate an Item_ID or you keep track of it some other way.
        # But in your schema, Product.Item_ID is PRIMARY KEY and NOT NULL, so let's do something like:
        cursor.execute("""
            INSERT INTO Product (Item_ID, Price, Quantity, Title, Year_Published)
            VALUES (NULL, ?, 0, ?, ?)
        """, (price, title, year))

        # 2) Get the newly created Item_ID
        item_id = cursor.lastrowid

        # 3) Insert into Book table
        cursor.execute("""
            INSERT INTO Book (Item_ID, ISBN)
            VALUES (?, ?)
        """, (item_id, isbn))

        # 4) Insert into Publisher table if needed
        #   or link in Published_Product, etc.
        #   ... depends on how you handle references to Publisher, Authors, etc.

        # Similarly, handle authors if you want to store them in Creator + Created_Product
        # This part is trickier since you have multiple authors on some rows.
        # You'd parse them, check if Creator already exists, insert if not, then
        # insert into Created_Product to link the product with that creator.

conn.commit()
conn.close()
