"""
Pre-train the ML model and save it for production use.
Run this once before deployment: python train_model.py
"""
import pandas as pd
import pickle
import os
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, 'Dataset')
DATASET_XLS = os.path.join(DATASET_DIR, 'healthcare_dataset.xlsx')
MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')

def train_and_save_model():
    """Train the Decision Tree model and save it."""
    print("[1/5] Loading dataset...")
    df = pd.read_excel(DATASET_XLS)
    
    # Rename the oddly named column
    med_col = [c for c in df.columns if 'Medication_Taken' in c][0]
    df.rename(columns={med_col: 'Medication_Taken'}, inplace=True)
    
    # Prepare features and target
    features = ['Age', 'Medication_Taken', 'Meals_Taken', 'Cleaning_Done']
    target = 'Risk_Level'
    df = df[features + [target]].dropna()
    
    print(f"[2/5] Dataset loaded: {len(df)} records")
    print(f"      Risk distribution:\n{df[target].value_counts()}\n")
    
    # Encode target
    le = LabelEncoder()
    df[target] = le.fit_transform(df[target])
    
    X = df[features].values
    y = df[target].values
    
    # Split for validation
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("[3/5] Training Decision Tree model...")
    clf = DecisionTreeClassifier(max_depth=6, random_state=42)
    clf.fit(X_train, y_train)
    
    # Evaluate
    print("[4/5] Evaluating model...")
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✓ Model Accuracy: {accuracy:.2%}\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    # Save model
    print("[5/5] Saving model...")
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump({
            'model': clf,
            'label_encoder': le,
            'features': features,
            'accuracy': accuracy
        }, f)
    
    print(f"\n✓ Model saved to: {MODEL_PATH}")
    print(f"✓ File size: {os.path.getsize(MODEL_PATH) / 1024:.2f} KB")
    print("\n🎉 Model training complete! Ready for deployment.\n")

if __name__ == '__main__':
    train_and_save_model()
