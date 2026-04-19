# 🚀 How to Run CareConnect - Simple Guide

## ⚡ Quick Start (Easiest Way)

### Step 1: Run the startup script
```cmd
start_app.cmd
```

That's it! The script will:
- Check if the ML model exists (train it if needed)
- Start the Flask application
- Show you the login credentials

### Step 2: Open your browser
Go to: **http://127.0.0.1:5000**

### Step 3: Login
- **Username:** admin
- **Password:** admin123

---

## 📋 Manual Setup (If script doesn't work)

### Step 1: Install dependencies
```cmd
pip install Flask Flask-SQLAlchemy Werkzeug pandas scikit-learn numpy openpyxl
```

### Step 2: Train the model (only needed once)
```cmd
python train_model.py
```

### Step 3: Run the app
```cmd
python app_fixed.py
```

### Step 4: Open browser
Go to: **http://127.0.0.1:5000**

---

## ✅ What Works Now

- ✅ **Login** - Simple session-based authentication
- ✅ **Register** - Create new user accounts
- ✅ **Dashboard** - View your health records
- ✅ **Health Input** - Log daily routine
- ✅ **Predictions** - ML-based risk assessment
- ✅ **Database** - SQLite (data persists)
- ✅ **Password Security** - Hashed passwords

---

## 🔧 Troubleshooting

### "No module named 'sklearn'"
```cmd
pip install scikit-learn pandas numpy openpyxl Flask Flask-SQLAlchemy Werkzeug
```

### "Model not found"
```cmd
python train_model.py
```

### "Port 5000 already in use"
Kill the existing process or change the port in `app_fixed.py` (last line)

### Login not working
Make sure you're using:
- Username: `admin`
- Password: `admin123`

If still not working, delete `careconnect.db` and restart the app.

---

## 📊 What Changed from Before

### Simplified Version (app_fixed.py)
- ❌ Removed CSRF protection (for simplicity)
- ❌ Removed rate limiting (for simplicity)
- ❌ Removed Flask-Login (using simple sessions)
- ❌ Removed Flask-Migrate (using simple db.create_all())
- ✅ Kept password hashing (security)
- ✅ Kept SQLite database (data persistence)
- ✅ Kept ML predictions (core feature)

This version is simpler and more reliable for local development and testing.

---

## 🎯 Testing Checklist

1. ✅ Start the app: `python app_fixed.py`
2. ✅ Open browser: http://127.0.0.1:5000
3. ✅ Login with admin/admin123
4. ✅ Go to "Log Today's Routine"
5. ✅ Fill the form and submit
6. ✅ Check dashboard - should show your entry
7. ✅ Logout and login again - data should persist

---

## 🚀 For Production Deployment

When you're ready to deploy to Render/Railway:

1. Use `app_fixed.py` (it's simpler and works)
2. Update `Procfile`:
   ```
   web: gunicorn app_fixed:app
   ```
3. Set environment variable:
   ```
   SECRET_KEY=<generate-random-key>
   DATABASE_URL=<postgresql-url-from-render>
   ```
4. For PostgreSQL, update the database URI in `app_fixed.py`

---

## 💡 Tips

- The database file `careconnect.db` will be created automatically
- All data is stored in this file
- To reset everything, just delete `careconnect.db` and restart
- The model file `model.pkl` only needs to be trained once

---

## 🆘 Still Having Issues?

1. Make sure you're in the correct directory
2. Make sure Python is installed: `python --version`
3. Make sure all dependencies are installed
4. Try deleting `careconnect.db` and restarting
5. Check if port 5000 is available

---

**Ready to start?**

```cmd
start_app.cmd
```

or

```cmd
python app_fixed.py
```

Then open: **http://127.0.0.1:5000**
