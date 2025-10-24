# MyLitUK Deployment Guide

Complete deployment guide for the MyLitUK platform using 100% free hosting services.

## Architecture Overview

- **Frontend**: Vercel (Free tier)
- **Backend**: Render.com (Free tier)
- **Database**: Supabase PostgreSQL (Free tier - 500MB)
- **Monitoring**: UptimeRobot (to prevent Render sleep)

## Prerequisites

Before deploying, you need:

1. GitHub account (for code hosting)
2. Vercel account (free)
3. Render.com account (free)
4. Supabase account (free)

## Step 1: Deploy Database (Supabase)

1. **Create Supabase Project**:
   - Go to [supabase.com](https://supabase.com)
   - Click "Start your project"
   - Create a new organization (if needed)
   - Create a new project
   - Choose a region close to your users
   - Set a strong database password (save this!)

2. **Get Database Connection String**:
   - Go to Project Settings → Database
   - Find "Connection string" section
   - Copy the URI connection string
   - Replace `[YOUR-PASSWORD]` with your actual password
   - Example: `postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`

3. **Database is now ready!** (No need to create tables manually - migrations will handle this)

## Step 2: Deploy Backend (Render.com)

1. **Create New Web Service**:
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `MyLitUK` repository

2. **Configure Service**:
   ```
   Name: mylituk-backend
   Region: Choose closest to your users
   Branch: main (or your feature branch)
   Root Directory: backend
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Set Environment Variables**:
   Click "Advanced" → "Add Environment Variable" and add:

   ```
   DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
   SECRET_KEY=[Generate using: openssl rand -hex 32]
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=10080
   ALLOWED_ORIGINS=https://[your-vercel-domain].vercel.app,https://mylituk.vercel.app
   ```

4. **Deploy**:
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment
   - Your backend URL will be: `https://mylituk-backend.onrender.com`

5. **Run Database Migrations**:
   After deployment, open Render Shell and run:
   ```bash
   cd backend
   alembic upgrade head
   ```

6. **Important - Free Tier Limitation**:
   Render free tier sleeps after 15 minutes of inactivity. Set up UptimeRobot to ping your API every 5 minutes:
   - Go to [uptimerobot.com](https://uptimerobot.com)
   - Add New Monitor
   - Type: HTTP(s)
   - URL: `https://mylituk-backend.onrender.com/health`
   - Monitoring Interval: 5 minutes

## Step 3: Deploy Frontend (Vercel)

1. **Deploy to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Select the repository

2. **Configure Project**:
   ```
   Framework Preset: Next.js
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```

3. **Set Environment Variables**:
   ```
   NEXT_PUBLIC_API_URL=https://mylituk-backend.onrender.com
   ```

4. **Deploy**:
   - Click "Deploy"
   - Wait 2-3 minutes
   - Your frontend URL will be: `https://mylituk.vercel.app` (or custom domain)

5. **Update Backend CORS**:
   Go back to Render.com → Your backend service → Environment
   - Update `ALLOWED_ORIGINS` to include your Vercel URL

## Step 4: Verification

1. **Test Backend API**:
   ```bash
   curl https://mylituk-backend.onrender.com/health
   ```
   Should return: `{"status":"healthy"}`

2. **Test Frontend**:
   - Open: `https://mylituk.vercel.app`
   - Should see the home page
   - Try registering a new account
   - Try logging in
   - Check the dashboard

3. **Test Multilingual**:
   - Visit: `https://mylituk.vercel.app/en` (English)
   - Visit: `https://mylituk.vercel.app/ko` (Korean)

## Step 5: Post-Deployment Configuration

### 1. Seed Initial Data

You'll need to add some initial data to make the platform useful:

**Authors**:
```python
# Create a script or use API to add UK authors
# Examples: Zadie Smith, Kazuo Ishiguro, Hilary Mantel, etc.
```

**Events**:
```python
# Add major UK literary festivals
# - Hay Festival
# - Edinburgh International Book Festival
# - Cheltenham Literature Festival
```

**Awards**:
```python
# Add major UK literary awards
# - Booker Prize
# - Women's Prize for Fiction
# - Costa Book Awards
```

### 2. Set Up Data Collection (Optional)

For automatic data updates, you can set up GitHub Actions to run web scraping scripts:

1. Create `.github/workflows/data-update.yml`
2. Configure to run daily
3. Scrape event and award websites
4. Update database via API

## Troubleshooting

### Backend Issues

**Problem**: Backend returns 500 errors
- **Solution**: Check Render logs: Dashboard → Your service → Logs
- Common cause: Database connection issues
- Verify `DATABASE_URL` is correct

**Problem**: Database migrations fail
- **Solution**: Check if Supabase database is accessible
- Try running migrations manually via Render Shell

**Problem**: Backend sleeps after 15 minutes
- **Solution**: Set up UptimeRobot to ping `/health` every 5 minutes
- Or upgrade to Render paid plan ($7/month)

### Frontend Issues

**Problem**: API calls fail (CORS errors)
- **Solution**: Add your Vercel domain to `ALLOWED_ORIGINS` in Render backend

**Problem**: 404 on page refresh
- **Solution**: Vercel should handle this automatically with Next.js
- Check vercel.json configuration

**Problem**: Language switching doesn't work
- **Solution**: Check middleware.ts is properly configured
- Verify locale files exist in `messages/en.json` and `messages/ko.json`

### Database Issues

**Problem**: Connection timeout
- **Solution**: Check Supabase project is active
- Verify connection string includes port :5432
- Check if IP is whitelisted (Supabase allows all by default)

**Problem**: "Too many connections"
- **Solution**: Free tier has connection limits
- Implement connection pooling
- Or upgrade to Supabase paid plan

## Monitoring

### Free Monitoring Tools

1. **Vercel Analytics** (built-in):
   - Go to Vercel Dashboard → Your project → Analytics
   - See page views, top pages, user countries

2. **Render Metrics** (built-in):
   - Go to Render Dashboard → Your service → Metrics
   - See CPU, memory, request counts

3. **Supabase Dashboard**:
   - See database size, query performance
   - Monitor connection count

4. **UptimeRobot**:
   - Monitor backend uptime
   - Get email alerts if backend goes down

## Scaling

### When You Need to Upgrade

**Free tier limits**:
- Vercel: 100GB bandwidth/month
- Render: Sleeps after 15 minutes inactivity, 750 hours/month
- Supabase: 500MB database, 2GB bandwidth

**Upgrade path**:
1. **Supabase Pro** ($25/month): 8GB database, better performance
2. **Render Starter** ($7/month): No sleep, always on
3. **Vercel Pro** ($20/month): More bandwidth, better analytics

### Cost Estimate for 5,000 Users

- Supabase Pro: $25/month (8GB database)
- Render Starter: $7/month (no sleep)
- Vercel Free: $0 (likely enough for 5,000 users)
- **Total**: ~$32/month

## Custom Domain (Optional)

### For Frontend (Vercel)

1. Go to Vercel Dashboard → Your project → Settings → Domains
2. Add your domain (e.g., `mylituk.com`)
3. Follow DNS configuration instructions
4. Update `ALLOWED_ORIGINS` in backend to include new domain

### For Backend (Render)

1. Render free tier doesn't support custom domains
2. Upgrade to Starter ($7/month) to use custom domains
3. Or use Render's provided domain: `mylituk-backend.onrender.com`

## Security Checklist

- [ ] Use strong database password (20+ characters)
- [ ] Generate secure SECRET_KEY (32 bytes minimum)
- [ ] Enable HTTPS (automatic on Vercel and Render)
- [ ] Restrict CORS to only your frontend domain
- [ ] Don't commit .env files to git
- [ ] Regularly update dependencies
- [ ] Monitor Render logs for suspicious activity

## Backup Strategy

### Database Backups (Supabase)

Free tier includes:
- Automatic daily backups (kept for 7 days)
- Point-in-time recovery

To manual backup:
```bash
pg_dump [CONNECTION_STRING] > backup.sql
```

### Code Backups

- Code is already in GitHub (version controlled)
- Tag releases: `git tag v1.0.0 && git push --tags`

## Next Steps

After successful deployment:

1. **Test thoroughly**: Register, login, follow authors/events/awards
2. **Add initial data**: Populate database with authors, events, awards
3. **Set up monitoring**: Configure UptimeRobot and check logs
4. **Plan content strategy**: How will you add new books, events, awards?
5. **Consider automation**: GitHub Actions for data scraping
6. **Plan scaling**: Monitor usage and upgrade when needed

## Support

- Vercel: [vercel.com/support](https://vercel.com/support)
- Render: [render.com/docs](https://render.com/docs)
- Supabase: [supabase.com/docs](https://supabase.com/docs)

## License

MIT
