"""
BONUS: Using the Trained Model Programmatically

This script shows how to:
1. Load the trained model
2. Make predictions without Streamlit
3. Get detailed information about predictions
4. Use the model in your own Python code

Run with: python predict_example.py
"""

import joblib
import pandas as pd
import numpy as np

print("=" * 70)
print("🤖 USING THE TRAINED MODEL - PROGRAMMATIC APPROACH")
print("=" * 70)

# ============================================
# STEP 1: Load the Trained Model
# ============================================
print("\n📂 Loading trained model...")

try:
    model = joblib.load('best_model.pkl')
    scaler = joblib.load('scaler_universal.pkl')
    features = joblib.load('features.pkl')
    print("✅ Model loaded successfully!")
    print(f"   Model type: {type(model).__name__}")
    print(f"   Number of features: {len(features)}")
    print(f"   Classes: {model.classes_}")
except FileNotFoundError:
    print("❌ Model files not found!")
    print("   Run these first:")
    print("   1. python 01_generate_data.py")
    print("   2. python 02_train_model.py")
    exit()

# ============================================
# STEP 2: Prepare Input Data
# ============================================
print("\n" + "=" * 70)
print("📊 EXAMPLE DEVELOPERS")
print("=" * 70)

# Example 1: High Performer
print("\n🌟 Example 1: High Performer Developer")
print("-" * 70)

high_performer = {
    'Years_Experience': 8,
    'Git_Commits_Per_Month': 180,
    'Pull_Requests': 45,
    'PR_Acceptance_Rate': 92,
    'Bugs_Fixed': 65,
    'Bugs_Introduced': 3,
    'Unit_Test_Coverage': 88,
    'Story_Points_Completed': 150,
    'Tasks_Completed': 65,
    'Deadline_Missed': 0,
    'Attendance_Percentage': 98,
    'Overtime_Hours': 8,
    'Code_Review_Score': 9.2,
    'Team_Feedback_Score': 8.8,
    'Training_Completed': 7
}

# Convert to array
high_perf_array = np.array([[high_performer[f] for f in features]])

# Make prediction
prediction_hp = model.predict(high_perf_array)[0]
probabilities_hp = model.predict_proba(high_perf_array)[0]
confidence_hp = max(probabilities_hp)

print(f"Predicted Performance: {prediction_hp}")
print(f"Confidence: {confidence_hp * 100:.1f}%")

print("\nBreakdown by category:")
for class_name, prob in zip(model.classes_, probabilities_hp):
    bar = "█" * int(prob * 40)
    print(f"  {class_name:<12} {bar} {prob*100:5.1f}%")

# ============================================
# Example 2: Average Performer
# ============================================
print("\n\n⭐ Example 2: Average Developer")
print("-" * 70)

average_performer = {
    'Years_Experience': 3,
    'Git_Commits_Per_Month': 75,
    'Pull_Requests': 20,
    'PR_Acceptance_Rate': 70,
    'Bugs_Fixed': 25,
    'Bugs_Introduced': 8,
    'Unit_Test_Coverage': 55,
    'Story_Points_Completed': 65,
    'Tasks_Completed': 32,
    'Deadline_Missed': 2,
    'Attendance_Percentage': 92,
    'Overtime_Hours': 5,
    'Code_Review_Score': 6.5,
    'Team_Feedback_Score': 6.8,
    'Training_Completed': 2
}

avg_perf_array = np.array([[average_performer[f] for f in features]])

prediction_avg = model.predict(avg_perf_array)[0]
probabilities_avg = model.predict_proba(avg_perf_array)[0]
confidence_avg = max(probabilities_avg)

print(f"Predicted Performance: {prediction_avg}")
print(f"Confidence: {confidence_avg * 100:.1f}%")

print("\nBreakdown by category:")
for class_name, prob in zip(model.classes_, probabilities_avg):
    bar = "█" * int(prob * 40)
    print(f"  {class_name:<12} {bar} {prob*100:5.1f}%")

# ============================================
# Example 3: At-Risk Developer
# ============================================
print("\n\n⚠️ Example 3: Developer at Risk")
print("-" * 70)

