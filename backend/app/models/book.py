from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    title_ko = Column(String(500))  # 한국어 제목
    author_id = Column(Integer, ForeignKey("authors.id"))
    isbn = Column(String(13), unique=True)
    publication_date = Column(Date)
    publisher = Column(String(200))
    genre = Column(String(100))
    description = Column(Text)
    description_ko = Column(Text)  # 한국어 설명
    cover_image_url = Column(String(500))
    amazon_url = Column(String(500))
    waterstones_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    author = relationship("Author", back_populates="books")

    def __repr__(self):
        return f"<Book {self.title}>"
