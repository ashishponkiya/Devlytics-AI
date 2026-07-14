"""
STEP 3: Streamlit Interactive Dashboard
Provides a web interface for:
1. Making predictions for new developers
2. Viewing analytics and dashboards
3. Comparing developers
4. Understanding model predictions

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
import plotly.express as px
from sklearn.preprocessing import StandardScaler
import os
import warnings
warnings.filterwarnings('ignore')

# Base directory (where this script lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Developer Performance AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# LOAD MODEL & DATA
# ============================================
@st.cache_resource
def load_model():
    """Load trained model, scaler, and features"""
    try:
        model = joblib.load(os.path.join(BASE_DIR, 'best_model.pkl'))
        scaler = joblib.load(os.path.join(BASE_DIR, 'scaler_universal.pkl'))
        features = joblib.load(os.path.join(BASE_DIR, 'features.pkl'))
        return model, scaler, features
    except FileNotFoundError:
        st.error("⚠️ Model files not found! Run 01_generate_data.py and 02_train_model.py first.")
        return None, None, None

@st.cache_data
def load_data():
    """Load original dataset"""
    try:
        return pd.read_csv(os.path.join(BASE_DIR, 'developer_data.csv'))
    except FileNotFoundError:
        return None

# Load everything
model, scaler, features = load_model()
df = load_data()

# ============================================
# SIDEBAR NAVIGATION
# ============================================
st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio(
    "Choose a page:",
    ["🏠 Home", "🔮 Make Prediction", "📊 Analytics", "👥 Developer Insights", "❓ How It Works"]
)

# ============================================
# HOME PAGE
# ============================================
if page == "🏠 Home":
    st.title("🚀 Developer Performance AI System")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 What is this?
        
        An AI-powered system that predicts **developer performance** based on:
        - 💻 Code metrics (commits, PRs, test coverage)
        - 🐛 Quality metrics (bugs fixed/introduced)
        - 📊 Productivity metrics (tasks, story points)
        - 👥 Team & behavioral metrics
        
        ### 🔥 Features
        - ✅ Predict performance ratings (Excellent/Good/Average/Poor)
        - ✅ Analyze team productivity
        - ✅ Identify top performers
        - ✅ Detect burnout risks
        """)
    
    with col2:
        st.markdown("""
        ### 📈 Quick Stats
        """)
        
        if df is not None:
            col_a, col_b, col_c, col_d = st.columns(4)
            
            with col_a:
                st.metric("Total Developers", len(df))
            
            with col_b:
                excellent = len(df[df['Performance_Category'] == 'Excellent'])
                st.metric("Excellent Performers", excellent)
            
            with col_c:
                avg_commits = df['Git_Commits_Per_Month'].mean()
                st.metric("Avg Commits/Month", f"{avg_commits:.0f}")
            
            with col_d:
                avg_rating = df['Performance_Rating'].mean()
                st.metric("Avg Performance", f"{avg_rating:.2f}/5")

