# 🔧 Fix Login Issue - Step by Step

## Problem
You're seeing "Rate limit exceeded" error and being redirected to dashboard automatically.

## Why This Happens
1. You have an old session cookie from a previous login
2. An old version of the app might still be running

## ✅ Solution (Choose One)

---

### Option A: Fresh Start (Easiest)

1. **Run this command:**
   ```cmd
   fresh_start.cmd
   ```

2. **Clear your browser cookies:**
   - Press `Ctrl + Shift + Delete`
   - Select "Cookies" and "Last hour"
   - Click "Clear data"

3. **Go to:** http://127.0.0.1:5000

4. **Login:**
   - Username: `admin`
   - Password: `admin123`

---

### Option B: Manual Steps

1. **Stop all Python processes:**
   ```cmd
   taskkill /F /IM python.exe
   ```

2. **Delete old database:**
   ```cmd
   del careconnect.db
   ```

3. **Start the app:**
   ```cmd
   python app_fixed.py
   ```

4. **Clear browser cookies** (Ctrl+Shift+Delete)

5. **Go to:** http://127.0.0.1:5000

---

### Option C: Use Incognito Mode (Quickest)

1. **Stop the old app:**
   ```cmd
   taskkill /F /IM python.exe
   ```

2. **Start fresh:**
   ```cmd
   python app_fixed.py
   ```

3. **Open Incognito/Private window:**
   - Chrome: `Ctrl + Shift + N`
   - Firefox: `Ctrl + Shift + P`
   - Edge: `Ctrl + Shift + N`

4. **Go to:** http://127.0.0.1:5000

5. **Login:** admin / admin123

---

## 🔄 Clear Session Manually

If you're still stuck, go to this URL to force clear your session:

**http://127.0.0.1:5000/clear-session**

This will:
- Clear your server-side session
- Clear browser local storage
- Show you instructions

Then click "Go to Login"

---

## ⚠️ Important Notes

### Make Sure You're Running app_fixed.py

Check your terminal - it should show:
```
✓ ML Model loaded successfully
✓ Admin user created
✓ Database initialized
* Running on http://127.0.0.1:5000
```

If you see "Rate limit" errors in the terminal, you're running the wrong file!

### Don't Run Multiple Apps

Only run ONE of these at a time:
- ✅ `app_fixed.py` (USE THIS)
- ❌ `app.py` (OLD - don't use)
- ❌ `app_production.py` (OLD - don't use)
- ❌ `app_secure.py` (OLD - don't use)

---

## 🧪 Test If It's Working

1. Open Incognito window
2. Go to: http://127.0.0.1:5000
3. You should see the home page (NOT dashboard)
4. Click "Sign In"
5. Enter: admin / admin123
6. Should login successfully

---

## 🆘 Still Not Working?

### Check What's Running
```cmd
netstat -ano | findstr :5000
```

If you see a process, kill it:
```cmd
taskkill /F /PID <process-id>
```

### Nuclear Option (Reset Everything)
```cmd
taskkill /F /IM python.exe
del careconnect.db
del *.pyc
python app_fixed.py
```

Then use Incognito mode.

---

## ✅ Success Checklist

- [ ] Stopped all old Python processes
- [ ] Deleted careconnect.db (optional but recommended)
- [ ] Running `python app_fixed.py`
- [ ] Cleared browser cookies OR using Incognito
- [ ] Can see home page at http://127.0.0.1:5000
- [ ] Can login with admin/admin123
- [ ] Dashboard loads after login

---

## 🎯 Quick Fix Command

Copy and paste this entire block:

```cmd
taskkill /F /IM python.exe & timeout /t 2 /nobreak & del careconnect.db & python app_fixed.py
```

Then open Incognito mode and go to http://127.0.0.1:5000

---

**Need more help?** Make sure you're using `app_fixed.py` and Incognito mode!
