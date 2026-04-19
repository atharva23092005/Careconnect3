from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
import os
import pickle
import numpy as np
from datetime import datetime
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(BASE_DIR, 'data')
DATASET_DIR = os.path.join(BASE_DIR, 'Dataset')
os.makedirs(DATA_DIR, exist_ok=True)

USERS_CSV   = os.path.join(DATA_DIR, 'users.csv')
HEALTH_CSV  = os.path.join(DATA_DIR, 'health_records.csv')
MODEL_PATH  = os.path.join(DATA_DIR, 'model.pkl')
DATASET_XLS = os.path.join(DATASET_DIR, 'healthcare_dataset.xlsx')

# ─── CSV Initialisation ───────────────────────────────────────────────────────
def init_csv():
    if not os.path.exists(USERS_CSV):
        # Hash the admin password
        hashed_password = generate_password_hash('admin123')
        admin = pd.DataFrame([{
            'id': 1, 'username': 'admin', 'email': 'admin@careconnect.com',
            'password': hashed_password, 'role': 'admin',
            'created_at': datetime.now().isoformat()
        }])
        admin.to_csv(USERS_CSV, index=False)

    if not os.path.exists(HEALTH_CSV):
        pd.DataFrame(columns=[
            'id', 'user_id', 'username', 'age',
            'medication_taken', 'meals_taken', 'cleaning_done',
            'compliance_score', 'rule_risk', 'ml_prediction', 'recorded_at'
        ]).to_csv(HEALTH_CSV, index=False)

init_csv()

# ─── ML Model — trained on real Excel dataset ─────────────────────────────────
def train_model_from_dataset():
    """Load healthcare_dataset.xlsx and train a Decision Tree."""
    try:
        df = pd.read_excel(DATASET_XLS)

        # Rename the oddly named column produced by Excel RANDBETWEEN formula
        med_col = [c for c in df.columns if 'Medication_Taken' in c][0]
        df.rename(columns={med_col: 'Medication_Taken'}, inplace=True)

        # Keep only usable rows
        features = ['Age', 'Medication_Taken', 'Meals_Taken', 'Cleaning_Done']
        target   = 'Risk_Level'
        df = df[features + [target]].dropna()

        # Encode target
        le = LabelEncoder()
        df[target] = le.fit_transform(df[target])   # High=0, Low=1, Moderate=2

        X = df[features].values
        y = df[target].values

        clf = DecisionTreeClassifier(max_depth=6, random_state=42)
        clf.fit(X, y)

        with open(MODEL_PATH, 'wb') as f:
            pickle.dump({'model': clf, 'label_encoder': le}, f)

        print("[CareConnect] Model trained from dataset and saved.")
        return clf, le
    except Exception as e:
        print(f"[ERROR] Failed to train model: {e}")
        raise

def load_model():
    if os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, 'rb') as f:
                obj = pickle.load(f)
            return obj['model'], obj['label_encoder']
        except Exception as e:
            print(f"[WARNING] Failed to load model: {e}. Retraining...")
    return train_model_from_dataset()

model, label_encoder = load_model()

# ─── Helpers ──────────────────────────────────────────────────────────────────
def get_users():
    try:
        return pd.read_csv(USERS_CSV)
    except Exception as e:
        print(f"[ERROR] Failed to read users: {e}")
        return pd.DataFrame()

def get_health():
    try:
        return pd.read_csv(HEALTH_CSV)
    except Exception as e:
        print(f"[ERROR] Failed to read health records: {e}")
        return pd.DataFrame()

def next_id(df):
    return int(df['id'].max()) + 1 if len(df) > 0 and not df['id'].isna().all() else 1

def compute_score(medication, meals, cleaning):
    """Rule-based compliance score (0–100)."""
    return round((medication * 0.5 + meals * 0.3 + cleaning * 0.2) * 100, 1)