at_risk_developer = {
    'Years_Experience': 2,
    'Git_Commits_Per_Month': 30,
    'Pull_Requests': 8,
    'PR_Acceptance_Rate': 50,
    'Bugs_Fixed': 10,
    'Bugs_Introduced': 15,
    'Unit_Test_Coverage': 25,
    'Story_Points_Completed': 35,
    'Tasks_Completed': 15,
    'Deadline_Missed': 6,
    'Attendance_Percentage': 80,
    'Overtime_Hours': 50,
    'Code_Review_Score': 4.2,
    'Team_Feedback_Score': 4.0,
    'Training_Completed': 0
}

risk_array = np.array([[at_risk_developer[f] for f in features]])

prediction_risk = model.predict(risk_array)[0]
probabilities_risk = model.predict_proba(risk_array)[0]
confidence_risk = max(probabilities_risk)

print(f"Predicted Performance: {prediction_risk}")
print(f"Confidence: {confidence_risk * 100:.1f}%")

print("\nBreakdown by category:")
for class_name, prob in zip(model.classes_, probabilities_risk):
    bar = "█" * int(prob * 40)
    print(f"  {class_name:<12} {bar} {prob*100:5.1f}%")

# ============================================
# BONUS: Batch Prediction
# ============================================
print("\n" + "=" * 70)
print("🚀 BATCH PREDICTION - PREDICTING MULTIPLE DEVELOPERS")
print("=" * 70)

# Create a DataFrame with all three examples
batch_data = pd.DataFrame([high_performer, average_performer, at_risk_developer])
developer_names = ['Alice (High Performer)', 'Bob (Average)', 'Charlie (At Risk)']

batch_predictions = model.predict(batch_data[features])
batch_probabilities = model.predict_proba(batch_data[features])

print("\nBatch Predictions:\n")
for i, (name, pred, probs) in enumerate(zip(developer_names, batch_predictions, batch_probabilities)):
    confidence = max(probs)
    print(f"{i+1}. {name}")
    print(f"   Predicted: {pred} (Confidence: {confidence*100:.1f}%)")
    print()

# ============================================
# HOW TO USE IN YOUR OWN CODE
# ============================================
print("=" * 70)
print("💡 HOW TO USE IN YOUR CODE")
print("=" * 70)

code_example = """
# 1. Load the model (do this once at startup)
import joblib
model = joblib.load('best_model.pkl')
features = joblib.load('features.pkl')

# 2. Prepare your data as a dictionary
developer_metrics = {
    'Years_Experience': 5,
    'Git_Commits_Per_Month': 100,
    'Pull_Requests': 25,
    'PR_Acceptance_Rate': 85,
    'Bugs_Fixed': 40,
    'Bugs_Introduced': 5,
    'Unit_Test_Coverage': 80,
    'Story_Points_Completed': 100,
    'Tasks_Completed': 50,
    'Deadline_Missed': 1,
    'Attendance_Percentage': 95,
    'Overtime_Hours': 10,
    'Code_Review_Score': 8.0,
    'Team_Feedback_Score': 7.5,
    'Training_Completed': 4
}

# 3. Convert to array
import numpy as np
input_array = np.array([[developer_metrics[f] for f in features]])

# 4. Make prediction
performance = model.predict(input_array)[0]
probabilities = model.predict_proba(input_array)[0]

# 5. Use the result
print(f"Performance: {performance}")
print(f"Confidence: {max(probabilities) * 100:.1f}%")
"""

print(code_example)

# ============================================
# MODEL INFORMATION
# ============================================
print("\n" + "=" * 70)
print("ℹ️ MODEL INFORMATION")
print("=" * 70)

print(f"\nModel Type: {type(model).__name__}")
print(f"Number of Features: {len(features)}")
print(f"Feature Names:")
for i, feature in enumerate(features, 1):
    print(f"  {i:2d}. {feature}")

print(f"\nPredictable Classes:")
for i, cls in enumerate(model.classes_, 1):
    print(f"  {i}. {cls}")

# Try to get feature importances if available
if hasattr(model, 'feature_importances_'):
    print(f"\nTop 5 Most Important Features:")
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'Feature': features,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    for idx, (_, row) in enumerate(feature_importance_df.head(5).iterrows(), 1):
        bar = "█" * int(row['Importance'] * 50)
        print(f"  {idx}. {row['Feature']:<35} {bar} {row['Importance']:.4f}")

print("\n" + "=" * 70)
print("✅ Model is ready to use!")
print("=" * 70)
