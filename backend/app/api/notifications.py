from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import NotificationResponse, NotificationList, NotificationStats

router = APIRouter()

@router.get("", response_model=NotificationList)
async def list_notifications(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    unread_only: bool = Query(False),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user notifications"""
    query = db.query(Notification).filter(Notification.user_id == current_user.id)

    # Filter unread only
    if unread_only:
        query = query.filter(Notification.is_read == False)

    # Order by priority and date
    query = query.order_by(
        Notification.priority.desc(),
        Notification.created_at.desc()
    )

    total = query.count()
    notifications = query.offset((page - 1) * size).limit(size).all()

    # Get unread count
    unread_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()

    return {
        "items": notifications,
        "total": total,
        "unread_count": unread_count,
        "page": page,
        "size": size
    }

@router.get("/stats", response_model=NotificationStats)
async def get_notification_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get notification statistics"""
    # Total count
    total = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).count()

    # Unread count
    unread = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()

    # Today's count
    today = datetime.now().date()
    today_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        func.date(Notification.created_at) == today
    ).count()

    # This week's count
    week_ago = datetime.now() - timedelta(days=7)
    week_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.created_at >= week_ago
    ).count()

    return {
        "total": total,
        "unread": unread,
        "today": today_count,
        "this_week": week_count
    }

@router.get("/count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get unread notification count"""
    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).count()
    return {"count": count}

@router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark notification as read"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    if notification.is_read:
        raise HTTPException(status_code=400, detail="Notification already read")

    notification.is_read = True
    notification.read_at = datetime.now()
    db.commit()

    return {"message": "Notification marked as read"}

@router.post("/mark-all-read")
async def mark_all_as_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark all notifications as read"""
    db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == False
    ).update({
        "is_read": True,
        "read_at": datetime.now()
    })
    db.commit()

    return {"message": "All notifications marked as read"}

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a notification"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()

    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")

    db.delete(notification)
    db.commit()

    return None
