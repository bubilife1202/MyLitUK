from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class LiteraryAward(Base):
    __tablename__ = "literary_awards"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    name_ko = Column(String(200))  # 한국어 이름
    description = Column(Text)
    description_ko = Column(Text)
    category = Column(String(100))  # 'Fiction', 'Poetry', 'Non-fiction'
    annual_cycle = Column(Integer, default=1)
    website_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    announcements = relationship("AwardAnnouncement", back_populates="award")
    followers = relationship("UserAwardFollow", back_populates="award")

    def __repr__(self):
        return f"<LiteraryAward {self.name}>"


class AwardAnnouncement(Base):
    __tablename__ = "award_announcements"

    id = Column(Integer, primary_key=True, index=True)
    award_id = Column(Integer, ForeignKey("literary_awards.id"))
    year = Column(Integer, nullable=False)
    stage = Column(String(20), nullable=False)  # 'longlist', 'shortlist', 'winner'
    announcement_date = Column(DateTime(timezone=True))
    announced = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    award = relationship("LiteraryAward", back_populates="announcements")
    nominees = relationship("AwardNominee", back_populates="announcement")

    def __repr__(self):
        return f"<AwardAnnouncement {self.award_id} {self.year} {self.stage}>"


class AwardNominee(Base):
    __tablename__ = "award_nominees"

    id = Column(Integer, primary_key=True, index=True)
    announcement_id = Column(Integer, ForeignKey("award_announcements.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    is_winner = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    announcement = relationship("AwardAnnouncement", back_populates="nominees")
    book = relationship("Book")

    def __repr__(self):
        return f"<AwardNominee book_id={self.book_id}>"
