"""
CareConnect - Production-Ready Flask Application
Elderly Routine Monitoring & AI Health Risk Prediction
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
import os
import pickle
import numpy as np
from datetime import datetime

from config import config
from models import db, User, HealthRecord

# Initialize Flask app
app = Flask(__name__)

# Load configuration
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config['RATELIMIT_STORAGE_URL']
)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ─── Load ML Model ────────────────────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')

def load_ml_model():
    """Load the pre-trained ML model."""
    try:
        with open(MODEL_PATH, 'rb') as f:
            model_data = pickle.load(f)
        print(f"✓ ML Model loaded successfully (Accuracy: {model_data.get('accuracy', 'N/A')})")
        return model_data['model'], model_data['label_encoder']
    except FileNotFoundError:
        print("⚠ WARNING: model.pkl not found. Run 'python train_model.py' first!")
        return None, None
    except Exception as e:
        print(f"⚠ ERROR loading model: {e}")
        return None, None

model, label_encoder = load_ml_model()

# ─── Helper Functions ─────────────────────────────────────────────────────────
def compute_score(medication, meals, cleaning):
    """Calculate compliance score (0-100)."""
    return round((medication * 0.5 + meals * 0.3 + cleaning * 0.2) * 100, 1)

def rule_based_risk(score):
    """Classify risk based on compliance score."""
    if score >= 80:
        return 'Low'
    elif score >= 60:
        return 'Moderate'
    return 'High'

def ml_predict(age, medication, meals, cleaning):
    """Use ML model to predict risk level."""
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
    """Home page."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm_password', '').strip()
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
        elif len(username) < 3:
            flash('Username must be at least 3 characters.', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
        elif password != confirm:
            flash('Passwords do not match.', 'error')
        elif User.query.filter_by(username=username).first():
            flash('Username already taken.', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
        else:
            # Create new user
            user = User(username=username, email=email, role='user')
            user.set_password(password)
            
            try:
                db.session.add(user)
                db.session.commit()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                flash('Registration failed. Please try again.', 'error')
                print(f"Registration error: {e}")
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Username and password are required.', 'error')
        else:
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with health statistics."""
    # Get user's health records
    records = HealthRecord.query.filter_by(user_id=current_user.id)\
        .order_by(HealthRecord.recorded_at.desc())\
        .limit(7)\
        .all()
    
    # Convert to dictionaries for template
    latest = records[0].to_dict() if records else None
    records_list = [r.to_dict() for r in records]
    
    return render_template(
        'dashboard.html',
        latest=latest,
        records=records_list,
        username=current_user.username
    )

@app.route('/health-input', methods=['GET', 'POST'])
@login_required
def health_input():
    """Health data input form."""
    return render_template('health_input.html')

@app.route('/predict', methods=['POST'])
@login_required
@limiter.limit("30 per hour")
def predict():
    """API endpoint for health risk prediction."""
    data = request.get_json(silent=True) or request.form
    
    # Validate input
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
    
    # Calculate predictions
    score = compute_score(medication, meals, cleaning)
    rule_risk = rule_based_risk(score)
    ml_risk = ml_predict(age, medication, meals, cleaning)
    
    # Save to database
    try:
        record = HealthRecord(
            user_id=current_user.id,
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
    """Health check endpoint for monitoring."""
    try:
        # Check database connection
        db.session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception:
        db_status = 'unhealthy'
    
    model_status = 'healthy' if model is not None else 'unhealthy'
    
    return jsonify({
        'status': 'healthy' if db_status == 'healthy' and model_status == 'healthy' else 'unhealthy',
        'database': db_status,
        'ml_model': model_status,
        'timestamp': datetime.utcnow().isoformat()
    })

# ─── Error Handlers ───────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

# ─── Database Initialization ──────────────────────────────────────────────────

def init_database():
    """Initialize database with admin user."""
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@careconnect.com',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created (username: admin, password: admin123)")
        
        print("✓ Database initialized")

# ─── Application Entry Point ──────────────────────────────────────────────────

if __name__ == '__main__':
    init_database()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=(env == 'development'), host='0.0.0.0', port=port)
