from sqlalchemy import Column, Integer, String, Text, Date, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    name_ko = Column(String(200))  # 한국어 이름
    bio = Column(Text)
    bio_ko = Column(Text)  # 한국어 소개
    birth_date = Column(Date)
    nationality = Column(String(100), default="UK")
    photo_url = Column(String(500))
    website_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    books = relationship("Book", back_populates="author")
    followers = relationship("UserAuthorFollow", back_populates="author")

    def __repr__(self):
        return f"<Author {self.name}>"
