from sqlalchemy import Column, Integer, String, Text, Float, Date, DateTime, Boolean, ForeignKey, func, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.core.database import Base


class UserBookList(Base):
    """사용자의 독서 리스트 (읽고 싶은 책, 읽는 중, 완독)"""
    __tablename__ = "user_book_lists"
    __table_args__ = (
        UniqueConstraint('user_id', 'book_id', name='unique_user_book'),
        Index('idx_user_status', 'user_id', 'status'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(20), nullable=False, default='want_to_read')  # 'want_to_read', 'reading', 'finished'
    rating = Column(Float)  # 0.0 ~ 5.0
    started_date = Column(Date)
    finished_date = Column(Date)
    current_page = Column(Integer)
    total_pages = Column(Integer)
    notes = Column(Text)  # 개인 메모
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User")
    book = relationship("Book")

    def __repr__(self):
        return f"<UserBookList user={self.user_id} book={self.book_id} status={self.status}>"


class BookReview(Base):
    """책 리뷰 및 평점"""
    __tablename__ = "book_reviews"
    __table_args__ = (
        UniqueConstraint('user_id', 'book_id', name='unique_user_book_review'),
        Index('idx_book_created', 'book_id', 'created_at'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Float, nullable=False)  # 0.0 ~ 5.0
    title = Column(String(200))
    content = Column(Text)
    spoiler = Column(Boolean, default=False)
    likes_count = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)  # 공개/비공개
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User")
    book = relationship("Book")
    likes = relationship("ReviewLike", back_populates="review", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<BookReview user={self.user_id} book={self.book_id} rating={self.rating}>"


class ReviewLike(Base):
    """리뷰 좋아요"""
    __tablename__ = "review_likes"
    __table_args__ = (UniqueConstraint('user_id', 'review_id', name='unique_user_review_like'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    review_id = Column(Integer, ForeignKey("book_reviews.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")
    review = relationship("BookReview", back_populates="likes")


class ReadingChallenge(Base):
    """연간 독서 챌린지"""
    __tablename__ = "reading_challenges"
    __table_args__ = (UniqueConstraint('user_id', 'year', name='unique_user_year_challenge'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    year = Column(Integer, nullable=False)
    goal_count = Column(Integer, nullable=False)  # 목표 권수
    current_count = Column(Integer, default=0)  # 현재 읽은 권수
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User")

    def __repr__(self):
        return f"<ReadingChallenge user={self.user_id} year={self.year} {self.current_count}/{self.goal_count}>"


class UserActivity(Base):
    """사용자 활동 피드 (팔로우한 사람들의 활동 추적)"""
    __tablename__ = "user_activities"
    __table_args__ = (Index('idx_user_created', 'user_id', 'created_at'),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    activity_type = Column(String(50), nullable=False)  # 'finished_book', 'added_review', 'followed_author', 'added_to_list'
    related_id = Column(Integer)  # book_id, review_id, author_id
    related_type = Column(String(50))  # 'book', 'review', 'author'
    visibility = Column(String(20), default='public')  # 'public', 'followers_only', 'private'
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User")

    def __repr__(self):
        return f"<UserActivity user={self.user_id} type={self.activity_type}>"


class UserFollow(Base):
    """사용자 간 팔로우 (다른 유저 팔로우)"""
    __tablename__ = "user_follows"
    __table_args__ = (UniqueConstraint('follower_id', 'following_id', name='unique_user_follow'),)

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # 팔로우하는 사람
    following_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # 팔로우 당하는 사람
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<UserFollow {self.follower_id} -> {self.following_id}>"
