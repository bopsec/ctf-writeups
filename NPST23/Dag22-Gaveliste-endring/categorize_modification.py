import sqlite3
import pandas as pd
import os

# Paths to the original and renamed database files
original_db_path = 'inventory_original.db'
renamed_db_path = 'inventory.db'

# Connect to the original database and fetch data
conn_original = sqlite3.connect(original_db_path)
df_original = pd.read_sql_query("SELECT * FROM gifts;", conn_original)
conn_original.close()

# Rename the original database file to trigger the merge
os.rename(original_db_path, renamed_db_path)

# Connect to the renamed database (now inventory.db) to trigger the merge
conn_renamed = sqlite3.connect(renamed_db_path)
df_renamed = pd.read_sql_query("SELECT * FROM gifts;", conn_renamed)
conn_renamed.close()

# Compare the original and renamed data to find changes
df_changes = pd.concat([df_original, df_renamed]).drop_duplicates(keep=False)

# Display the changes
print("Changes identified in the database:")
print(df_changes)

# Identify the entry with zero quantity in the merged data
zero_quantity_entry = df_renamed[df_renamed['quantity'] == 0]
print("\nEntry with zero quantity in the merged database:")
print(zero_quantity_entry)
