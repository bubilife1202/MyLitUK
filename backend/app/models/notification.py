from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, ForeignKey, func, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    type = Column(String(50), nullable=False)  # 'new_book', 'event_ticket', 'award_longlist'
    title = Column(String(300), nullable=False)
    message = Column(Text, nullable=False)
    related_id = Column(Integer)  # book_id, event_id, announcement_id
    related_type = Column(String(50))  # 'book', 'event', 'award'
    action_url = Column(String(500))  # 구매/티켓 링크
    priority = Column(String(20), default='medium')  # 'high', 'medium', 'low'
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")

    # Indexes
    __table_args__ = (
        Index('idx_user_unread', 'user_id', 'is_read', 'created_at'),
    )

    def __repr__(self):
        return f"<Notification {self.type} for user {self.user_id}>"


class UserVisitStreak(Base):
    __tablename__ = "user_visit_streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    visit_date = Column(Date, nullable=False)
    streak_count = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")

    # Unique constraint
    __table_args__ = (
        UniqueConstraint('user_id', 'visit_date', name='unique_user_visit_date'),
    )
