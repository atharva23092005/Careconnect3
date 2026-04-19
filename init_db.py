"""
Database initialization script for production deployment
Run this once to create tables and admin user
"""
from app_fixed import app, db, User

def initialize_database():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Tables created")
        
        # Create admin user if not exists
        existing_admin = User.query.filter_by(username='admin').first()
        if not existing_admin:
            admin = User(username='admin', email='admin@careconnect.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created (username: admin, password: admin123)")
        else:
            print("✓ Admin user already exists")
        
        print("✓ Database initialization complete!")

if __name__ == '__main__':
    initialize_database()
