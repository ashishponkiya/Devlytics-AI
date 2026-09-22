"""
Devlytics AI - Developer Performance Intelligence Platform
===========================================================
Features:
  - GitHub OAuth & demo authentication
  - Role-based access: Admin, Manager, Developer
  - Predictive analytics for developer performance
  - Team and individual insights

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

# Local modules
from auth import login_page, is_authenticated, get_current_user, logout, handle_github_callback, is_github_oauth_configured
from database import (
    get_all_users, get_all_demo_users, get_team_members,
    update_user_role, update_user_team, update_user_developer_id,
    update_demo_user_role, update_demo_user_team, update_demo_user_developer_id,
    delete_user, get_all_teams, init_db
)

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Devlytics AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global styles
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="st-"] {
    font-family: 'Inter', sans-serif;
}

.user-card {
    background: linear-gradient(135deg, #1a1a2e, #16213e);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.25rem;
    margin-bottom: 1rem;
    text-align: center;
}
.user-avatar {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    border: 2px solid rgba(123,47,247,0.5);
    margin: 0 auto 0.6rem;
    display: block;
}
.user-name {
    color: #ccd6f6;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 0.25rem;
}
.user-role {
    display: inline-block;
    padding: 3px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.role-admin { background: rgba(255,107,107,0.18); color: #ff6b6b; }
.role-manager { background: rgba(0,210,255,0.18); color: #00d2ff; }
.role-developer { background: rgba(123,47,247,0.18); color: #b57bff; }

.team-badge {
    color: #5a6577;
    font-size: 0.8rem;
    margin-top: 0.3rem;
}

.access-denied {
    text-align: center;
    padding: 3rem;
    color: #ff6b6b;
    font-family: 'Inter', sans-serif;
}
.access-denied h2 { color: #ff6b6b; }
.access-denied p { color: #8892b0; }

.mgmt-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1rem;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Initialize database
init_db()

# ============================================
# AUTHENTICATION CHECK
# ============================================

# Handle GitHub OAuth callback
if is_github_oauth_configured():
    handle_github_callback()

if not is_authenticated():
    login_page()
    st.stop()

# Get current user
user = get_current_user()
user_role = user.get('role', 'developer')
user_name = user.get('name', user.get('username', 'User'))
user_team = user.get('team', 'Unassigned')
user_avatar = user.get('avatar_url', '')
user_dev_id = user.get('developer_id', None)
auth_method = st.session_state.get('auth_method', 'demo')


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


model, scaler, features = load_model()
df = load_data()


# ============================================
# HELPER: FILTER DATA BY ROLE
# ============================================
def get_filtered_data(dataframe):
    """Filter the dataset based on user role."""
    if dataframe is None:
        return None

    if user_role == 'admin':
        return dataframe

    if user_role == 'manager':
        # Get team members' developer IDs
        if auth_method == 'demo':
            team_users = get_all_demo_users()
        else:
            team_users = get_all_users()
        team_dev_ids = [
            u['developer_id'] for u in team_users
            if u.get('team') == user_team and u.get('developer_id')
        ]
        if team_dev_ids:
            return dataframe[dataframe['Developer_ID'].isin(team_dev_ids)]
        return dataframe  # Show all if no mapping exists yet

    if user_role == 'developer':
        if user_dev_id:
            return dataframe[dataframe['Developer_ID'] == user_dev_id]
        return dataframe.head(1)  # Show limited data if no mapping

    return dataframe


# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    # User card
    if user_avatar:
        st.markdown(f'''
        <div class="user-card">
            <img src="{user_avatar}" class="user-avatar" />
            <div class="user-name">{user_name}</div>
            <span class="user-role role-{user_role}">{user_role}</span>
            <div class="team-badge">📂 {user_team}</div>
        </div>
        ''', unsafe_allow_html=True)
    else:
        role_emoji = {'admin': '👑', 'manager': '📋', 'developer': '💻'}.get(user_role, '👤')
        st.markdown(f'''
        <div class="user-card">
            <div style="font-size:2.5rem; margin-bottom:0.5rem;">{role_emoji}</div>
            <div class="user-name">{user_name}</div>
            <span class="user-role role-{user_role}">{user_role}</span>
            <div class="team-badge">📂 {user_team}</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")

    # Role-based navigation
    if user_role == 'admin':
        pages = [
            "🏠 Home",
            "🔮 Make Prediction",
            "📊 Analytics",
            "👥 Developer Insights",
            "⚙️ User Management",
            "❓ How It Works"
        ]
    elif user_role == 'manager':
        pages = [
            "🏠 Home",
            "🔮 Make Prediction",
            "📊 Team Analytics",
            "👥 Team Insights",
            "❓ How It Works"
        ]
    else:  # developer
        pages = [
            "🏠 Home",
            "🔮 Make Prediction",
            "📊 My Performance",
            "❓ How It Works"
        ]

    page = st.radio("🧭 Navigation", pages, label_visibility="collapsed")

    st.markdown("---")

    if st.button("🚪 Logout", use_container_width=True):
        logout()


# ============================================
# HOME PAGE
# ============================================
if page == "🏠 Home":
    if user_role == 'admin':
        st.title("🚀 Devlytics AI — Admin Dashboard")
    elif user_role == 'manager':
        st.title(f"🚀 Devlytics AI — {user_team}")
    else:
        st.title(f"🚀 Welcome, {user_name}")

    filtered_df = get_filtered_data(df)

    col1, col2 = st.columns(2)

    with col1:
        if user_role == 'admin':
            st.markdown("""
            ### 👑 Admin Overview

            You have **full access** to the platform:
            - 🔮 Run predictions for **any developer**
            - 📊 View **all analytics** and dashboards
            - 👥 Manage **all developers** and teams
            - ⚙️ Control **user roles** and access
            """)
        elif user_role == 'manager':
            st.markdown(f"""
            ### 📋 Team Manager View

            You're managing **{user_team}**:
            - 🔮 Run predictions for **team members**
            - 📊 View **team analytics**
            - 👥 Monitor **team performance**
            """)
        else:
            st.markdown("""
            ### 💻 Developer View

            Your personal performance hub:
            - 🔮 Run **self-assessment** predictions
            - 📊 Track **your performance** metrics
            - 📈 Identify areas for **growth**
            """)

    with col2:
        st.markdown("### 📈 Quick Stats")
        if filtered_df is not None and len(filtered_df) > 0:
            col_a, col_b = st.columns(2)
            col_c, col_d = st.columns(2)

            with col_a:
                st.metric("Total Developers", len(filtered_df))
            with col_b:
                excellent = len(filtered_df[filtered_df['Performance_Category'] == 'Excellent'])
                st.metric("⭐ Excellent", excellent)
            with col_c:
                avg_commits = filtered_df['Git_Commits_Per_Month'].mean()
                st.metric("Avg Commits/Month", f"{avg_commits:.0f}")
            with col_d:
                avg_rating = filtered_df['Performance_Rating'].mean()
                st.metric("Avg Rating", f"{avg_rating:.2f}/5")
        else:
            st.info("No data available for your scope.")

    # Access summary for admins
    if user_role == 'admin':
        st.markdown("---")
        st.subheader("👥 Platform Users")
        if auth_method == 'demo':
            all_users = get_all_demo_users()
        else:
            all_users = get_all_users()

        col1, col2, col3 = st.columns(3)
        with col1:
            admins = len([u for u in all_users if u['role'] == 'admin'])
            st.metric("👑 Admins", admins)
        with col2:
            managers = len([u for u in all_users if u['role'] == 'manager'])
            st.metric("📋 Managers", managers)
        with col3:
            devs = len([u for u in all_users if u['role'] == 'developer'])
            st.metric("💻 Developers", devs)


# ============================================
# PREDICTION PAGE (All roles)
# ============================================
elif page == "🔮 Make Prediction":
    st.title("🔮 Predict Developer Performance")

    if user_role == 'developer':
        st.info("💡 Use this to **self-assess** and explore how metrics affect your rating.")
    elif user_role == 'manager':
        st.info("💡 Predict performance for your **team members** based on their metrics.")

    st.markdown("Enter developer metrics below to predict performance rating.")

    # Input form
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

    # Make prediction
    if st.button("🎯 Predict Performance", key="predict", use_container_width=True):
        if model is None:
            st.error("Model not loaded. Please ensure model files exist.")
        else:
            input_data = np.array([[
                years_exp, git_commits, pull_requests, pr_rate,
                bugs_fixed, bugs_intro, test_coverage, story_points,
                tasks, deadline_miss, attendance, overtime,
                code_review, team_score, training
            ]])

            prediction = model.predict(input_data)[0]
            probabilities = model.predict_proba(input_data)[0]

            st.success("✅ Prediction Complete!")

            col1, col2 = st.columns([1, 2])

            with col1:
                colors = {"Excellent": "🟢", "Good": "🔵", "Average": "🟡", "Poor": "🔴"}
                color = colors.get(prediction, "⚪")
                st.metric("Predicted Performance", f"{color} {prediction}")

            with col2:
                class_names = model.classes_
                fig = go.Figure(data=[
                    go.Bar(
                        x=class_names, y=probabilities,
                        marker_color=['#00ff00', '#0080ff', '#ffcc00', '#ff4444'],
                        text=[f"{p*100:.1f}%" for p in probabilities],
                        textposition='outside'
                    )
                ])
                fig.update_layout(
                    title="Confidence Scores",
                    xaxis_title="Performance Category",
                    yaxis_title="Probability",
                    height=300,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)

            # Insights
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
# ANALYTICS PAGE (Admin: all | Manager: team | Dev: personal)
# ============================================
elif page in ["📊 Analytics", "📊 Team Analytics", "📊 My Performance"]:
    if user_role == 'admin':
        st.title("📊 Developer Analytics Dashboard")
    elif user_role == 'manager':
        st.title(f"📊 {user_team} — Team Analytics")
    else:
        st.title("📊 My Performance")

    filtered_df = get_filtered_data(df)

    if filtered_df is not None and len(filtered_df) > 0:
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            avg_rating = filtered_df['Performance_Rating'].mean()
            st.metric("Average Performance", f"{avg_rating:.2f}/5.0")
        with col2:
            excellent_pct = (len(filtered_df[filtered_df['Performance_Category'] == 'Excellent']) / len(filtered_df)) * 100
            st.metric("Excellent %", f"{excellent_pct:.1f}%")
        with col3:
            avg_experience = filtered_df['Years_Experience'].mean()
            st.metric("Avg Experience", f"{avg_experience:.1f} years")
        with col4:
            high_risk = len(filtered_df[filtered_df['Overtime_Hours'] > 40])
            st.metric("🔴 Burnout Risk", high_risk)

        # Charts
        col1, col2 = st.columns(2)

        with col1:
            fig = px.pie(
                filtered_df,
                names='Performance_Category',
                title='Performance Distribution',
                color_discrete_map={
                    'Excellent': '#00ff00', 'Good': '#0080ff',
                    'Average': '#ffcc00', 'Poor': '#ff4444'
                }
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.scatter(
                filtered_df,
                x='Years_Experience',
                y='Performance_Rating',
                color='Performance_Category',
                title='Performance vs Experience'
            )
            st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            fig = px.scatter(
                filtered_df,
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
                filtered_df,
                x='Unit_Test_Coverage',
                y='Performance_Rating',
                color='Team_Feedback_Score',
                title='Test Coverage vs Performance',
                size='Story_Points_Completed'
            )
            st.plotly_chart(fig, use_container_width=True)

        # Correlation heatmap (admin/manager only)
        if user_role in ['admin', 'manager']:
            st.subheader("🔗 Feature Correlation")
            correlation_features = [
                'Performance_Rating', 'Years_Experience', 'Git_Commits_Per_Month',
                'PR_Acceptance_Rate', 'Bugs_Fixed', 'Unit_Test_Coverage',
                'Story_Points_Completed', 'Attendance_Percentage'
            ]
            available = [f for f in correlation_features if f in filtered_df.columns]
            if len(available) >= 2:
                corr_matrix = filtered_df[available].corr()
                fig = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=available, y=available,
                    colorscale='RdBu'
                ))
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for your current scope.")


# ============================================
# DEVELOPER INSIGHTS (Admin: all | Manager: team)
# ============================================
elif page in ["👥 Developer Insights", "👥 Team Insights"]:
    if user_role == 'admin':
        st.title("👥 Developer Insights & Comparisons")
    else:
        st.title(f"👥 {user_team} — Team Insights")

    filtered_df = get_filtered_data(df)

    if filtered_df is not None and len(filtered_df) > 0:
        df_sorted = filtered_df.sort_values('Performance_Rating', ascending=False)

        # Top performers
        st.subheader("🌟 Top Performers")
        top_n = min(10, len(df_sorted))
        top_df = df_sorted.head(top_n)[['Developer_ID', 'Performance_Rating', 'Performance_Category', 'Git_Commits_Per_Month', 'Team_Feedback_Score']]
        st.dataframe(top_df, use_container_width=True)

        # Need support
        st.subheader("⚠️ Developers Needing Support")
        bottom_n = min(10, len(df_sorted))
        bottom_df = df_sorted.tail(bottom_n)[['Developer_ID', 'Performance_Rating', 'Performance_Category', 'Deadline_Missed', 'Overtime_Hours']]
        st.dataframe(bottom_df, use_container_width=True)

        # Burnout risk
        st.subheader("🔴 Burnout Risk Analysis")
        high_risk = filtered_df[filtered_df['Overtime_Hours'] > 40].sort_values('Overtime_Hours', ascending=False)
        if len(high_risk) > 0:
            st.dataframe(
                high_risk[['Developer_ID', 'Overtime_Hours', 'Attendance_Percentage', 'Performance_Rating']],
                use_container_width=True
            )
        else:
            st.success("✅ No developers at high burnout risk!")

        # Developer search
        st.subheader("🔍 Search Developer")
        dev_id = st.selectbox("Select a developer:", filtered_df['Developer_ID'].unique())

        if dev_id:
            dev_data = filtered_df[filtered_df['Developer_ID'] == dev_id].iloc[0]

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Performance", f"{dev_data['Performance_Rating']:.2f}/5")
            with col2:
                st.metric("Experience", f"{dev_data['Years_Experience']:.1f} yrs")
            with col3:
                st.metric("Team Feedback", f"{dev_data['Team_Feedback_Score']:.1f}/10")
            with col4:
                st.metric("Test Coverage", f"{dev_data['Unit_Test_Coverage']:.1f}%")

            metrics = {
                'Commits/Month': dev_data['Git_Commits_Per_Month'],
                'Pull Requests': dev_data['Pull_Requests'],
                'Bugs Fixed': dev_data['Bugs_Fixed'],
                'Bugs Introduced': dev_data['Bugs_Introduced'],
                'Story Points': dev_data['Story_Points_Completed'],
                'Tasks Done': dev_data['Tasks_Completed'],
                'Deadlines Missed': dev_data['Deadline_Missed'],
                'Overtime Hrs': dev_data['Overtime_Hours'],
                'Training': dev_data['Training_Completed']
            }
            fig = go.Figure(data=[go.Bar(x=list(metrics.keys()), y=list(metrics.values()))])
            fig.update_layout(title=f"Detailed Metrics — {dev_id}", height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No developer data available for your current scope.")


# ============================================
# USER MANAGEMENT (Admin only)
# ============================================
elif page == "⚙️ User Management":
    if user_role != 'admin':
        st.markdown("""
        <div class="access-denied">
            <h2>🔒 Access Denied</h2>
            <p>You need <strong>Admin</strong> privileges to access User Management.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    st.title("⚙️ User Management")

    # Get all users based on auth method
    if auth_method == 'demo':
        all_users = get_all_demo_users()
    else:
        all_users = get_all_users()

    # Summary
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Total Users", len(all_users))
    with col2:
        st.metric("👑 Admins", len([u for u in all_users if u['role'] == 'admin']))
    with col3:
        st.metric("📋 Managers", len([u for u in all_users if u['role'] == 'manager']))
    with col4:
        st.metric("💻 Developers", len([u for u in all_users if u['role'] == 'developer']))

    st.markdown("---")

    # Get developer IDs from data for mapping
    if df is not None:
        dev_ids = ['None'] + sorted(df['Developer_ID'].unique().tolist())
    else:
        dev_ids = ['None']

    # Available teams
    available_teams = ['Unassigned', 'Alpha Team', 'Beta Team', 'Gamma Team', 'Delta Team']

    # User management table
    st.subheader("📋 Manage Users")

    for u in all_users:
        user_identifier = u.get('github_username', u.get('username', 'Unknown'))
        display_name = u.get('name', user_identifier)
        current_role = u.get('role', 'developer')
        current_team = u.get('team', 'Unassigned')
        current_dev_id = u.get('developer_id', None) or 'None'

        with st.expander(f"{'👑' if current_role == 'admin' else '📋' if current_role == 'manager' else '💻'}  {display_name} — @{user_identifier}"):
            col_a, col_b, col_c = st.columns(3)

            with col_a:
                new_role = st.selectbox(
                    "Role",
                    ['admin', 'manager', 'developer'],
                    index=['admin', 'manager', 'developer'].index(current_role),
                    key=f"role_{u['id']}"
                )

            with col_b:
                current_team_safe = current_team if current_team in available_teams else 'Unassigned'
                new_team = st.selectbox(
                    "Team",
                    available_teams,
                    index=available_teams.index(current_team_safe),
                    key=f"team_{u['id']}"
                )

            with col_c:
                current_dev_id_safe = current_dev_id if current_dev_id in dev_ids else 'None'
                new_dev_id = st.selectbox(
                    "Linked Developer ID",
                    dev_ids,
                    index=dev_ids.index(current_dev_id_safe),
                    key=f"dev_{u['id']}"
                )

            col_save, col_spacer = st.columns([1, 3])
            with col_save:
                if st.button("💾 Save Changes", key=f"save_{u['id']}", use_container_width=True):
                    mapped_dev_id = None if new_dev_id == 'None' else new_dev_id
                    if auth_method == 'demo':
                        update_demo_user_role(u['id'], new_role)
                        update_demo_user_team(u['id'], new_team)
                        update_demo_user_developer_id(u['id'], mapped_dev_id)
                    else:
                        update_user_role(u['id'], new_role)
                        update_user_team(u['id'], new_team)
                        update_user_developer_id(u['id'], mapped_dev_id)

                    # Update session if editing own user
                    if u.get('username') == user.get('username') or u.get('github_username') == user.get('github_username'):
                        st.session_state['user']['role'] = new_role
                        st.session_state['user']['team'] = new_team
                        st.session_state['user']['developer_id'] = mapped_dev_id

                    st.success(f"✅ Updated {display_name}")
                    st.rerun()


# ============================================
# HOW IT WORKS PAGE (All roles)
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

    ### 🔐 Role-Based Access

    | Role | Access Level |
    |------|-------------|
    | **👑 Admin** | Full access, user management, all data |
    | **📋 Manager** | Team data, team predictions, team analytics |
    | **💻 Developer** | Personal data, self-assessment only |

    ### 🔒 Important Notes

    ⚠️ **This is a predictive tool**, not a replacement for human judgment

    - Helps identify trends and patterns
    - Supports HR and management decisions
    - Should be used alongside qualitative feedback
    - Predictions have confidence scores
    """)

# Footer
st.markdown("---")
col_f1, col_f2 = st.columns([3, 1])
with col_f1:
    st.markdown("🚀 **Devlytics AI** — Developer Performance Intelligence Platform")
with col_f2:
    st.caption(f"Logged in as **{user_name}** ({user_role})")
