# Database Migration Guide

## Creating the Initial Migration

To create the initial database migration, follow these steps:

1. **Install dependencies** (if not already installed):
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Ensure PostgreSQL is running** and the database exists:
   ```bash
   createdb mylituk
   # Or connect to PostgreSQL and create the database:
   # psql -U postgres
   # CREATE DATABASE mylituk;
   ```

3. **Create the initial migration**:
   ```bash
   cd backend
   alembic revision --autogenerate -m "Initial migration with all models"
   ```

4. **Review the generated migration** in `alembic/versions/`. Make sure it includes all 14 tables:
   - users
   - authors
   - books
   - events
   - event_keywords
   - literary_awards
   - award_announcements
   - award_nominees
   - user_author_follows
   - user_event_follows
   - user_award_follows
   - user_event_alert_preferences
   - notifications
   - user_visit_streaks

5. **Apply the migration**:
   ```bash
   alembic upgrade head
   ```

## Production Deployment

When deploying to production (Render.com backend + Supabase database):

1. Set the `DATABASE_URL` environment variable in Render.com to your Supabase PostgreSQL URL
2. Run migrations as part of the build command or as a release command:
   ```bash
   alembic upgrade head
   ```

## Future Migrations

To create new migrations after modifying models:

```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## Rollback

To rollback the last migration:

```bash
alembic downgrade -1
```

To rollback all migrations:

```bash
alembic downgrade base
```
