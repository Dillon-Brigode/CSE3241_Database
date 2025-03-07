CREATE TABLE if Not EXISTS "Book" (
	"Item_ID"	INTEGER NOT NULL,
	"ISBN"	CHAR(10) NOT NULL,
	PRIMARY KEY("Item_ID"),
	FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID")
);

CREATE TABLE if Not EXISTS "Created_Product" (
	"Item_ID"	INTEGER NOT NULL,
	"FirstName"	VARCHAR(10) NOT NULL,
	"MiddleName"	VARCHAR(10) NOT NULL,
	"LastName"	VARCHAR(10) NOT NULL,
	PRIMARY KEY("Item_ID","FirstName","MiddleName","LastName"),
	FOREIGN KEY("FirstName") REFERENCES "Creator"("FirstName"),
	FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID"),
	FOREIGN KEY("LastName") REFERENCES "Creator"("LastName"),
	FOREIGN KEY("MiddleName") REFERENCES "Creator"("MiddleName")
);

CREATE TABLE if Not EXISTS "Creator" (
	"FirstName"	VARCHAR(10) NOT NULL,
	"MiddleName"	VARCHAR(10) NOT NULL,
	"LastName"	VARCHAR(10) NOT NULL,
	"DOB"	DATE NOT NULL,
	PRIMARY KEY("FirstName","MiddleName","LastName")
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
	"CustomerID"	INTEGER NOT NULL,
	PRIMARY KEY("Order_ID"),
	FOREIGN KEY("CustomerID") REFERENCES "Customer"("Customer_ID")
);

CREATE TABLE if Not EXISTS "Orderded_Product" (
	"Order_ID"	INTEGER NOT NULL,
	"CustomerID"	INTEGER NOT NULL,
	PRIMARY KEY("Order_ID","CustomerID"),
	FOREIGN KEY("CustomerID") REFERENCES "Customer"("Customer_ID"),
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
	"Published_ID"	INTEGER NOT NULL,
	PRIMARY KEY("Item_ID","Published_ID"),
	FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID"),
	FOREIGN KEY("Published_ID") REFERENCES "Publisher"("PublisherID")
);

CREATE TABLE if Not EXISTS "Publisher" (
	"PublisherID"	INTEGER NOT NULL,
	"Address"	VARCHAR(30),
	PRIMARY KEY("PublisherID")
);

CREATE TABLE if Not EXISTS "Record" (
	"Record_ID"	INTEGER NOT NULL,
	"TrackList"	VARCHAR(100) NOT NULL,
	"Catalog#"	INTEGER NOT NULL,
	PRIMARY KEY("Record_ID"),
	FOREIGN KEY("Record_ID") REFERENCES "Product"("Item_ID")
);


CREATE TABLE if Not EXISTS "Review" (
	"ReviewID"	INTEGER NOT NULL,
	"Text"	VARCHAR(100),
	"Score"	INTEGER NOT NULL CHECK(Score >= 0 and Score <= 10),
	"Customer_ID"	INTEGER NOT NULL,
	"Item_ID"	INTEGER NOT NULL,
	PRIMARY KEY("ReviewID"),
	FOREIGN KEY("Customer_ID") REFERENCES "Customer"("Customer_ID"),
	FOREIGN KEY("Item_ID") REFERENCES "Product"("Item_ID")
);