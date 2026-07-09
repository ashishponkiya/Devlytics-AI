"""
STEP 2: Model Training Script
Trains machine learning models to predict developer performance

This script will:
1. Load the generated data
2. Split into training and testing sets
3. Train multiple ML models
4. Evaluate their performance
5. Save the best model for later predictions
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    confusion_matrix,
    classification_report
)
import xgboost as xgb
import joblib
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("🤖 DEVELOPER PERFORMANCE PREDICTION MODEL TRAINING")
print("=" * 60)

# ============================================
# STEP 1: Load Data
# ============================================
print("\n📂 Loading data...")
df = pd.read_csv('developer_data.csv')
print(f"✅ Loaded {len(df)} developer records")

# ============================================
# STEP 2: Feature Selection
# ============================================
print("\n🎯 Selecting features for model training...")

# Features to use (everything except ID and target)
features = [
    'Years_Experience',
    'Git_Commits_Per_Month',
    'Pull_Requests',
    'PR_Acceptance_Rate',
    'Bugs_Fixed',
    'Bugs_Introduced',
    'Unit_Test_Coverage',
    'Story_Points_Completed',
    'Tasks_Completed',
    'Deadline_Missed',
    'Attendance_Percentage',
    'Overtime_Hours',
    'Code_Review_Score',
    'Team_Feedback_Score',
    'Training_Completed'
]

X = df[features]  # Features (input)
y = df['Performance_Category']  # Target (output to predict)

# ============================================
# Label Encoding for Target Variable
# ============================================
le = LabelEncoder()
y_encoded = le.fit_transform(y)

print(f"✅ Selected {len(features)} features")
print(f"   Features: {', '.join(features)}")

# ============================================
# STEP 3: Split Data into Training & Testing
# ============================================
print("\n📊 Splitting data into training (80%) and testing (20%)...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, 
    test_size=0.2,  # 20% for testing
    random_state=42,
    stratify=y_encoded  # Keep class balance
)

print(f"✅ Training set: {len(X_train)} samples")
print(f"✅ Testing set: {len(X_test)} samples")

# ============================================
# STEP 4: Feature Scaling
# ============================================
print("\n⚖️ Scaling features (normalizing values)...")

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("✅ Features scaled successfully")

# ============================================
# STEP 5: Train Multiple Models
# ============================================
print("\n" + "=" * 60)
print("🚀 TRAINING MODELS")
print("=" * 60)

models = {}

# Model 1: Logistic Regression
print("\n1️⃣ Training Logistic Regression...")
lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train_scaled, y_train)
models['Logistic Regression'] = (lr_model, X_train_scaled, X_test_scaled, scaler)
print("✅ Logistic Regression trained")

# Model 2: Decision Tree
print("\n2️⃣ Training Decision Tree...")
dt_model = DecisionTreeClassifier(max_depth=10, random_state=42)
dt_model.fit(X_train, y_train)
models['Decision Tree'] = (dt_model, X_train, X_test, None)
print("✅ Decision Tree trained")

# Model 3: Random Forest (Usually best for this type of data)
print("\n3️⃣ Training Random Forest...")
rf_model = RandomForestClassifier(
    n_estimators=100,  # 100 trees
    max_depth=15,
    random_state=42,
    n_jobs=-1  # Use all CPU cores
)
rf_model.fit(X_train, y_train)
models['Random Forest'] = (rf_model, X_train, X_test, None)
print("✅ Random Forest trained")

# Model 4: XGBoost (Advanced gradient boosting)
print("\n4️⃣ Training XGBoost...")
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=7,
    learning_rate=0.1,
    random_state=42,
    verbosity=0
)
xgb_model.fit(X_train, y_train)
models['XGBoost'] = (xgb_model, X_train, X_test, None)
print("✅ XGBoost trained")

# ============================================
# STEP 6: Evaluate Models
# ============================================
print("\n" + "=" * 60)
print("📊 MODEL EVALUATION")
print("=" * 60)

results = {}

for model_name, (model, X_tr, X_te, scale) in models.items():
    print(f"\n{'=' * 60}")
    print(f"📈 {model_name}")
    print(f"{'=' * 60}")
    
    # Make predictions
    y_pred = model.predict(X_te)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # Store results
    results[model_name] = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'model': model,
        'predictions': y_pred
    }
    
    # Print metrics
    print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    
    # Show classification report
    print(f"\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred))

# ============================================
# STEP 7: Select Best Model
# ============================================
print("\n" + "=" * 60)
print("🏆 BEST MODEL SELECTION")
print("=" * 60)

best_model_name = max(results, key=lambda x: results[x]['f1'])
best_model_obj = models[best_model_name][0]

print(f"\n🥇 Best Model: {best_model_name}")
print(f"   F1-Score: {results[best_model_name]['f1']:.4f}")
print(f"   Accuracy: {results[best_model_name]['accuracy']:.4f}")

# ============================================
# STEP 8: Feature Importance (for tree-based models)
# ============================================
if best_model_name in ['Random Forest', 'XGBoost', 'Decision Tree']:
    print(f"\n📊 Top 10 Most Important Features ({best_model_name}):")
    
    feature_importance = pd.DataFrame({
        'Feature': features,
        'Importance': best_model_obj.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    for idx, row in feature_importance.head(10).iterrows():
        bar = "█" * int(row['Importance'] * 50)
        print(f"   {row['Feature']:<30} {bar} {row['Importance']:.4f}")

# ============================================
# STEP 9: Save Model & Scaler
# ============================================
print("\n" + "=" * 60)
print("💾 SAVING MODELS")
print("=" * 60)

# Save best model
joblib.dump(best_model_obj, 'best_model.pkl')
print(f"✅ Saved best model: {best_model_name} -> best_model.pkl")

# Save scaler if used
if models[best_model_name][3] is not None:
    joblib.dump(models[best_model_name][3], 'scaler.pkl')
    print("✅ Saved scaler -> scaler.pkl")

# Save feature names
joblib.dump(features, 'features.pkl')
print("✅ Saved feature names -> features.pkl")

# Save scaler for all models
joblib.dump(scaler, 'scaler_universal.pkl')
print("✅ Saved universal scaler -> scaler_universal.pkl")

print("\n" + "=" * 60)
print("✨ MODEL TRAINING COMPLETE!")
print("=" * 60)
print("\n📁 Generated files:")
print("   - best_model.pkl (trained model)")
print("   - features.pkl (feature names)")
print("   - scaler_universal.pkl (for feature scaling)")
print("   - developer_data.csv (original dataset)")
print("\nNext step: Run app.py for interactive predictions!")
