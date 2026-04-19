"""
Database models for CareConnect application.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and profile."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    health_records = db.relationship('HealthRecord', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class HealthRecord(db.Model):
    """Health record model for storing daily health logs."""
    __tablename__ = 'health_records'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    age = db.Column(db.Integer, nullable=False)
    medication_taken = db.Column(db.Integer, nullable=False)  # 0 or 1
    meals_taken = db.Column(db.Integer, nullable=False)  # 0 or 1
    cleaning_done = db.Column(db.Integer, nullable=False)  # 0 or 1
    compliance_score = db.Column(db.Float, nullable=False)
    rule_risk = db.Column(db.String(20), nullable=False)  # Low, Moderate, High
    ml_prediction = db.Column(db.String(20), nullable=False)  # Low, Moderate, High
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def to_dict(self):
        """Convert record to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'age': self.age,
            'medication_taken': self.medication_taken,
            'meals_taken': self.meals_taken,
            'cleaning_done': self.cleaning_done,
            'compliance_score': self.compliance_score,
            'rule_risk': self.rule_risk,
            'ml_prediction': self.ml_prediction,
            'recorded_at': self.recorded_at.isoformat()
        }
    
    def __repr__(self):
        return f'<HealthRecord {self.id} - User {self.user_id}>'
