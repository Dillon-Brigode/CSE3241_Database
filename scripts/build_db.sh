

# Delete old DB if it exists
[ -f 3241.db ] && rm 3241.db

# Create a new DB by running our SQL scripts
# SCRIPTS GO HERE TO BUILD DB
sqlite3 3241.db < ../sql/schema.sql

#creates a new table in data base with just the data
sqlite3 3241.db <<EOF
.mode csv
.import ../data/data.csv data
EOF

echo "Tht data is BUILT."