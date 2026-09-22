<![CDATA[<div align="center">

# 🚀 Devlytics AI

### Developer Performance Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.26+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-189FDD?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**An end-to-end Machine Learning application for predictive analytics and developer performance evaluation — featuring a complete data pipeline, multi-algorithm model training, role-based access control, GitHub OAuth, and an interactive Streamlit dashboard.**

[Features](#-features) •
[Demo](#-demo-accounts) •
[Installation](#-installation) •
[Usage](#-usage) •
[Tech Stack](#-tech-stack) •
[Project Structure](#-project-structure)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [ML Pipeline](#-machine-learning-pipeline)
- [Authentication](#-authentication)
- [Role-Based Access Control](#-role-based-access-control)
- [Demo Accounts](#-demo-accounts)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

**Devlytics AI** is a full-stack machine learning platform that predicts and analyzes developer performance using 15 key metrics collected from Git repositories, project management tools, code review systems, and HR data.

The platform trains and compares **4 ML algorithms** (Logistic Regression, Decision Tree, Random Forest, XGBoost), selects the best-performing model, and deploys it through an interactive **Streamlit web dashboard** with real-time predictions, confidence scoring, and team analytics.

---

## ✨ Features

### 🤖 Machine Learning Engine
- **Multi-Algorithm Comparison** — Trains & evaluates Logistic Regression, Decision Tree, Random Forest, and XGBoost
- **Automated Model Selection** — Best model selected based on F1-Score
- **Real-Time Predictions** — Predict developer performance with confidence scores
- **Feature Importance Analysis** — Identifies top predictors (Git Commits, Bug Fixes, Experience)
- **86.67% Accuracy** — Achieved with XGBoost classifier on 150 developer records

### 📊 Analytics Dashboard
- **Performance Distribution** — Pie charts, scatter plots, and heatmaps
- **Burnout Risk Analysis** — Identifies developers with excessive overtime
- **Team Insights** — Top performers, developers needing support
- **Correlation Heatmap** — Understand relationships between metrics
- **Interactive Visualizations** — Built with Plotly Express

### 🔐 Authentication & Security
- **GitHub OAuth Integration** — Sign in with GitHub account
- **Demo Login System** — Pre-configured accounts for testing
- **Role-Based Access Control** — Admin, Manager, Developer roles
- **SQLite Database** — Persistent user management

### ⚙️ Admin Features
- **User Management Panel** — Assign roles, teams, and developer IDs
- **Full Platform Access** — View all analytics and manage all users
- **Team Configuration** — Create and manage development teams

---

## 🛠 Tech Stack

| Category | Technologies |
|---|---|
| **Language** | Python 3.11 |
| **Web Framework** | Streamlit 1.26 |
| **ML Libraries** | scikit-learn 1.3, XGBoost 2.0 |
| **Data Processing** | Pandas 2.0, NumPy 1.26 |
| **Visualization** | Plotly 5.15, Matplotlib |
| **Database** | SQLite3 |
| **Authentication** | GitHub OAuth 2.0 |
| **Serialization** | Joblib |
| **Environment** | python-dotenv |

---

## 🚀 Installation

### Prerequisites

- **Python 3.11+** installed
- **pip** package manager
- **Git** (optional, for cloning)

### Step-by-Step Setup

**1. Clone the repository**

```bash
git clone https://github.com/ashishponkiya/Devlytics-AI.git
cd Devlytics-AI
```

**2. Create a virtual environment**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r files/requirements.txt
```

**4. Generate training data**

```bash
cd files
python 01_generate_data.py
```

**5. Train the ML model**

```bash
python 02_train_model.py
```

**6. (Optional) Configure GitHub OAuth**

```bash
# Copy the environment example file
cp .env.example .env

# Edit .env with your GitHub OAuth credentials
# See files/SETUP_OAUTH.md for detailed instructions
```

**7. Run the application**

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501** 🎉

---

## 📖 Usage

### Quick Start (Demo Mode)

1. Run `streamlit run files/app.py`
2. Login with a demo account (see [Demo Accounts](#-demo-accounts))
3. Navigate using the sidebar menu
4. Try making a prediction on the **🔮 Make Prediction** page

### Making Predictions

1. Navigate to **🔮 Make Prediction**
2. Enter 15 developer metrics using sliders and input fields:
   - **Experience & Activity**: Years of experience, Git commits/month, Pull requests
   - **Quality Metrics**: PR acceptance rate, Bugs fixed/introduced, Test coverage
   - **Productivity**: Story points, Tasks completed, Deadlines missed
   - **Behavior**: Attendance, Overtime hours
   - **Feedback**: Code review score, Team feedback score
   - **Learning**: Training courses completed
3. Click **🎯 Predict Performance**
4. View the predicted category (Excellent / Good / Average / Poor) with confidence scores

### Performance Categories

| Category | Rating Range | Description |
|---|---|---|
| 🟢 **Excellent** | 4.5 – 5.0 | Top performer, exceeds expectations |
| 🔵 **Good** | 3.5 – 4.5 | Meets expectations, reliable contributor |
| 🟡 **Average** | 2.5 – 3.5 | Meets basic requirements |
| 🔴 **Poor** | 1.0 – 2.5 | Needs improvement and support |

---

## 📁 Project Structure

```
Devlytics-AI/
├── files/
│   ├── app.py                  # Main Streamlit dashboard (828 lines)
│   ├── auth.py                 # Authentication module (GitHub OAuth + Demo)
│   ├── database.py             # SQLite database operations
│   ├── 01_generate_data.py     # Synthetic data generation script
│   ├── 02_train_model.py       # Multi-algorithm model training script
│   ├── predict_example.py      # Standalone prediction example
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variables template
│   ├── SETUP_OAUTH.md          # GitHub OAuth setup guide
│   ├── developer_data.csv      # Generated training dataset (150 records)
│   ├── best_model.pkl          # Trained ML model (serialized)
│   ├── scaler_universal.pkl    # StandardScaler for feature normalization
│   ├── features.pkl            # Feature names list
│   └── devlytics.db            # SQLite database (users, roles, teams)
├── .gitignore
└── README.md
```

---

## 🧠 Machine Learning Pipeline

### Pipeline Overview

```
Data Generation → Feature Engineering → Model Training → Evaluation → Deployment
```

### Step 1: Data Generation (`01_generate_data.py`)

- Generates **150 synthetic developer profiles** with 15 performance metrics
- Simulates real-world data from Git repos, project management tools, and HR systems
- Creates target variable (Performance Rating 1–5) using a weighted scoring function
- Categorizes performance into 4 classes: Excellent, Good, Average, Poor

### Step 2: Model Training (`02_train_model.py`)

- **Data Split**: 80% training / 20% testing with stratified sampling
- **Feature Scaling**: StandardScaler normalization
- **Models Trained**:

| Model | Description |
|---|---|
| Logistic Regression | Linear baseline model |
| Decision Tree | Non-linear, interpretable model |
| Random Forest | Ensemble of 100 decision trees |
| XGBoost | Advanced gradient boosting |

- **Evaluation Metrics**: Accuracy, Precision, Recall, F1-Score
- **Model Selection**: Best model chosen by F1-Score
- **Feature Importance**: Identifies top predictors for performance

### Step 3: Deployment (`app.py`)

- Loads trained model with `joblib`
- Accepts 15 input metrics via interactive UI
- Returns predicted category with probability distribution
- Generates actionable insights based on input values

### 15 Input Features

| # | Feature | Source |
|---|---|---|
| 1 | Years of Experience | HR System |
| 2 | Git Commits/Month | Git Repository |
| 3 | Pull Requests | Git Repository |
| 4 | PR Acceptance Rate (%) | Code Review Tool |
| 5 | Bugs Fixed | Issue Tracker |
| 6 | Bugs Introduced | Issue Tracker |
| 7 | Unit Test Coverage (%) | CI/CD Pipeline |
| 8 | Story Points Completed | Project Management |
| 9 | Tasks Completed | Project Management |
| 10 | Deadlines Missed | Project Management |
| 11 | Attendance (%) | HR System |
| 12 | Overtime Hours/Month | HR System |
| 13 | Code Review Score (1-10) | Peer Review |
| 14 | Team Feedback Score (1-10) | 360° Review |
| 15 | Training Courses Completed | Learning Platform |

---

## 🔐 Authentication

### GitHub OAuth (Production)

For GitHub OAuth integration, you need to:

1. Create a GitHub OAuth App at [GitHub Developer Settings](https://github.com/settings/developers)
2. Set the callback URL to `http://localhost:8501`
3. Copy the Client ID and Client Secret to your `.env` file

```env
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
GITHUB_REDIRECT_URI=http://localhost:8501
```

> See [`files/SETUP_OAUTH.md`](files/SETUP_OAUTH.md) for detailed instructions.

### Demo Login (Development)

Demo login works out of the box — no configuration needed!

---

## 👥 Role-Based Access Control

| Feature | 👑 Admin | 📋 Manager | 💻 Developer |
|---|:---:|:---:|:---:|
| Home Dashboard | ✅ Full | ✅ Team Scope | ✅ Personal |
| Make Prediction | ✅ Any Developer | ✅ Team Members | ✅ Self-Assessment |
| Analytics | ✅ All Data | ✅ Team Data | ✅ Personal Data |
| Developer Insights | ✅ All Developers | ✅ Team Insights | ❌ |
| User Management | ✅ Full Control | ❌ | ❌ |
| Burnout Risk Analysis | ✅ | ✅ | ❌ |
| Correlation Heatmap | ✅ | ✅ | ❌ |

---

## 🔑 Demo Accounts

| Role | Username | Password |
|---|---|---|
| 👑 Admin | `admin` | `admin123` |
| 📋 Manager | `manager` | `manager123` |
| 💻 Developer | `developer` | `developer123` |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Ashish Ponkiya** — [@ashishponkiya](https://github.com/ashishponkiya)

---

<div align="center">

**⭐ If you found this project helpful, please give it a star! ⭐**

Built with ❤️ using Python, Streamlit, and Machine Learning

</div>
]]>
