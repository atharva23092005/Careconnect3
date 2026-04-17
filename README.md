<div align="center">

# 💚 CareConnect
### Elderly Routine Monitoring & AI Health Risk Prediction

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![Pandas](https://img.shields.io/badge/Pandas-Data-150458?style=flat-square&logo=pandas&logoColor=white)](https://pandas.pydata.org)

*A compassionate web application that monitors daily routines of elderly individuals and predicts health risk levels using Machine Learning.*

</div>

---

## 📌 Overview

**CareConnect** is a healthcare web application built for the elderly population and their caregivers. It tracks daily routine compliance — medication, meals, and hygiene — then uses a Decision Tree ML model trained on real patient data to assess the individual's health risk level.

### Key Features

- 🔐 **User Authentication** — Register, login, and session-based access control
- 📋 **Daily Health Log** — Log medication, meals, and hygiene habits via a clean form
- 📊 **Compliance Score** — Weighted formula calculating adherence (0–100)
- 🤖 **AI Risk Prediction** — Decision Tree model predicts Low / Moderate / High risk
- ⚖️ **Dual Prediction** — Both rule-based and ML-based risk shown side-by-side
- 📈 **Dashboard** — Visual progress bar, color-coded metric cards, history table
- 💾 **Data Storage** — All entries stored in CSV for persistence

---

## 🖼️ Screenshots

| Home Page | Login | Dashboard |
|---|---|---|
| Hero with CTA buttons | Clean centered card | Cards + progress bar |

| Health Log | Result |
|---|---|
| Dropdown routine form | Animated score ring + risk badges |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Flask |
| **ML Model** | Scikit-learn (Decision Tree Classifier) |
| **Data** | Pandas, OpenPyXL, CSV storage |
| **Frontend** | HTML5, CSS3 (custom), Vanilla JavaScript (Fetch API) |
| **Icons** | Font Awesome 6 |
| **Fonts** | Nunito (Google Fonts) |

---

## 📁 Project Structure

```
Project_CareConnect/
├── app.py                    # Flask backend — routes, ML model, /predict API
├── requirements.txt          # Python dependencies
│
├── Dataset/
│   └── healthcare_dataset.xlsx   # Training dataset (55,000+ hospital records)
│
├── data/                     # Auto-generated on first run (gitignored)
│   ├── users.csv             # Registered users
│   ├── health_records.csv    # Health log entries
│   └── model.pkl             # Trained Decision Tree
│
├── static/
│   └── css/
│       └── style.css         # Full soothing healthcare design system
│
└── templates/
    ├── base.html             # Navbar layout shell
    ├── index.html            # Home / landing page
    ├── login.html            # Sign in
    ├── register.html         # Create account
    ├── health_input.html     # Daily routine form (JS fetch → /predict)
    └── dashboard.html        # Stats cards, progress bar, history table
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/CareConnect.git
cd CareConnect
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:
- **Windows:** `.\.venv\Scripts\activate`
- **macOS/Linux:** `source .venv/bin/activate`

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open your browser at **http://127.0.0.1:5000**

> ℹ️ On first run, the app will automatically:
> - Create the `data/` directory and CSV files
> - Load `Dataset/healthcare_dataset.xlsx`
> - Train the Decision Tree model and save it as `data/model.pkl`

---

## 🔑 Default Login

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |

---

## 🤖 How the ML Model Works

### Training Data
The model is trained on `healthcare_dataset.xlsx` — a real-world hospital dataset with **55,000+ patient records**.

### Features Used
| Feature | Type | Description |
|---|---|---|
| `Age` | Integer | Patient's age (50–110) |
| `Medication_Taken` | Binary (0/1) | Whether medication was taken |
| `Meals_Taken` | Binary (0/1) | Whether meals were eaten |
| `Cleaning_Done` | Binary (0/1) | Whether hygiene was maintained |

### Target
`Risk_Level` — **Low**, **Moderate**, or **High**

### Algorithm
**Decision Tree Classifier** (`max_depth=6`, `random_state=42`) from Scikit-learn.

---

## 📐 Compliance Score Formula

```
Score = (Medication × 0.5 + Meals × 0.3 + Cleaning × 0.2) × 100
```

| Score | Risk Level |
|---|---|
| ≥ 80 | 🟢 Low |
| 60 – 79 | 🟡 Moderate |
| < 60 | 🔴 High |

---

## 🔗 API Endpoint

### `POST /predict`

**Request (JSON):**
```json
{
  "age": 70,
  "medication": 1,
  "meals": 1,
  "cleaning": 0
}
```

**Response (JSON):**
```json
{
  "compliance_score": 80.0,
  "rule_based_risk": "Low",
  "ml_prediction": "Moderate"
}
```

---

## 🔮 Future Scope

- [ ] Reports page with Chart.js graphs (Compliance Over Time, Risk Distribution)
- [ ] Caregiver module (registration, booking, reviews)
- [ ] Export health records as PDF
- [ ] Mobile-responsive enhancements
- [ ] Email / SMS alerts for high-risk entries
- [ ] Multi-patient support for families

---

## 📄 License

This project was built as an academic project for healthcare technology education.

---

<div align="center">

Made with 💚 for elderly care

</div>
