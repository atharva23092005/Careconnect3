"""
CareConnect - Working Production Version
"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pickle
import numpy as np
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))

# Use PostgreSQL in production (Render/Railway), SQLite locally
database_url = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'careconnect.db'))

# Fix for Render/Heroku postgres:// URL
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# ─── Database Models ──────────────────────────────────────────────────────────

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    health_records = db.relationship('HealthRecord', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class HealthRecord(db.Model):
    __tablename__ = 'health_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    medication_taken = db.Column(db.Integer, nullable=False)
    meals_taken = db.Column(db.Integer, nullable=False)
    cleaning_done = db.Column(db.Integer, nullable=False)
    compliance_score = db.Column(db.Float, nullable=False)
    rule_risk = db.Column(db.String(20), nullable=False)
    ml_prediction = db.Column(db.String(20), nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

# ─── Load ML Model ────────────────────────────────────────────────────────────

MODEL_PATH = os.path.join(basedir, 'model.pkl')

def load_ml_model():
    try:
        with open(MODEL_PATH, 'rb') as f:
            model_data = pickle.load(f)
        print("✓ ML Model loaded successfully")
        return model_data['model'], model_data['label_encoder']
    except Exception as e:
        print(f"⚠ WARNING: Could not load model: {e}")
        return None, None

model, label_encoder = load_ml_model()

# ─── Helper Functions ─────────────────────────────────────────────────────────

def compute_score(medication, meals, cleaning):
    return round((medication * 0.5 + meals * 0.3 + cleaning * 0.2) * 100, 1)

def rule_based_risk(score):
    if score >= 80:
        return 'Low'
    elif score >= 60:
        return 'Moderate'
    return 'High'

def ml_predict(age, medication, meals, cleaning):
    if model is None or label_encoder is None:
        return 'Unknown'
    try:
        X = np.array([[age, medication, meals, cleaning]])
        pred = model.predict(X)[0]
        return label_encoder.inverse_transform([pred])[0]
    except Exception as e:
        print(f"ML Prediction error: {e}")
        return 'Unknown'

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    # Check if there's a logout parameter
    if request.args.get('logout') == 'true':
        session.clear()
    
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm_password', '').strip()
        
        if not username or not email or not password:
            error = 'All fields are required.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif password != confirm:
            error = 'Passwords do not match.'
        elif User.query.filter_by(username=username).first():
            error = 'Username already taken.'
        elif User.query.filter_by(email=email).first():
            error = 'Email already registered.'
        else:
            try:
                user = User(username=username, email=email, role='user')
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                error = 'Registration failed. Please try again.'
                print(f"Registration error: {e}")
    
    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            error = 'Username and password are required.'
        else:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid username or password.'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return render_template('clear_session.html')

@app.route('/clear-session')
def clear_session():
    session.clear()
    return render_template('clear_session.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    records = HealthRecord.query.filter_by(user_id=session['user_id'])\
        .order_by(HealthRecord.recorded_at.desc())\
        .limit(7)\
        .all()
    
    latest = None
    if records:
        r = records[0]
        latest = {
            'id': r.id,
            'age': r.age,
            'medication_taken': r.medication_taken,
            'meals_taken': r.meals_taken,
            'cleaning_done': r.cleaning_done,
            'compliance_score': r.compliance_score,
            'rule_risk': r.rule_risk,
            'ml_prediction': r.ml_prediction,
            'recorded_at': r.recorded_at.isoformat()
        }
    
    records_list = []
    for r in records:
        records_list.append({
            'id': r.id,
            'age': r.age,
            'medication_taken': r.medication_taken,
            'meals_taken': r.meals_taken,
            'cleaning_done': r.cleaning_done,
            'compliance_score': r.compliance_score,
            'rule_risk': r.rule_risk,
            'ml_prediction': r.ml_prediction,
            'recorded_at': r.recorded_at.isoformat()
        })
    
    return render_template(
        'dashboard.html',
        latest=latest,
        records=records_list,
        username=session['username']
    )

@app.route('/health-input')
def health_input():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('health_input.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.get_json(silent=True) or request.form
    
    try:
        age = int(data.get('age', 0))
        medication = int(data.get('medication', 0))
        meals = int(data.get('meals', 0))
        cleaning = int(data.get('cleaning', 0))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input values.'}), 400
    
    if not (50 <= age <= 110):
        return jsonify({'error': 'Age must be between 50 and 110.'}), 400
    
    if any(v not in (0, 1) for v in [medication, meals, cleaning]):
        return jsonify({'error': 'Medication, meals, and cleaning must be 0 or 1.'}), 400
    
    score = compute_score(medication, meals, cleaning)
    rule_risk = rule_based_risk(score)
    ml_risk = ml_predict(age, medication, meals, cleaning)
    
    try:
        record = HealthRecord(
            user_id=session['user_id'],
            age=age,
            medication_taken=medication,
            meals_taken=meals,
            cleaning_done=cleaning,
            compliance_score=score,
            rule_risk=rule_risk,
            ml_prediction=ml_risk
        )
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to save record.'}), 500
    
    return jsonify({
        'compliance_score': score,
        'rule_based_risk': rule_risk,
        'ml_prediction': ml_risk
    })

@app.route('/health')
def health_check():
    try:
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception:
        db_status = 'unhealthy'
    
    model_status = 'healthy' if model is not None else 'unhealthy'
    
    return jsonify({
        'status': 'healthy' if db_status == 'healthy' and model_status == 'healthy' else 'unhealthy',
        'database': db_status,
        'ml_model': model_status
    })

# ─── Initialize Database ──────────────────────────────────────────────────────

def init_db():
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@careconnect.com', role='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created (username: admin, password: admin123)")
        
        print("✓ Database initialized")

# ─── Run Application ──────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
