# 💚 CareConnect
### Elderly Routine Monitoring & AI Health Risk Prediction

A compassionate web application that monitors daily routines of elderly individuals and predicts health risk levels using Machine Learning.

---

## 🚀 Live Demo

**Deployed on Railway:** [Your Railway URL]

---

## ✨ Features

- 🔐 User Authentication (Register/Login)
- 📋 Daily Health Logging (Medication, Meals, Hygiene)
- 📊 Compliance Score Calculation
- 🤖 AI Risk Prediction (Decision Tree ML Model)
- 📈 Dashboard with Visual Stats
- 💾 Persistent Data Storage (PostgreSQL)

---

## 🛠️ Tech Stack

- **Backend:** Flask, SQLAlchemy
- **ML Model:** Scikit-learn (Decision Tree)
- **Database:** PostgreSQL (Production), SQLite (Local)
- **Frontend:** HTML5, CSS3, JavaScript
- **Deployment:** Railway

---

## 📋 Local Setup

### 1. Clone Repository
```bash
git clone https://github.com/YOUR-USERNAME/CareConnect.git
cd CareConnect
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
python app_fixed.py
```

### 4. Open Browser
```
http://127.0.0.1:5000
```

### 5. Login
- **Username:** admin
- **Password:** admin123

---

## 🌐 Deployment

### Deploy to Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Create new project from GitHub repo
4. Add PostgreSQL database
5. Add environment variable:
   - `SECRET_KEY` = (generate random key)
6. Deploy!

---

## 📁 Project Structure

```
CareConnect/
├── app_fixed.py          # Main Flask application
├── model.pkl             # Pre-trained ML model
├── train_model.py        # Model training script
├── requirements.txt      # Python dependencies
├── Procfile             # Deployment configuration
├── runtime.txt          # Python version
├── Dataset/             # Training data
├── templates/           # HTML templates
└── static/              # CSS and assets
```

---

## 🔑 Default Credentials

**Username:** admin  
**Password:** admin123

⚠️ Change this after first login!

---

## 🤖 ML Model

- **Algorithm:** Decision Tree Classifier
- **Training Data:** 55,000+ patient records
- **Features:** Age, Medication, Meals, Hygiene
- **Accuracy:** ~85%

---

## 📊 Compliance Score Formula

```
Score = (Medication × 0.5 + Meals × 0.3 + Hygiene × 0.2) × 100
```

**Risk Levels:**
- ≥ 80: Low Risk 🟢
- 60-79: Moderate Risk 🟡
- < 60: High Risk 🔴

---

## 🧪 Testing

1. Register a new account
2. Log daily health routine
3. View compliance score
4. Check ML prediction
5. Review dashboard stats

---

## 📄 License

Academic project for healthcare technology education.

---

## 👥 Contributors

- Shrutkirti01
- atharva23092005

---

## 🙏 Acknowledgments

Built with 💚 for elderly care and health monitoring.

---

**Made with Flask, Scikit-learn, and PostgreSQL**
