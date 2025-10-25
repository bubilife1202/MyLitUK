"""간단한 사용자 추가 (직접 bcrypt 사용)"""
import bcrypt
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User

db = SessionLocal()

try:
    # 기존 사용자 확인
    existing = db.query(User).filter(User.email == "demo@mylituk.com").first()
    if existing:
        print("✅ 테스트 사용자가 이미 존재합니다!")
        print("\n📧 이메일: demo@mylituk.com")
        print("🔑 비밀번호: demo1234")
    else:
        # 비밀번호 해싱 (직접 bcrypt 사용)
        password = "demo1234"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # 새 사용자 생성
        demo_user = User(
            email="demo@mylituk.com",
            username="demo",
            full_name="Demo User",
            password_hash=hashed.decode('utf-8'),
            preferred_language="ko"
        )
        db.add(demo_user)
        db.commit()
        print("✅ 테스트 사용자 추가 완료!")
        print("\n📧 이메일: demo@mylituk.com")
        print("🔑 비밀번호: demo1234")

except Exception as e:
    print(f"오류: {e}")
    import traceback
    traceback.print_exc()
    db.rollback()
finally:
    db.close()
