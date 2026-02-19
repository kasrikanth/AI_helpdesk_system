from app.utils.config import SessionLocal
from app.models.database import Role, User
from app.utils.jwt_security import hash_password
import uuid

def seed():

    db = SessionLocal()

    # Create roles
    roles_data = [
        {"name": "super_admin", "level": 100},
        {"name": "admin", "level": 80},
        {"name": "support_engineer", "level": 60},
        {"name": "operator", "level": 40},
        {"name": "trainee", "level": 20},
        {"name": "instructor", "level": 30},
    ]

    for r in roles_data:
        if not db.query(Role).filter(Role.name == r["name"]).first():
            db.add(Role(name=r["name"], level=r["level"]))

    db.commit()

    # Create first super admin
    super_role = db.query(Role).filter(Role.name == "super_admin").first()

    if not db.query(User).filter(User.email == "superadmin_email").first():
        user = User(
            id=uuid.uuid4(),
            email="superadmin_email",
            full_name="Super Admin",
            password_hash=hash_password("password"),
            role_id=super_role.id
        )
        db.add(user)
        db.commit()

    print("✅ Roles and Super Admin created")

if __name__ == "__main__":
    seed()
