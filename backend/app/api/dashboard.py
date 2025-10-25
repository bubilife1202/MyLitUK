from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, func, desc, extract
from datetime import datetime, date, timedelta
from typing import List, Dict, Any
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.author import Author
from app.models.book import Book
from app.models.event import Event
from app.models.literary_award import LiteraryAward, AwardAnnouncement
from app.models.follows import UserAuthorFollow, UserEventFollow, UserAwardFollow
from app.models.notification import Notification
from app.models.reading import UserBookList, BookReview, ReadingChallenge

router = APIRouter()

@router.get("")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized dashboard feed - core feature!

    Returns ONLY content from followed authors, events, and awards.
    This creates a personalized, curated experience instead of overwhelming content.
    """

    # Get followed authors
    followed_author_ids = [f.author_id for f in db.query(UserAuthorFollow).filter(
        UserAuthorFollow.user_id == current_user.id
    ).all()]

    # Get followed events
    followed_event_ids = [f.event_id for f in db.query(UserEventFollow).filter(
        UserEventFollow.user_id == current_user.id
    ).all()]

    # Get followed awards
    followed_award_ids = [f.award_id for f in db.query(UserAwardFollow).filter(
        UserAwardFollow.user_id == current_user.id
    ).all()]

    # Get new books from followed authors (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    new_books = []
    if followed_author_ids:
        books = db.query(Book).filter(
            Book.author_id.in_(followed_author_ids),
            Book.created_at >= thirty_days_ago
        ).order_by(Book.publication_date.desc()).limit(10).all()

        for book in books:
            author = db.query(Author).filter(Author.id == book.author_id).first()
            new_books.append({
                "type": "new_book",
                "book_id": book.id,
                "title": book.title,
                "title_ko": book.title_ko,
                "author_name": author.name if author else None,
                "publication_date": book.publication_date.isoformat() if book.publication_date else None,
                "amazon_url": book.amazon_url,
                "created_at": book.created_at.isoformat()
            })

    # Get upcoming events from followed events
    today = date.today()
    upcoming_events = []
    if followed_event_ids:
        events = db.query(Event).filter(
            Event.id.in_(followed_event_ids),
            or_(Event.start_date >= today, Event.end_date >= today)
        ).order_by(Event.start_date.asc()).limit(10).all()

        for event in events:
            upcoming_events.append({
                "type": "upcoming_event",
                "event_id": event.id,
                "name": event.name,
                "name_ko": event.name_ko,
                "start_date": event.start_date.isoformat() if event.start_date else None,
                "end_date": event.end_date.isoformat() if event.end_date else None,
                "ticket_url": event.ticket_url,
                "ticket_open_date": event.ticket_open_date.isoformat() if event.ticket_open_date else None,
                "city": event.city,
                "region": event.region
            })

    # Get award announcements from followed awards (current year and upcoming)
    current_year = datetime.now().year
    award_updates = []
    if followed_award_ids:
        announcements = db.query(AwardAnnouncement).filter(
            AwardAnnouncement.award_id.in_(followed_award_ids),
            AwardAnnouncement.year >= current_year - 1
        ).order_by(AwardAnnouncement.announcement_date.desc()).limit(10).all()

        for announcement in announcements:
            award = db.query(LiteraryAward).filter(
                LiteraryAward.id == announcement.award_id
            ).first()
            award_updates.append({
                "type": "award_announcement",
                "award_id": award.id if award else None,
                "award_name": award.name if award else None,
                "award_name_ko": award.name_ko if award else None,
                "year": announcement.year,
                "stage": announcement.stage,
                "announcement_date": announcement.announcement_date.isoformat() if announcement.announcement_date else None,
                "announced": announcement.announced
            })

    # Get recent unread notifications
    recent_notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).order_by(Notification.created_at.desc()).limit(5).all()

    notifications_list = [{
        "id": n.id,
        "type": n.type,
        "title": n.title,
        "message": n.message,
        "priority": n.priority,
        "created_at": n.created_at.isoformat()
    } for n in recent_notifications]

    return {
        "summary": {
            "followed_authors": len(followed_author_ids),
            "followed_events": len(followed_event_ids),
            "followed_awards": len(followed_award_ids),
            "new_books_count": len(new_books),
            "upcoming_events_count": len(upcoming_events),
            "award_updates_count": len(award_updates),
            "unread_notifications": len(recent_notifications)
        },
        "new_books": new_books,
        "upcoming_events": upcoming_events,
        "award_updates": award_updates,
        "recent_notifications": notifications_list
    }

@router.get("/today")
async def get_today_updates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get today's updates from followed content"""
    today = datetime.now().date()

    # Get followed entities
    followed_author_ids = [f.author_id for f in db.query(UserAuthorFollow).filter(
        UserAuthorFollow.user_id == current_user.id
    ).all()]

    followed_event_ids = [f.event_id for f in db.query(UserEventFollow).filter(
        UserEventFollow.user_id == current_user.id
    ).all()]

    updates = []

    # New books added today from followed authors
    if followed_author_ids:
        books = db.query(Book).filter(
            Book.author_id.in_(followed_author_ids),
            func.date(Book.created_at) == today
        ).all()

        for book in books:
            updates.append({
                "type": "new_book",
                "content": f"New book: {book.title}",
                "created_at": book.created_at.isoformat()
            })

    # Events starting today from followed events
    if followed_event_ids:
        events = db.query(Event).filter(
            Event.id.in_(followed_event_ids),
            Event.start_date == today
        ).all()

        for event in events:
            updates.append({
                "type": "event_starting",
                "content": f"Event starting today: {event.name}",
                "event_id": event.id
            })

    # Today's notifications
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        func.date(Notification.created_at) == today
    ).all()

    for notif in notifications:
        updates.append({
            "type": "notification",
            "content": notif.title,
            "created_at": notif.created_at.isoformat()
        })

    return {
        "date": today.isoformat(),
        "count": len(updates),
        "updates": updates
    }

