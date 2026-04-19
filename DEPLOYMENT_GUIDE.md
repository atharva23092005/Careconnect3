# 🚀 CareConnect Production Deployment Guide

## ✅ Pre-Deployment Checklist

Before deploying, complete these steps locally:

### Step 1: Train the ML Model
```cmd
python train_model.py
```
This creates `model.pkl` (~50KB) which will be committed to your repo.

### Step 2: Initialize Database Migrations
```cmd
python init_db.py
```
This creates the `migrations/` folder with your database schema.

### Step 3: Test Locally with SQLite
```cmd
python app_production.py
```
Open http://127.0.0.1:5000 and test:
- Registration
- Login
- Health input
- Dashboard

### Step 4: Generate Secret Key
```cmd
python -c "import secrets; print(secrets.token_hex(32))"
```
Save this key for deployment configuration.

### Step 5: Commit Everything
```cmd
git add .
git commit -m "Production-ready with PostgreSQL and security fixes"
git push origin main
```

---

## 🌐 Deploy to Render (Recommended)

### 1. Create Account
Sign up at [render.com](https://render.com)

### 2. Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Name: `careconnect-db`
3. Database: `careconnect`
4. User: `careconnect`
5. Region: Choose closest to your users
6. Plan: **Free** (for testing) or **Starter** (for production)
7. Click "Create Database"
8. **Copy the Internal Database URL** (starts with `postgresql://`)

### 3. Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name:** `careconnect`
   - **Environment:** `Python 3`
   - **Region:** Same as database
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `flask db upgrade && gunicorn app_production:app`
   - **Plan:** Free (for testing) or Starter ($7/month for production)

### 4. Add Environment Variables
In the "Environment" section, add:

```
SECRET_KEY=<paste-your-generated-secret-key>
FLASK_ENV=production
DATABASE_URL=<paste-internal-database-url-from-step-2>
PYTHON_VERSION=3.10.12
```

### 5. Deploy!
Click "Create Web Service" and wait 3-5 minutes for deployment.

### 6. Access Your App
Your app will be available at: `https://careconnect.onrender.com`

### 7. Change Admin Password
1. Log in with `admin` / `admin123`
2. Immediately change the password (or create a new admin user)

---

## 🔧 Alternative: Deploy to Railway

### 1. Create Account
Sign up at [railway.app](https://railway.app)

### 2. Create New Project
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository

### 3. Add PostgreSQL
1. Click "New" → "Database" → "Add PostgreSQL"
2. Railway automatically creates `DATABASE_URL` variable

### 4. Configure Environment Variables
Add these variables:
```
SECRET_KEY=<your-secret-key>
FLASK_ENV=production
```

### 5. Configure Start Command
In Settings → Deploy:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `flask db upgrade && gunicorn app_production:app`

### 6. Deploy
Railway automatically deploys. Click "Generate Domain" to get your URL.

---

## 🧪 Testing Your Deployment

### 1. Health Check
Visit: `https://your-app.com/health`

Should return:
```json
{
  "status": "healthy",
  "database": "healthy",
  "ml_model": "healthy",
  "timestamp": "2024-01-01T00:00:00"
}
```

### 2. Test Registration
1. Go to `/register`
2. Create a new account
3. Verify you can log in

### 3. Test Health Input
1. Log in
2. Go to "Health Input"
3. Submit a health record
4. Check dashboard for results

### 4. Test Data Persistence
1. Submit a health record
2. Log out
3. Log back in
4. Verify the record is still there

---

## 🔒 Post-Deployment Security

### 1. Change Admin Password
```sql
-- Connect to your database and run:
UPDATE users SET password_hash = '<new-hashed-password>' WHERE username = 'admin';
```

Or create a new admin user and delete the default one.

### 2. Enable HTTPS
Both Render and Railway provide free SSL certificates automatically.

### 3. Monitor Your App
- Set up uptime monitoring (UptimeRobot, Pingdom)
- Check logs regularly in Render/Railway dashboard
- Monitor the `/health` endpoint

### 4. Backup Database
- Render: Automatic backups on paid plans
- Railway: Use `pg_dump` for manual backups

---

## 📊 Database Management

### View Database (Render)
1. Go to your PostgreSQL database in Render
2. Click "Connect" → "External Connection"
3. Use provided credentials with a tool like pgAdmin or DBeaver

### Run Migrations
If you update models:
```cmd
# Locally
flask db migrate -m "Description of changes"
flask db upgrade

# Commit and push
git add migrations/
git commit -m "Add new migration"
git push

# Render will automatically run migrations on deploy
```

### Reset Database (if needed)
```cmd
# In Render shell or Railway
flask db downgrade base
flask db upgrade
```

---

## 🐛 Troubleshooting

### Issue: "Model not found"
**Solution:** Make sure `model.pkl` is committed to git:
```cmd
git add model.pkl
git commit -m "Add trained model"
git push
```

### Issue: "Database connection failed"
**Solution:** Check `DATABASE_URL` environment variable is set correctly.

### Issue: "Internal Server Error"
**Solution:** Check logs in Render/Railway dashboard for details.

### Issue: "Rate limit errors"
**Solution:** Add Redis for better rate limiting:
1. Add Redis database in Render/Railway
2. Set `REDIS_URL` environment variable

---

## 📈 Scaling Considerations

### Free Tier Limitations
- Render Free: Spins down after 15 min of inactivity (cold starts)
- Railway Free: $5 credit/month
- Database: Limited storage and connections

### Upgrade to Paid Plans When:
- You have >100 active users
- You need 99.9% uptime
- You need faster response times
- You need more database storage

### Performance Optimization
1. Add Redis for caching
2. Use CDN for static files
3. Enable database connection pooling
4. Add database indexes for common queries

---

## 🎉 You're Done!

Your CareConnect app is now production-ready with:
- ✅ PostgreSQL database (persistent data)
- ✅ Password hashing (secure authentication)
- ✅ Rate limiting (DDoS protection)
- ✅ CSRF protection (security)
- ✅ Pre-trained ML model (fast predictions)
- ✅ Error handling (graceful failures)
- ✅ Health check endpoint (monitoring)

**Live URL:** `https://your-app.onrender.com` or `https://your-app.up.railway.app`

---

## 📞 Need Help?

If you encounter issues:
1. Check the logs in Render/Railway dashboard
2. Test locally first with `python app_production.py`
3. Verify all environment variables are set
4. Check the `/health` endpoint

Good luck with your deployment! 🚀