def rule_based_risk(score):
    """Classify risk from compliance score."""
    if score >= 80:
        return 'Low'
    elif score >= 60:
        return 'Moderate'
    return 'High'

def ml_predict(age, medication, meals, cleaning):
    """Use the trained Decision Tree to predict risk."""
    X = np.array([[age, medication, meals, cleaning]])
    pred = model.predict(X)[0]
    return label_encoder.inverse_transform([pred])[0]

# ─── Auth Routes ──────────────────────────────────────────────────────────────
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            error = 'Username and password are required.'
        else:
            users = get_users()
            user = users[users['username'] == username]
            
            if not user.empty:
                row = user.iloc[0]
                # Check hashed password
                if check_password_hash(row['password'], password):
                    session['user_id']  = int(row['id'])
                    session['username'] = row['username']
                    session['role']     = row['role']
                    return redirect(url_for('dashboard'))
            
            error = 'Invalid username or password.'
    
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm  = request.form.get('confirm_password', '').strip()

        if not username or not email or not password:
            error = 'All fields are required.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        elif password != confirm:
            error = 'Passwords do not match.'
        else:
            users = get_users()
            if username in users['username'].values:
                error = 'Username already taken.'
            elif email in users['email'].values:
                error = 'Email already registered.'
            else:
                # Hash the password before storing
                hashed_password = generate_password_hash(password)
                new_user = pd.DataFrame([{
                    'id': next_id(users), 'username': username,
                    'email': email, 'password': hashed_password,
                    'role': 'user', 'created_at': datetime.now().isoformat()
                }])
                pd.concat([users, new_user], ignore_index=True).to_csv(USERS_CSV, index=False)
                return redirect(url_for('login'))
    
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ─── Dashboard ────────────────────────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    health = get_health()
    user_records = health[health['user_id'] == session['user_id']].sort_values('recorded_at', ascending=False)
    latest  = user_records.iloc[0].to_dict() if not user_records.empty else None
    records = user_records.head(7).to_dict('records')
    
    return render_template('dashboard.html', latest=latest, records=records, username=session['username'])

# ─── Health Input ─────────────────────────────────────────────────────────────
@app.route('/health-input', methods=['GET', 'POST'])
def health_input():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('health_input.html')

# ─── /predict API ─────────────────────────────────────────────────────────────
@app.route('/predict', methods=['POST'])
def predict():
    """Accept JSON or form data, return compliance score + risk predictions."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    data = request.get_json(silent=True) or request.form

    try:
        age        = int(data.get('age', 0))
        medication = int(data.get('medication', 0))
        meals      = int(data.get('meals', 0))
        cleaning   = int(data.get('cleaning', 0))
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid input values. Ensure all fields are numbers.'}), 400

    if not (50 <= age <= 110):
        return jsonify({'error': 'Age must be between 50 and 110.'}), 400
    if any(v not in (0, 1) for v in [medication, meals, cleaning]):
        return jsonify({'error': 'Medication, meals, and cleaning must be 0 or 1.'}), 400

    score      = compute_score(medication, meals, cleaning)
    rule_risk  = rule_based_risk(score)
    ml_risk    = ml_predict(age, medication, meals, cleaning)

    # Persist to CSV
    try:
        health = get_health()
        new_rec = pd.DataFrame([{
            'id': next_id(health),
            'user_id': session['user_id'],
            'username': session['username'],
            'age': age,
            'medication_taken': medication,
            'meals_taken': meals,
            'cleaning_done': cleaning,
            'compliance_score': score,
            'rule_risk': rule_risk,
            'ml_prediction': ml_risk,
            'recorded_at': datetime.now().isoformat()
        }])
        pd.concat([health, new_rec], ignore_index=True).to_csv(HEALTH_CSV, index=False)
    except Exception as e:
        print(f"[ERROR] Failed to save health record: {e}")

    return jsonify({
        'compliance_score': score,
        'rule_based_risk': rule_risk,
        'ml_prediction': ml_risk
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
