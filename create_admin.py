from cms_app import create_app, db
from cms_app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    username = input("Admin username: ")
    email = input("Admin email: ")
    password = input("Admin password: ")

    admin_user = User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        is_admin=True
    )
    db.session.add(admin_user)
    db.session.commit()
    print("Admin user created successfully.")
