from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class UserAuthorFollow(Base):
    __tablename__ = "user_author_follows"
    __table_args__ = (UniqueConstraint('user_id', 'author_id', name='unique_user_author'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    author = relationship("Author", back_populates="followers")


class UserEventFollow(Base):
    __tablename__ = "user_event_follows"
    __table_args__ = (UniqueConstraint('user_id', 'event_id', name='unique_user_event'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    notify_on_ticket_open = Column(Boolean, default=True)
    notify_on_program_update = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    event = relationship("Event", back_populates="followers")


class UserAwardFollow(Base):
    __tablename__ = "user_award_follows"
    __table_args__ = (UniqueConstraint('user_id', 'award_id', name='unique_user_award'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    award_id = Column(Integer, ForeignKey("literary_awards.id", ondelete="CASCADE"))
    notify_longlist = Column(Boolean, default=True)
    notify_shortlist = Column(Boolean, default=True)
    notify_winner = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    award = relationship("LiteraryAward", back_populates="followers")


class UserEventAlertPreference(Base):
    __tablename__ = "user_event_alert_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    region = Column(String(100))  # 'London', 'Manchester'
    keywords = Column(Text)  # JSON array stored as text: '["Poetry", "Fiction"]'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