# ============================================
# PREDICTION PAGE
# ============================================
elif page == "🔮 Make Prediction":
    st.title("🔮 Predict Developer Performance")
    
    st.markdown("""
    Enter developer metrics below to predict their performance rating.
    """)
    
    # Create input form
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📊 Experience & Activity")
        years_exp = st.slider("Years of Experience", 0.0, 20.0, 5.0)
        git_commits = st.number_input("Git Commits/Month", 0, 300, 50)
        pull_requests = st.number_input("Pull Requests", 0, 100, 15)
    
    with col2:
        st.subheader("🐛 Quality Metrics")
        pr_rate = st.slider("PR Acceptance Rate (%)", 0, 100, 80)
        bugs_fixed = st.number_input("Bugs Fixed", 0, 200, 30)
        bugs_intro = st.number_input("Bugs Introduced", 0, 50, 5)
        test_coverage = st.slider("Unit Test Coverage (%)", 0, 100, 75)
    
    with col3:
        st.subheader("✅ Productivity")
        story_points = st.number_input("Story Points Completed", 0, 500, 80)
        tasks = st.number_input("Tasks Completed", 0, 200, 40)
        deadline_miss = st.number_input("Deadlines Missed", 0, 20, 1)
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.subheader("👥 Behavior")
        attendance = st.slider("Attendance (%)", 0, 100, 95)
        overtime = st.slider("Overtime Hours/Month", 0.0, 100.0, 10.0)
    
    with col5:
        st.subheader("📈 Feedback")
        code_review = st.slider("Code Review Score (1-10)", 1.0, 10.0, 7.0)
        team_score = st.slider("Team Feedback Score (1-10)", 1.0, 10.0, 7.0)
    
    with col6:
        st.subheader("🎓 Learning")
        training = st.number_input("Training Courses Completed", 0, 20, 3)
    
    # ============================================
    # MAKE PREDICTION
    # ============================================
    if st.button("🎯 Predict Performance", key="predict", use_container_width=True):
        
        # Prepare input data
        input_data = np.array([[
            years_exp,
            git_commits,
            pull_requests,
            pr_rate,
            bugs_fixed,
            bugs_intro,
            test_coverage,
            story_points,
            tasks,
            deadline_miss,
            attendance,
            overtime,
            code_review,
            team_score,
            training
        ]])
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        
        # Display results
        st.success("✅ Prediction Complete!")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Determine color
            if prediction == "Excellent":
                color = "🟢"
            elif prediction == "Good":
                color = "🔵"
            elif prediction == "Average":
                color = "🟡"
            else:
                color = "🔴"
            
            st.metric("Predicted Performance", f"{color} {prediction}")
        
        with col2:
            # Show probability distribution
            class_names = model.classes_
            fig = go.Figure(data=[
                go.Bar(x=class_names, y=probabilities,
                       marker_color=['#00ff00', '#0080ff', '#ffcc00', '#ff4444'],
                       text=[f"{p*100:.1f}%" for p in probabilities],
                       textposition='outside')
            ])
            fig.update_layout(
                title="Confidence Scores",
                xaxis_title="Performance Category",
                yaxis_title="Probability",
                height=300,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Key insights
        st.markdown("### 💡 Key Insights")
        
        insights = []
        
        if git_commits > 150:
            insights.append("✅ High coding activity - great contribution rate")
        elif git_commits < 30:
            insights.append("⚠️ Low commit frequency - consider checking engagement")
        
        if pr_rate > 90:
            insights.append("✅ Excellent PR quality - high acceptance rate")
        
        if test_coverage > 80:
            insights.append("✅ Strong test coverage - good code quality")
        elif test_coverage < 50:
            insights.append("⚠️ Low test coverage - consider writing more unit tests")
        
        if bugs_intro < 5:
            insights.append("✅ Very few bugs introduced - excellent quality")
        elif bugs_intro > 15:
            insights.append("⚠️ High bug introduction - may need code review focus")
        
        if deadline_miss == 0:
            insights.append("✅ All deadlines met - reliable team member")
        elif deadline_miss > 3:
            insights.append("⚠️ Multiple missed deadlines - workload review needed")
        
        if attendance < 90:
            insights.append("⚠️ Attendance below expected - check employee wellbeing")
        
        if overtime > 40:
            insights.append("🔴 High overtime - risk of burnout, consider workload adjustment")
        
        if not insights:
            insights.append("✅ Developer metrics look good overall")
        
        for insight in insights:
            st.write(insight)

# ============================================
# ANALYTICS PAGE
# ============================================
elif page == "📊 Analytics":
    st.title("📊 Developer Analytics Dashboard")
    
    if df is not None:
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_rating = df['Performance_Rating'].mean()
            st.metric("Average Performance Rating", f"{avg_rating:.2f}/5.0")
        
        with col2:
            excellent_pct = (len(df[df['Performance_Category'] == 'Excellent']) / len(df)) * 100
            st.metric("Excellent Performers", f"{excellent_pct:.1f}%")
        
        with col3:
            avg_experience = df['Years_Experience'].mean()
            st.metric("Average Experience", f"{avg_experience:.1f} years")
        
        with col4:
            high_risk = len(df[df['Overtime_Hours'] > 40])
            st.metric("Burnout Risk (High Overtime)", high_risk)
        
        # Charts
        col1, col2 = st.columns(2)
        
        # Performance Distribution
        with col1:
            fig = px.pie(
                df,
                names='Performance_Category',
                title='Performance Distribution',
                color_discrete_map={
                    'Excellent': '#00ff00',
                    'Good': '#0080ff',
                    'Average': '#ffcc00',
                    'Poor': '#ff4444'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Performance by Experience
        with col2:
            fig = px.scatter(
                df,
                x='Years_Experience',
                y='Performance_Rating',
                color='Performance_Category',
                title='Performance vs Experience'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # More detailed charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(
                df,
                x='Git_Commits_Per_Month',
                y='Bugs_Introduced',
                size='Performance_Rating',
                color='Performance_Category',
                title='Commits vs Bug Introduction',
                hover_data=['Developer_ID']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(
                df,
                x='Unit_Test_Coverage',
                y='Performance_Rating',
                color='Team_Feedback_Score',
                title='Test Coverage vs Performance',
                size='Story_Points_Completed'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Correlation heatmap
        st.subheader("🔗 Feature Correlation")
        
        correlation_features = [
            'Performance_Rating', 'Years_Experience', 'Git_Commits_Per_Month',
            'PR_Acceptance_Rate', 'Bugs_Fixed', 'Unit_Test_Coverage',
            'Story_Points_Completed', 'Attendance_Percentage'
        ]
        
        corr_matrix = df[correlation_features].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=correlation_features,
            y=correlation_features,
            colorscale='RdBu'
        ))
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# DEVELOPER INSIGHTS PAGE
# ============================================
elif page == "👥 Developer Insights":
    st.title("👥 Developer Insights & Comparisons")
    
    if df is not None:
        # Sort developers by performance
        df_sorted = df.sort_values('Performance_Rating', ascending=False)
        
        # Top performers
        st.subheader("🌟 Top 10 Performers")
        top_10 = df_sorted.head(10)[['Developer_ID', 'Performance_Rating', 'Performance_Category', 'Git_Commits_Per_Month', 'Team_Feedback_Score']]
        st.dataframe(top_10, use_container_width=True)
        
        # Developers needing support
        st.subheader("⚠️ Developers Needing Support")
        bottom_10 = df_sorted.tail(10)[['Developer_ID', 'Performance_Rating', 'Performance_Category', 'Deadline_Missed', 'Overtime_Hours']]
        st.dataframe(bottom_10, use_container_width=True)
        
        # Burnout risk
        st.subheader("🔴 Burnout Risk Analysis")
        high_risk = df[df['Overtime_Hours'] > 40].sort_values('Overtime_Hours', ascending=False)
        if len(high_risk) > 0:
            st.dataframe(high_risk[['Developer_ID', 'Overtime_Hours', 'Attendance_Percentage', 'Performance_Rating']], use_container_width=True)
        else:
            st.info("No developers at high burnout risk")
        
        # Developer search
        st.subheader("🔍 Search Developer")
        dev_id = st.selectbox("Select a developer:", df['Developer_ID'].unique())
        
        if dev_id:
            dev_data = df[df['Developer_ID'] == dev_id].iloc[0]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Performance Rating", f"{dev_data['Performance_Rating']:.2f}/5")
            with col2:
                st.metric("Years Experience", f"{dev_data['Years_Experience']:.1f}")
            with col3:
                st.metric("Team Feedback", f"{dev_data['Team_Feedback_Score']:.1f}/10")
            with col4:
                st.metric("Test Coverage", f"{dev_data['Unit_Test_Coverage']:.1f}%")
            
            # Detailed metrics
            metrics = {
                'Git Commits/Month': dev_data['Git_Commits_Per_Month'],
                'Pull Requests': dev_data['Pull_Requests'],
                'Bugs Fixed': dev_data['Bugs_Fixed'],
                'Bugs Introduced': dev_data['Bugs_Introduced'],
                'Story Points': dev_data['Story_Points_Completed'],
                'Tasks Completed': dev_data['Tasks_Completed'],
                'Deadlines Missed': dev_data['Deadline_Missed'],
                'Overtime Hours': dev_data['Overtime_Hours'],
                'Training Completed': dev_data['Training_Completed']
            }
            
            fig = go.Figure(data=[go.Bar(x=list(metrics.keys()), y=list(metrics.values()))])
            fig.update_layout(title=f"Detailed Metrics - {dev_id}", height=400)
            st.plotly_chart(fig, use_container_width=True)

# ============================================
# HOW IT WORKS PAGE
# ============================================
elif page == "❓ How It Works":
    st.title("❓ How This AI System Works")
    
    st.markdown("""
    ### 🔬 Machine Learning Process
    
    #### 1️⃣ Data Collection
    - Developer metrics are collected from various sources
    - Git repositories, project management tools, HR systems
    - 150+ developers in training dataset
    
    #### 2️⃣ Feature Selection
    - **15 key features** are used for prediction
    - Examples: commits, PR rate, bug metrics, test coverage
    
    #### 3️⃣ Model Training
    - Multiple ML algorithms are trained:
      - Logistic Regression
      - Decision Trees
      - Random Forest (Usually best)
      - XGBoost (Advanced)
    
    #### 4️⃣ Performance Evaluation
    - Models are tested on unseen data
    - Best model is selected based on F1-score
    
    #### 5️⃣ Prediction
    - New developer data → Model → Performance Rating
    - Model provides confidence scores for each category
    
    ### 📊 Features Used
    
    | Category | Features |
    |----------|----------|
    | **Experience** | Years of experience |
    | **Coding** | Commits, PRs, PR acceptance rate |
    | **Quality** | Bugs fixed/introduced, test coverage |
    | **Productivity** | Story points, tasks, missed deadlines |
    | **Behavior** | Attendance, overtime, feedback scores |
    | **Learning** | Training courses completed |
    
    ### 🎯 Output: Performance Categories
    
    - **🟢 Excellent** (4.5-5.0): Top performer, exceeds expectations
    - **🔵 Good** (3.5-4.5): Meets expectations, reliable
    - **🟡 Average** (2.5-3.5): Meets basic requirements
    - **🔴 Poor** (1.0-2.5): Below expectations, needs support
    
    ### 🔒 Important Notes
    
    ⚠️ **This is a predictive tool**, not a replacement for human judgment
    
    - Helps identify trends and patterns
    - Supports HR and management decisions
    - Should be used alongside qualitative feedback
    - Predictions have confidence scores
    
    ### 💡 Use Cases
    
    ✅ Identify top performers for promotion  
    ✅ Detect developers needing additional training  
    ✅ Predict burnout and prevent attrition  
    ✅ Plan team capacity and workload  
    ✅ Benchmark team productivity  
    """)

# Footer
st.markdown("---")
st.markdown("🚀 **Developer Performance AI System** | Built with Streamlit & Machine Learning")
