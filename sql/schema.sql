CREATE TABLE if Not EXISTS "Book" (
	"Item_ID"	INTEGER NOT NULL,
	"ISBN"	CHAR(10) NOT NULL,
	PRIMARY KEY("Item_ID"),
	FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID")
);

CREATE TABLE if Not EXISTS "Created_Product" (
	"Item_ID"	INTEGER NOT NULL,
	"Creator_ID" INTEGER NOT NULL
	PRIMARY KEY("Item_ID","Creator_ID"),
	FOREIGN KEY("Creator_ID") REFERENCES "Creator"("Creator_ID"),
	FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID"),
);

CREATE TABLE if Not EXISTS "Creator" (
	"Creator_ID" INTEGER NOT NULL,
	"Name" VARCHAR(30), NOT NULL,
	"DOB"	DATE,
	PRIMARY KEY("Creator_ID")
);

CREATE TABLE if Not EXISTS "Customer" (
	"Customer_ID"	INTEGER NOT NULL,
	"Name"	VARCHAR(30) NOT NULL,
	"Address"	VARCHAR(40),
	PRIMARY KEY("Customer_ID")
);

CREATE TABLE if Not EXISTS "Order" (
	"Order_ID"	INTEGER NOT NULL,
	"Delivery_Status"	VARCHAR(10) NOT NULL,
	"Payment_Info"	VARCHAR(20) NOT NULL,
	"Date_of_Purchase"	DATE NOT NULL,
	"Customer_ID"	INTEGER NOT NULL,
	PRIMARY KEY("Order_ID"),
	FOREIGN KEY("Customer_ID") REFERENCES "Customer"("Customer_ID")
);

CREATE TABLE if Not EXISTS "Ordered_Product" (
	"Order_ID"	INTEGER NOT NULL,
	"Item_ID"	INTEGER NOT NULL,
	PRIMARY KEY("Order_ID","Item_ID"),
	FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID"),
	FOREIGN KEY("Order_ID") REFERENCES "Order"("Order_ID")
);

CREATE TABLE if Not EXISTS "Product" (
	"Item_ID"	INTEGER NOT NULL,
	"Price"	DECIMAL(5, 2) NOT NULL,
	"Quantity"	INTEGER NOT NULL,
	"Title"	VARCHAR(50) NOT NULL,
	"Year_Published"	INTEGER,
	PRIMARY KEY("Item_ID")
);
CREATE TABLE if Not EXISTS "Product_Genre" (
	"Item_ID"	INTEGER NOT NULL,
	"Genre"	VARCHAR(15) NOT NULL,
	PRIMARY KEY("Item_ID","Genre"),
	FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID")
);

CREATE TABLE if Not EXISTS "Published_Product" (
	"Item_ID"	INTEGER NOT NULL,
	"Publisher_ID"	INTEGER NOT NULL,
	PRIMARY KEY("Item_ID","Publisher_ID"),
	FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID"),
	FOREIGN KEY("Publisher_ID") REFERENCES "Publisher"("Publisher_ID")
);

CREATE TABLE if Not EXISTS "Publisher" (
	"Publisher_ID"	INTEGER NOT NULL,
	"Name" VARCHAR(30) NOT NULL,
	"Address"	VARCHAR(30),
	PRIMARY KEY("Publisher_ID")
);

CREATE TABLE if Not EXISTS "Record" (
	"Item_ID"	INTEGER NOT NULL,
	"Catalog#"	INTEGER,
	PRIMARY KEY("Item_ID"),
	FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID")
);


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

CREATE TABLE if Not EXISTS "Song" (
    "Song_ID"   INTEGER NOT NULL,
    "Name"      VARCHAR(30) NOT NULL,
    PRIMARY KEY("Song_ID")
);

CREATE TABLE if Not EXISTS "Songs_On_Records" (
"Item_ID" INTEGER   NOT NULL,
"Song_ID"   INTEGER NOT NULL,
PRIMARY KEY("Item_ID", "Song_ID")
FOREIGN KEY("Song_ID") REFERENCES "Song"("Song_ID")
FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID")
);