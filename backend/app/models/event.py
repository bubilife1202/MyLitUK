from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300), nullable=False, index=True)
    name_ko = Column(String(300))  # 한국어 이름
    type = Column(String(50))  # 'festival', 'reading', 'discussion', 'workshop'
    is_annual = Column(Boolean, default=False)
    description = Column(Text)
    description_ko = Column(Text)
    venue = Column(String(300))
    venue_ko = Column(String(300))
    city = Column(String(100))
    region = Column(String(100))  # 'London', 'Manchester', 'Edinburgh'
    start_date = Column(Date)
    end_date = Column(Date)
    ticket_url = Column(String(500))
    ticket_open_date = Column(DateTime(timezone=True))
    website_url = Column(String(500))
    image_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    keywords = relationship("EventKeyword", back_populates="event", cascade="all, delete-orphan")
    followers = relationship("UserEventFollow", back_populates="event")

    def __repr__(self):
        return f"<Event {self.name}>"


class EventKeyword(Base):
    __tablename__ = "event_keywords"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"))
    keyword = Column(String(100), nullable=False)  # 'Poetry', 'Fiction', 'Crime'

    # Relationships
    event = relationship("Event", back_populates="keywords")

    def __repr__(self):
        return f"<EventKeyword {self.keyword}>"
