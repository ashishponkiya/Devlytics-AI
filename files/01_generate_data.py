"""
STEP 1: Data Generation Script
Generates synthetic developer performance data for training the ML model

This script creates a dataset with developer metrics that you would collect from:
- Git repositories (commits, PRs)
- Project management tools (story points, tasks)
- Code review tools (PR acceptance rate)
- HR systems (attendance, training)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Number of developers to generate data for
num_developers = 150

print("🚀 Generating synthetic developer data...\n")

# ============================================
# FEATURE 1: Basic Information
# ============================================
developer_ids = [f"DEV_{str(i).zfill(4)}" for i in range(1, num_developers + 1)]
years_experience = np.random.uniform(1, 15, num_developers)  # 1-15 years

# ============================================
# FEATURE 2: Coding Activity (Git metrics)
# ============================================
git_commits_per_month = np.random.randint(10, 200, num_developers)
pull_requests = np.random.randint(5, 50, num_developers)
pr_acceptance_rate = np.random.uniform(60, 100, num_developers)  # 60-100% of PRs merged

# ============================================
# FEATURE 3: Quality & Bug Metrics
# ============================================
bugs_fixed = np.random.randint(5, 100, num_developers)
bugs_introduced = np.random.randint(0, 30, num_developers)
unit_test_coverage = np.random.uniform(40, 95, num_developers)  # 40-95% coverage

# ============================================
# FEATURE 4: Productivity Metrics
# ============================================
story_points_completed = np.random.randint(20, 200, num_developers)
tasks_completed = np.random.randint(10, 100, num_developers)
deadline_missed = np.random.randint(0, 10, num_developers)

# ============================================
# FEATURE 5: Behavioral Metrics
# ============================================
attendance_percentage = np.random.uniform(80, 100, num_developers)  # 80-100% attendance
overtime_hours = np.random.uniform(0, 50, num_developers)  # 0-50 hours per month
code_review_score = np.random.uniform(1, 10, num_developers)  # 1-10 rating
team_feedback_score = np.random.uniform(1, 10, num_developers)  # 1-10 rating
training_completed = np.random.randint(0, 12, num_developers)  # 0-12 courses per year

# ============================================
# TARGET VARIABLE: Create Performance Rating
# ============================================
# Let's create a performance rating based on a combination of features
# (In real world, this would be manager's rating)

def calculate_performance_rating(
    commits, prs, pr_rate, bugs_fixed, bugs_intro, 
    coverage, points, tasks, missed, attendance, 
    review_score, team_score, experience
):
    """
    Simple scoring function to create performance ratings
    This mimics how a manager might rate someone
    """
    # Start with base score
    score = 0
    
    # Higher commits = better (but not too high, means efficiency matters)
    score += (commits / 20) * 1.5
    
    # Higher PR acceptance rate = better quality
    score += (pr_rate / 100) * 2
    
    # Fix more bugs = better
    score += (bugs_fixed / 20) * 1.5
    
    # Introduce fewer bugs = better
    score += ((30 - bugs_intro) / 30) * 2
    
    # Higher test coverage = better
    score += (coverage / 100) * 2
    
    # Complete more tasks = better
    score += (tasks / 50) * 1.5
    
    # Fewer missed deadlines = better
    score += ((10 - missed) / 10) * 2
    
    # Higher attendance = better
    score += (attendance / 100) * 1.5
    
    # Better peer reviews = better
    score += (review_score / 10) * 1.5
    
    # Better team feedback = better
    score += (team_score / 10) * 1.5
    
    # More experience = slight boost
    score += (experience / 15) * 1
    
    # Add some randomness (real world isn't perfectly predictable)
    score += np.random.normal(0, 0.5)
    
    return score

# Calculate performance scores for each developer
performance_scores = []
for i in range(num_developers):
    score = calculate_performance_rating(
        git_commits_per_month[i],
        pull_requests[i],
        pr_acceptance_rate[i],
        bugs_fixed[i],
        bugs_introduced[i],
        unit_test_coverage[i],
        story_points_completed[i],
        tasks_completed[i],
        deadline_missed[i],
        attendance_percentage[i],
        code_review_score[i],
        team_feedback_score[i],
        years_experience[i]
    )
    performance_scores.append(score)

# Convert scores to ratings (1-5 scale)
performance_scores = np.array(performance_scores)
performance_scores = (performance_scores - performance_scores.min()) / (performance_scores.max() - performance_scores.min())
performance_rating = (performance_scores * 4) + 1  # Scale to 1-5

# Create categorical labels for performance
def score_to_category(rating):
    """Convert numeric rating to category"""
    if rating >= 4.5:
        return "Excellent"
    elif rating >= 3.5:
        return "Good"
    elif rating >= 2.5:
        return "Average"
    else:
        return "Poor"

performance_category = [score_to_category(score) for score in performance_rating]

# ============================================
# Create DataFrame
# ============================================
data = {
    'Developer_ID': developer_ids,
    'Years_Experience': years_experience,
    'Git_Commits_Per_Month': git_commits_per_month,
    'Pull_Requests': pull_requests,
    'PR_Acceptance_Rate': pr_acceptance_rate,
    'Bugs_Fixed': bugs_fixed,
    'Bugs_Introduced': bugs_introduced,
    'Unit_Test_Coverage': unit_test_coverage,
    'Story_Points_Completed': story_points_completed,
    'Tasks_Completed': tasks_completed,
    'Deadline_Missed': deadline_missed,
    'Attendance_Percentage': attendance_percentage,
    'Overtime_Hours': overtime_hours,
    'Code_Review_Score': code_review_score,
    'Team_Feedback_Score': team_feedback_score,
    'Training_Completed': training_completed,
    'Performance_Rating': performance_rating,
    'Performance_Category': performance_category
}

df = pd.DataFrame(data)

# ============================================
# Save Dataset
# ============================================
df.to_csv('developer_data.csv', index=False)

print("✅ Data generated successfully!\n")
print(f"📊 Dataset shape: {df.shape}")
print(f"📁 Saved to: developer_data.csv\n")

# ============================================
# Show Sample Data
# ============================================
print("📈 Sample of generated data:\n")
print(df.head(10))

print("\n📊 Dataset Statistics:\n")
print(df.describe())

print("\n📊 Performance Category Distribution:\n")
print(df['Performance_Category'].value_counts())

print("\n✅ Data generation complete! Ready for training.")
