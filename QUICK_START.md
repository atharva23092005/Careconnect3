# ⚡ CareConnect - Quick Start Guide

## 🎯 Choose Your Path

### Path 1: Local Testing (5 minutes)
Just want to see it work locally?

```cmd
pip install -r requirements.txt
python train_model.py
python init_db.py
python app_production.py
```

Open http://127.0.0.1:5000

---

### Path 2: Deploy to Production (30 minutes)
Ready to deploy for real users?

#### Step 1: Setup (5 min)
```cmd
setup_production.cmd
```

#### Step 2: Commit (2 min)
```cmd
git add .
git commit -m "Production-ready deployment"
git push origin main
```

#### Step 3: Deploy to Render (20 min)
1. Go to [render.com](https://render.com)
2. Create PostgreSQL database
3. Create Web Service from your GitHub repo
4. Add environment variables:
   - `SECRET_KEY` (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `FLASK_ENV=production`
   - `DATABASE_URL` (from PostgreSQL database)
5. Deploy!

#### Step 4: Test (3 min)
Visit your app URL and test registration, login, and health input.

**Full details:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---

## 📋 What You Get

✅ Secure password hashing  
✅ PostgreSQL database (persistent data)  
✅ Rate limiting (DDoS protection)  
✅ CSRF protection  
✅ Pre-trained ML model  
✅ Health monitoring endpoint  
✅ Production-ready configuration  

---

## 🔑 Default Login

**Username:** admin  
**Password:** admin123

⚠️ Change this after first login!

---

## 📚 Documentation

- **[README_PRODUCTION.md](README_PRODUCTION.md)** - Overview of changes
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Detailed deployment steps
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - What was fixed

---

## 🆘 Need Help?

**Issue:** Model not found  
**Fix:** `python train_model.py`

**Issue:** Database errors  
**Fix:** `python init_db.py`

**Issue:** Import errors  
**Fix:** `pip install -r requirements.txt`

---

## 🚀 Ready? Let's Go!

```cmd
setup_production.cmd
```

That's it! Follow the prompts and you'll be production-ready in minutes.