@router.get("/following")
async def get_following_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get summary of all followed authors, events, and awards"""

    # Get followed authors with details
    followed_authors = db.query(Author).join(UserAuthorFollow).filter(
        UserAuthorFollow.user_id == current_user.id
    ).all()

    # Get followed events with details
    followed_events = db.query(Event).join(UserEventFollow).filter(
        UserEventFollow.user_id == current_user.id
    ).all()

    # Get followed awards with details
    followed_awards = db.query(LiteraryAward).join(UserAwardFollow).filter(
        UserAwardFollow.user_id == current_user.id
    ).all()

    return {
        "authors": [{
            "id": a.id,
            "name": a.name,
            "name_ko": a.name_ko,
            "photo_url": a.photo_url
        } for a in followed_authors],
        "events": [{
            "id": e.id,
            "name": e.name,
            "name_ko": e.name_ko,
            "start_date": e.start_date.isoformat() if e.start_date else None
        } for e in followed_events],
        "awards": [{
            "id": aw.id,
            "name": aw.name,
            "name_ko": aw.name_ko
        } for aw in followed_awards]
    }


@router.get("/stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """개인화된 대시보드 통계"""

    # 독서 통계
    want_to_read = db.query(UserBookList).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.status == 'want_to_read'
    ).count()

    reading = db.query(UserBookList).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.status == 'reading'
    ).count()

    finished = db.query(UserBookList).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.status == 'finished'
    ).count()

    favorites = db.query(UserBookList).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.is_favorite == True
    ).count()

    # 리뷰 통계
    total_reviews = db.query(BookReview).filter(
        BookReview.user_id == current_user.id
    ).count()

    avg_rating = db.query(func.avg(BookReview.rating)).filter(
        BookReview.user_id == current_user.id
    ).scalar()

    total_likes_received = db.query(func.sum(BookReview.likes_count)).filter(
        BookReview.user_id == current_user.id
    ).scalar()

    # 팔로우 통계
    following_authors = db.query(UserAuthorFollow).filter(
        UserAuthorFollow.user_id == current_user.id
    ).count()

    following_events = db.query(UserEventFollow).filter(
        UserEventFollow.user_id == current_user.id
    ).count()

    following_awards = db.query(UserAwardFollow).filter(
        UserAwardFollow.user_id == current_user.id
    ).count()

    # 독서 챌린지 통계
    current_year = datetime.now().year
    challenge = db.query(ReadingChallenge).filter(
        ReadingChallenge.user_id == current_user.id,
        ReadingChallenge.year == current_year,
        ReadingChallenge.is_active == True
    ).first()

    challenge_stats = {}
    if challenge:
        challenge_stats = {
            "goal": challenge.goal_count,
            "current": challenge.current_count,
            "percentage": round((challenge.current_count / challenge.goal_count) * 100, 1) if challenge.goal_count > 0 else 0
        }

    # 알림 개수
    unread_notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()

    return {
        "reading_stats": {
            "want_to_read": want_to_read,
            "reading": reading,
            "finished": finished,
            "favorites": favorites,
            "total": want_to_read + reading + finished
        },
        "review_stats": {
            "total_reviews": total_reviews,
            "average_rating": round(float(avg_rating), 2) if avg_rating else 0.0,
            "total_likes_received": int(total_likes_received) if total_likes_received else 0
        },
        "follow_stats": {
            "authors": following_authors,
            "events": following_events,
            "awards": following_awards,
            "total": following_authors + following_events + following_awards
        },
        "challenge_stats": challenge_stats,
        "notification_count": unread_notifications
    }


@router.get("/reading-insights")
async def get_reading_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """독서 인사이트 (장르별, 월별 등)"""
    # 장르별 통계
    genre_stats = db.query(
        Book.genre,
        func.count(UserBookList.id).label('count')
    ).join(
        UserBookList, UserBookList.book_id == Book.id
    ).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.status == 'finished',
        Book.genre.isnot(None)
    ).group_by(Book.genre).all()

    # 월별 독서량 (올해)
    current_year = datetime.now().year
    monthly_stats = db.query(
        extract('month', UserBookList.finished_date).label('month'),
        func.count(UserBookList.id).label('count')
    ).filter(
        UserBookList.user_id == current_user.id,
        UserBookList.status == 'finished',
        UserBookList.finished_date.isnot(None),
        extract('year', UserBookList.finished_date) == current_year
    ).group_by('month').all()

    return {
        "genres": [{"genre": genre, "count": count} for genre, count in genre_stats],
        "monthly": [{"month": int(month), "count": count} for month, count in monthly_stats]
    }
