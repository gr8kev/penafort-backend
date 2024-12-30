import sqlite3


conn = sqlite3.connect('test.db')  
cursor = conn.cursor()


cursor.execute("SELECT COUNT(*) FROM users")
total_users = cursor.fetchone()[0]  
print(f"Total users in the database: {total_users}")


cursor.execute("DELETE FROM users")
conn.commit()  
print(f"All users have been deleted.")


conn.close()
