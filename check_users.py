from database import SessionLocal, User

# Create a new session
db = SessionLocal()

# Count the number of users
user_count = db.query(User).count()

# Print the count
print(f"Total number of users: {user_count}")

# Optionally, print user details
users = db.query(User).all()
for user in users:
    print(f"ID: {user.id}, First Name: {user.first_name}, Last Name: {user.last_name}, Email: {user.email}, Phone Number: {user.phone_number}")

# Close the session
db.close()
