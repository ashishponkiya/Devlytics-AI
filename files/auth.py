"""
Authentication module for Devlytics AI
Supports GitHub OAuth and demo login for testing.
"""

import streamlit as st
import requests
import os
from dotenv import load_dotenv
from database import (
    get_user_by_github_id, create_user, update_user_login,
    verify_demo_user, init_db
)

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID', '')
GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET', '')
GITHUB_REDIRECT_URI = os.getenv('GITHUB_REDIRECT_URI', 'http://localhost:8501')

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"


def is_github_oauth_configured():
    """Check if GitHub OAuth credentials are set."""
    return bool(GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET)


def get_github_auth_url():
    """Generate GitHub OAuth authorization URL."""
    return (
        f"{GITHUB_AUTH_URL}"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={GITHUB_REDIRECT_URI}"
        f"&scope=read:user user:email"
    )


def exchange_code_for_token(code):
    """Exchange OAuth code for access token."""
    response = requests.post(
        GITHUB_TOKEN_URL,
        headers={"Accept": "application/json"},
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": GITHUB_REDIRECT_URI,
        },
        timeout=10,
    )
    if response.status_code == 200:
        data = response.json()
        return data.get("access_token")
    return None


def get_github_user_info(access_token):
    """Get user info from GitHub API."""
    response = requests.get(
        GITHUB_USER_URL,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
        timeout=10,
    )
    if response.status_code == 200:
        return response.json()
    return None


def handle_github_callback():
    """Handle the OAuth callback from GitHub."""
    params = st.query_params
    code = params.get("code")

    if code:
        token = exchange_code_for_token(code)
        if token:
            github_user = get_github_user_info(token)
            if github_user:
                # Check if user exists
                user = get_user_by_github_id(github_user['id'])
                if not user:
                    user = create_user(
                        github_id=github_user['id'],
                        github_username=github_user['login'],
                        name=github_user.get('name', github_user['login']),
                        email=github_user.get('email', ''),
                        avatar_url=github_user.get('avatar_url', ''),
                    )
                else:
                    update_user_login(github_user['id'])

                # Store in session
                st.session_state['authenticated'] = True
                st.session_state['user'] = user
                st.session_state['auth_method'] = 'github'

                # Clear the code from URL
                st.query_params.clear()
                st.rerun()
                return True
    return False


def is_authenticated():
    """Check if user is authenticated."""
    return st.session_state.get('authenticated', False)


def get_current_user():
    """Get the current authenticated user."""
    return st.session_state.get('user', None)


def logout():
    """Clear authentication state."""
    for key in ['authenticated', 'user', 'auth_method']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


def login_page():
    """Render the login page with GitHub OAuth and demo login."""

    # Custom CSS for login page
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .login-container {
        max-width: 480px;
        margin: 0 auto;
        padding: 2.5rem;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }

    .login-title {
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #00d2ff, #7b2ff7, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .login-subtitle {
        font-family: 'Inter', sans-serif;
        text-align: center;
        color: #8892b0;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    .github-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        width: 100%;
        padding: 14px 24px;
        background: #24292e;
        color: white;
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
    }
    .github-btn:hover {
        background: #2ea44f;
        border-color: #2ea44f;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(46,164,79,0.35);
        color: white;
    }

    .divider-line {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.5rem 0;
        color: #5a6577;
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
    }
    .divider-line::before, .divider-line::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .divider-line::before { margin-right: 1rem; }
    .divider-line::after { margin-left: 1rem; }

    .role-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    .role-admin { background: rgba(255,107,107,0.15); color: #ff6b6b; }
    .role-manager { background: rgba(0,210,255,0.15); color: #00d2ff; }
    .role-developer { background: rgba(123,47,247,0.15); color: #b57bff; }

    .demo-info {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
        font-family: 'Inter', sans-serif;
    }
    .demo-info-title {
        color: #ccd6f6;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }
    .demo-cred {
        color: #8892b0;
        font-size: 0.8rem;
        line-height: 1.8;
    }
    .demo-cred code {
        background: rgba(255,255,255,0.08);
        padding: 2px 8px;
        border-radius: 4px;
        color: #ccd6f6;
        font-size: 0.8rem;
    }

    div[data-testid="stVerticalBlock"] > div:has(> .login-container) {
        display: flex;
        justify-content: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # Centered layout
    col_spacer1, col_center, col_spacer2 = st.columns([1, 2, 1])

    with col_center:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<p class="login-title">🚀 Devlytics AI</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="login-subtitle">Developer Performance Intelligence Platform</p>',
            unsafe_allow_html=True
        )

        # GitHub OAuth Login
        if is_github_oauth_configured():
            auth_url = get_github_auth_url()
            st.markdown(
                f'<a href="{auth_url}" class="github-btn">'
                f'<svg height="20" width="20" viewBox="0 0 16 16" fill="white">'
                f'<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38'
                f' 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28'
                f'-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28'
                f'-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02'
                f'.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04'
                f' 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75'
                f'-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013'
                f' 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
                f' Sign in with GitHub</a>',
                unsafe_allow_html=True,
            )
            st.markdown('<div class="divider-line">or use demo account</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="divider-line">Sign in with demo account</div>',
                unsafe_allow_html=True,
            )

        # Demo Login Form
        with st.form("demo_login", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter demo username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("🔐  Sign In", use_container_width=True)

            if submitted:
                if username and password:
                    demo_user = verify_demo_user(username, password)
                    if demo_user:
                        st.session_state['authenticated'] = True
                        st.session_state['user'] = demo_user
                        st.session_state['auth_method'] = 'demo'
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
                else:
                    st.warning("Please enter both username and password")

        # Demo credentials info
        st.markdown('''
        <div class="demo-info">
            <div class="demo-info-title">🔑 Demo Accounts</div>
            <div class="demo-cred">
                <span class="role-badge role-admin">Admin</span>&nbsp;
                <code>admin</code> / <code>admin123</code><br>
                <span class="role-badge role-manager">Manager</span>&nbsp;
                <code>manager</code> / <code>manager123</code><br>
                <span class="role-badge role-developer">Developer</span>&nbsp;
                <code>developer</code> / <code>developer123</code>
            </div>
        </div>
        ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # Handle GitHub callback if code is in URL
    if is_github_oauth_configured():
        handle_github_callback()
