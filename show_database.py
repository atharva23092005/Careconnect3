"""
Script to show database structure and data
Run this to demonstrate the database to your teacher
"""
from app_fixed import app, db, User, HealthRecord
from sqlalchemy import inspect

def show_database_info():
    with app.app_context():
        print("\n" + "="*60)
        print("📊 CARECONNECT DATABASE INFORMATION")
        print("="*60)
        
        # Show database URL (hide password)
        db_url = str(db.engine.url)
        if '@' in db_url:
            # Hide password for security
            parts = db_url.split('@')
            credentials = parts[0].split('://')
            if len(credentials) > 1 and ':' in credentials[1]:
                user = credentials[1].split(':')[0]
                db_url = f"{credentials[0]}://{user}:****@{parts[1]}"
        
        print(f"\n🔗 Database URL: {db_url}")
        print(f"🗄️  Database Type: PostgreSQL (Production) / SQLite (Local)")
        
        # Show all tables
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"\n📋 Tables in Database: {len(tables)}")
        for table in tables:
            print(f"   ✓ {table}")
            columns = inspector.get_columns(table)
            print(f"     Columns: {len(columns)}")
            for col in columns:
                print(f"       - {col['name']} ({col['type']})")
        
        # Show user count
        user_count = User.query.count()
        print(f"\n👥 Total Users: {user_count}")
        
        if user_count > 0:
            print("\n📝 Sample Users:")
            users = User.query.limit(5).all()
            for user in users:
                print(f"   - {user.username} ({user.email}) - Role: {user.role}")
        
        # Show health records count
        record_count = HealthRecord.query.count()
        print(f"\n📈 Total Health Records: {record_count}")
        
        if record_count > 0:
            print("\n📊 Recent Health Records:")
            records = HealthRecord.query.order_by(HealthRecord.recorded_at.desc()).limit(5).all()
            for record in records:
                user = User.query.get(record.user_id)
                print(f"   - User: {user.username}, Age: {record.age}, "
                      f"Compliance: {record.compliance_score}%, "
                      f"Risk: {record.rule_risk}, "
                      f"ML Prediction: {record.ml_prediction}")
        
        print("\n" + "="*60)
        print("✅ Database is working correctly!")
        print("="*60 + "\n")

if __name__ == '__main__':
    show_database_info()
