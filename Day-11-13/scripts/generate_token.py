import sys
from pathlib import Path
# Ensure project root (Day-11-13) is on sys.path so `app` is importable
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()
from app.database.config import SessionLocal
from app.models.models import User
from app.auth.security import create_access_token

s = SessionLocal()
user = s.query(User).filter(User.email=='customer@ecommerce.com').first()
if not user:
    print('NO_USER_FOUND')
else:
    token = create_access_token({'sub': user.id, 'role': user.role})
    print(token)
