import sqlite3
import pandas as pd

# 1. Load CSV with pandas
df = pd.read_csv('./Proj Data CSV.csv')

# 2. Connect to SQLite (creates university.db if it doesn't exist)
conn = sqlite3.connect('3241.db')
cursor = conn.cursor()


# 3. Write the DataFrame to the table
df.to_sql('students', conn, if_exists='append', index=False)

# 4. Clean up
conn.commit()
conn.close()
