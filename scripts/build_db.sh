

# Delete old DB if it exists
[ -f 3241.db ] && rm 3241.db

# Create a new DB by running our SQL scripts
# SCRIPTS GO HERE TO BUILD DB
sqlite3 3241.db < ../sql/schema.sql
sqlite3 3241.db < 

echo "Tht data is BUILT."