# **Bits & Books Online Bookstore Project**  
*CSE 3241 Database*


## **Introduction**
This repository contains the final project code for our CSE 3241 class. We developed a relational database system to manage the inventory and sales operations for an online bookstore called Bits & Books. The project includes a final report, a complete SQL database with all necessary scripts, and data files to create the database based off of the schema we designed.

## **Submission File Directory Map**


      Final_Project                                     # Submitted Folder to Canvas 
      ├── Checkpoints                                   # Folder that holds all of the submitted checkpoints
      │   ├── Checkpoint3                               # Folder that holds all of the files submitted in Checkpoint 3
      │   │   ├── TableCreationCode 
      │   │   ├── test3241                               # database files for Checkpoint 3 
      │   │   ├── WorksheetTwoAdvancedQueries
      │   │   ├── WorksheetTwoExtraQueries 
      │   │   └── WorksheetTwoSimpleQueries
      │   ├── Checkpoint1 
      │   ├── Checkpoint2
      │   └── Checkpoint4
      ├── SQL_Database_Files                             # All of the files relating to Part II - The SQL Database from the Project Overview document 
      │   ├── data                                       # Holds all of the csv files needed for parse_csv.py to work properly 
      │   │   ├── customer_data 
      │   │   ├── data
      │   │   ├── order_data 
      │   │   ├── ordered_product_data
      │   │   ├── proj_data 
      │   │   ├── record_data 
      │   │   ├── review_data 
      │   │   ├── song_data 
      │   │   ├── songs_on_albums_data 
      │   │   ├── final_version3241                      # Completed database file 
      │   │   ├── parse_csv                              # Python file to create a new .db file if needed 
      │   │   ├── README                                 # Instructions on how to use the parse_csv file 
      │   │   ├── SQL_Insert_Delete 
      │   │   └──  SQL_Queries 
      ├── CheckpointRevisions 
      ├── DatabaseDescription
      ├── README 
      └──  UserManual


## **Repository Structure**
Below is an outline of the repository’s file structure:


    ├── data/                                           # Files containing the data to be loaded into the database
    │   ├── customer_data.csv
    │   ├── data.csv
    │   ├── order_data.csv
    │   ├── ordered_product_data.csv
    │   ├── proj_data.csv
    │   ├── record_data.csv
    │   ├── review_data.csv
    ├── scripts/                                      # Scripts which load the data files into the database
    │   ├── build_db.sh
    ├── sql/                                          # Includes the schema for the Bits & Books database
    │   ├── schema.sql
    ├── .DS_Store
    ├── .gitignore
    ├── README.md              
    ├── import_csv.py
    └── parse_csv.py   

## **Project Details**
Instead of having one large file that encompasses all three sections of the Final Report, we decided to break them down into smaller, more readable portions. The three files that make up the entirety of the Final Report, are 
*  "DatabaseDescription" (Section 1 of the Final Report)
*  "UserManual" (Section 2 of the Final Report)
*  "CheckpointRevisions" (Section 3)

All of the files relating to the SQL Database can be found in the "SQL_Database_Files" folder. Inside that folder you will find the final .db database as well as a python file that can be executed to create a new .db file in case the submitted one was corrupted. The "data" sub folder is used by the parse_csv.py file in order to properly populate all of the tables for the database. There is also a README.txt file that instructs you on how to execute the python file. You will also find the text file "SQL_Insert_Delete" which house example sql insert/delete statements that were provided within the UserManual. The "SQL_Queries" text file holds all of the SQL queries from the checkpoints.  
A final report was professionally presented with two main parts:

- **Database Description:**  
  Includes:
  - An ER diagram that visually represents the database design.
  - A detailed, annotated relational schema with primary keys, foreign keys, and noted functional dependencies.
  - An analysis of normalization for each table.
  - Explanations and rationales for the chosen indexes.
  - Descriptions of views along with their relational algebra, SQL code, and sample outputs.
  - A discussion and examples of three sample transactions.

- **User Manual:**  
  Includes:
  - Explanations of the real-world entities represented by each table.
  - Detailed descriptions of table attributes (data types and constraints).
  - Sample SQL queries with their English descriptions and relational algebra representations.
  - INSERT and DELETE syntax along with dependency instructions for correctly adding or removing records.

  - **CheckpointRevisions:**
   Includes:
   -  Revised checkpoint documents which were assigned throughout the semester.

## **Team Members**
- **Dillon Brigode** 
- **Alex Fizer** 
- **Aidan Whitlach**
- **Levi Keck** 

