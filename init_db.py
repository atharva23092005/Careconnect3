"""
Initialize database and create migrations.
Run this locally before first deployment: python init_db.py
"""
import os
from app_production import app, db
from flask_migrate import init as migrate_init, migrate, upgrade

def setup_database():
    """Initialize database and create migration files."""
    with app.app_context():
        print("[1/4] Creating database tables...")
        db.create_all()
        print("✓ Database tables created")
        
        # Initialize migrations if not already done
        if not os.path.exists('migrations'):
            print("\n[2/4] Initializing Flask-Migrate...")
            migrate_init()
            print("✓ Migrations folder created")
            
            print("\n[3/4] Creating initial migration...")
            migrate(message='Initial migration')
            print("✓ Initial migration created")
            
            print("\n[4/4] Applying migrations...")
            upgrade()
            print("✓ Migrations applied")
        else:
            print("\n[2/4] Migrations already initialized")
            print("\n[3/4] Creating new migration...")
            migrate(message='Update schema')
            print("✓ Migration created")
            
            print("\n[4/4] Applying migrations...")
            upgrade()
            print("✓ Migrations applied")
        
        print("\n🎉 Database setup complete!")
        print("\nNext steps:")
        print("1. Train the model: python train_model.py")
        print("2. Test locally: python app_production.py")
        print("3. Commit migrations folder to git")
        print("4. Deploy to Render")

if __name__ == '__main__':
    setup_database()
