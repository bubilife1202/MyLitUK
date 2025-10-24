from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date
from app.core.database import get_db
from app.core.deps import get_current_user, get_current_user_optional
from app.models.event import Event
from app.models.user import User
from app.models.follows import UserEventFollow
from app.schemas.event import EventResponse, EventList

router = APIRouter()

@router.get("", response_model=EventList)
async def list_events(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    region: str = Query(None),
    event_type: str = Query(None),
    upcoming: bool = Query(True),
    current_user: User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """List events with filters"""
    query = db.query(Event)

    # Filter by search term
    if search:
        query = query.filter(
            or_(
                Event.name.ilike(f"%{search}%"),
                Event.name_ko.ilike(f"%{search}%") if Event.name_ko else False,
                Event.city.ilike(f"%{search}%")
            )
        )

    # Filter by region
    if region:
        query = query.filter(Event.region == region)

    # Filter by type
    if event_type:
        query = query.filter(Event.type == event_type)

    # Filter upcoming events
    if upcoming:
        today = date.today()
        query = query.filter(
            or_(
                Event.start_date >= today,
                Event.end_date >= today
            )
        )

    # Order by start date
    query = query.order_by(Event.start_date.asc())

    total = query.count()
    events = query.offset((page - 1) * size).limit(size).all()

    # Check if user follows each event
    if current_user:
        followed_event_ids = {f.event_id for f in db.query(UserEventFollow).filter(
            UserEventFollow.user_id == current_user.id
        ).all()}
        for event in events:
            event.is_followed = event.id in followed_event_ids

    return {
        "items": events,
        "total": total,
        "page": page,
        "size": size
    }

@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    current_user: User = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get event details"""
    event = db.query(Event).filter(Event.id == event_id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check if user follows this event
    if current_user:
        follow = db.query(UserEventFollow).filter(
            UserEventFollow.user_id == current_user.id,
            UserEventFollow.event_id == event_id
        ).first()
        event.is_followed = follow is not None

    return event

@router.post("/{event_id}/follow", status_code=status.HTTP_201_CREATED)
async def follow_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Follow an event"""
    # Check if event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Check if already following
    existing = db.query(UserEventFollow).filter(
        UserEventFollow.user_id == current_user.id,
        UserEventFollow.event_id == event_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already following this event")

    # Create follow
    follow = UserEventFollow(user_id=current_user.id, event_id=event_id)
    db.add(follow)
    db.commit()

    return {"message": "Successfully followed event", "event_id": event_id}

@router.delete("/{event_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_event(
    event_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Unfollow an event"""
    # Find follow relationship
    follow = db.query(UserEventFollow).filter(
        UserEventFollow.user_id == current_user.id,
        UserEventFollow.event_id == event_id
    ).first()

    if not follow:
        raise HTTPException(status_code=404, detail="Not following this event")

    # Delete follow
    db.delete(follow)
    db.commit()

    return None
