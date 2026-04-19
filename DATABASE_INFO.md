# 🗄️ CareConnect Database Documentation

## Database Overview

CareConnect uses **PostgreSQL** database hosted on **Render** for production deployment.

---

## 📊 Database Structure

### Tables

#### 1. **users** table
Stores user account information:
- `id` - Unique user identifier (Primary Key)
- `username` - User's login name (Unique)
- `email` - User's email address (Unique)
- `password_hash` - Encrypted password (using Werkzeug security)
- `role` - User role (admin/user)
- `created_at` - Account creation timestamp

#### 2. **health_records** table
Stores daily health monitoring data:
- `id` - Record identifier (Primary Key)
- `user_id` - Foreign key linking to users table
- `age` - Patient age
- `medication_taken` - Whether medication was taken (0/1)
- `meals_taken` - Whether meals were taken (0/1)
- `cleaning_done` - Whether hygiene routine was done (0/1)
- `compliance_score` - Calculated compliance percentage (0-100)
- `rule_risk` - Rule-based risk assessment (Low/Moderate/High)
- `ml_prediction` - Machine Learning risk prediction
- `recorded_at` - Timestamp of record creation

---

## 🔗 Database Connection

### Production (Render)
- **Type:** PostgreSQL 16
- **Host:** Render Cloud
- **Connection:** Automatic via `DATABASE_URL` environment variable
- **Backup:** Automatic daily backups by Render

### Local Development
- **Type:** SQLite
- **File:** `careconnect.db`
- **Location:** Project root directory

---

## 🔐 Security Features

1. **Password Hashing:** All passwords encrypted using Werkzeug's `generate_password_hash`
2. **SQL Injection Protection:** SQLAlchemy ORM prevents SQL injection
3. **Environment Variables:** Database credentials stored securely in environment
4. **Session Management:** Flask sessions with secret key encryption

---

## 📈 How to View Database

### Method 1: Run the Database Info Script

```bash
python show_database.py
```

This will display:
- Database connection info
- All tables and columns
- User count and sample users
- Health records count and recent entries

### Method 2: Access Render Dashboard

1. Go to: https://dashboard.render.com
2. Login to your account
3. Click on "careconnect-db" (PostgreSQL database)
4. View:
   - Connection details
   - Storage usage
   - Database metrics
   - Backup status

### Method 3: Use Database Client (Advanced)

Connect using tools like:
- **pgAdmin** (PostgreSQL GUI)
- **DBeaver** (Universal database tool)
- **psql** (Command line)

Connection details available in Render dashboard under "Connections" section.

---

## 📊 Sample Data Flow

```
User Registration
    ↓
User data saved to 'users' table
    ↓
User logs in
    ↓
User enters health data
    ↓
ML model predicts risk
    ↓
Record saved to 'health_records' table
    ↓
Dashboard displays data from database
```

---

## 🎯 Database Features

✅ **Persistent Storage** - All data saved permanently
✅ **Relational Data** - Users linked to their health records
✅ **Automatic Timestamps** - Records when data was created
✅ **Data Integrity** - Foreign key constraints ensure data consistency
✅ **Scalable** - PostgreSQL can handle thousands of users
✅ **Cloud Hosted** - Accessible from anywhere

---

## 🔍 Verification Commands

### Check if database is working:
```bash
python -c "from app_fixed import app, db; app.app_context().push(); print('Tables:', db.engine.table_names())"
```

### Count users:
```bash
python -c "from app_fixed import app, User; app.app_context().push(); print('Users:', User.query.count())"
```

### Count health records:
```bash
python -c "from app_fixed import app, HealthRecord; app.app_context().push(); print('Records:', HealthRecord.query.count())"
```

---

## 📝 For Your Teacher

**Key Points to Mention:**

1. **Production Database:** PostgreSQL hosted on Render cloud platform
2. **Two Tables:** Users and Health Records with proper relationships
3. **Security:** Passwords are hashed, not stored in plain text
4. **Persistence:** All data is permanently stored and survives app restarts
5. **Scalability:** Can handle multiple users simultaneously
6. **Professional Setup:** Using industry-standard database (PostgreSQL)

**Demo Steps:**

1. Show the Render dashboard with the database
2. Run `python show_database.py` to display database structure
3. Login to the app and create a health record
4. Run the script again to show the new data was saved
5. Refresh the dashboard to show updated data

---

## 🎓 Technical Details

- **ORM:** SQLAlchemy (Python database toolkit)
- **Migration Support:** Flask-Migrate ready (for future schema changes)
- **Connection Pooling:** Automatic connection management
- **Transaction Support:** ACID compliance for data integrity
- **Indexing:** Primary keys and unique constraints for fast queries

---

**Database is fully functional and production-ready!** ✅
