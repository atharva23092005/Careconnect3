# 🚀 Deployment Guide

## Quick Deploy to Railway

### 1. Push to GitHub
```bash
git add .
git commit -m "Update"
git push origin main
```

### 2. Deploy on Railway
1. Go to [railway.app](https://railway.app)
2. Login with GitHub
3. New Project → Deploy from GitHub repo
4. Select your repository
5. Add PostgreSQL database (New → Database → PostgreSQL)
6. Add environment variable:
   - Key: `SECRET_KEY`
   - Value: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
7. Settings → Start Command: `gunicorn app_fixed:app --bind 0.0.0.0:$PORT`
8. Settings → Generate Domain
9. Done!

---

## Local Development

### Run Locally
```bash
python app_fixed.py
```

### Access
```
http://127.0.0.1:5000
```

### Login
- Username: admin
- Password: admin123

---

## Environment Variables

### Required for Production
- `SECRET_KEY` - Random secret key for sessions
- `DATABASE_URL` - Automatically set by Railway PostgreSQL

### Optional
- `PORT` - Automatically set by Railway

---

## Files Overview

### Essential Files
- `app_fixed.py` - Main application
- `model.pkl` - Pre-trained ML model
- `requirements.txt` - Dependencies
- `Procfile` - Deployment config
- `runtime.txt` - Python version

### Folders
- `templates/` - HTML files
- `static/` - CSS and assets
- `Dataset/` - Training data

---

## Troubleshooting

### App not starting?
- Check Railway logs
- Verify start command: `gunicorn app_fixed:app --bind 0.0.0.0:$PORT`
- Ensure PostgreSQL is added

### Database errors?
- Make sure PostgreSQL database is created
- DATABASE_URL should be automatic

### Build failed?
- Check if all files are pushed to GitHub
- Verify requirements.txt is correct

---

## Support

- Railway Docs: https://docs.railway.app
- GitHub Repo: https://github.com/atharva23092005/CareConnect

---

**Your app is deployed and running! 🎉**
