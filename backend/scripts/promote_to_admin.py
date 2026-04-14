import argparse
import sys
from pathlib import Path

# Make sure `app` is importable when script is run from backend root.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.database import SessionLocal
from app.models.user import User, UserRole


def promote_user(email: str) -> int:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"User not found for email: {email}")
            print("Register this user first, then run this command again.")
            return 1

        if user.role == UserRole.admin:
            print(f"User {email} is already an admin.")
            return 0

        user.role = UserRole.admin
        db.commit()
        db.refresh(user)

        print(f"User {email} promoted to admin successfully.")
        return 0
    finally:
        db.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Promote an existing user to admin role")
    parser.add_argument("--email", required=True, help="Email of existing user to promote")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return promote_user(args.email)


if __name__ == "__main__":
    raise SystemExit(main())
