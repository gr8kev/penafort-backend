from database import SessionLocal, User

# Create a new session
db = SessionLocal()

# Query all users
users = db.query(User).all()

# Print user details
for user in users:
    print(f"ID: {user.id}, First Name: {user.first_name}, Last Name: {user.last_name}, Email: {user.email}, Phone Number: {user.phone_number}")

db.close()
