from database import SessionLocal, User


db = SessionLocal()


user_count = db.query(User).count()


print(f"Total number of users: {user_count}")


users = db.query(User).all()
for user in users:
    print(f"ID: {user.id}, First Name: {user.first_name}, Last Name: {user.last_name}, Email: {user.email}, Phone Number: {user.phone_number}")


db.close()
