"""간단한 사용자 추가 스크립트"""
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

try:
    # 기존 사용자 확인
    existing = db.query(User).filter(User.email == "demo@mylituk.com").first()
    if existing:
        print("✅ 테스트 사용자가 이미 존재합니다!")
    else:
        # 새 사용자 생성
        demo_user = User(
            email="demo@mylituk.com",
            username="demo",
            full_name="Demo User",
            password_hash=get_password_hash("demo1234"),
            preferred_language="ko"
        )
        db.add(demo_user)
        db.commit()
        print("✅ 테스트 사용자 추가 완료!")

    print("\n📧 이메일: demo@mylituk.com")
    print("🔑 비밀번호: demo1234")

except Exception as e:
    print(f"오류: {e}")
    db.rollback()
finally:
    db.close()
