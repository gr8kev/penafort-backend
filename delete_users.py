import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('test.db')  # Replace with your actual database file
cursor = conn.cursor()

# 1. View the total number of users
cursor.execute("SELECT COUNT(*) FROM users")
total_users = cursor.fetchone()[0]  # Fetch the first column (count) from the result
print(f"Total users in the database: {total_users}")

# 2. Delete all users
cursor.execute("DELETE FROM users")
conn.commit()  # Commit the changes to the database
print(f"All users have been deleted.")

# Close the connection
conn.close()
