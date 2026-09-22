"""
Database module for Devlytics AI
Handles user management, roles, and team assignments using SQLite.
"""

import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'devlytics.db')


def get_connection():
    """Get a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize the database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            github_id INTEGER UNIQUE,
            github_username TEXT NOT NULL UNIQUE,
            name TEXT,
            email TEXT,
            avatar_url TEXT,
            role TEXT DEFAULT 'developer' CHECK(role IN ('admin', 'manager', 'developer')),
            team TEXT DEFAULT 'Unassigned',
            developer_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demo_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            name TEXT,
            role TEXT DEFAULT 'developer' CHECK(role IN ('admin', 'manager', 'developer')),
            team TEXT DEFAULT 'Unassigned',
            developer_id TEXT,
            avatar_url TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Insert default demo users if they don't exist
    demo_users = [
        ('admin', 'admin123', 'Admin User', 'admin', 'All Teams', None),
        ('manager', 'manager123', 'Team Lead', 'manager', 'Alpha Team', None),
        ('developer', 'developer123', 'Dev User', 'developer', 'Alpha Team', 'DEV_001'),
    ]

    for username, password, name, role, team, dev_id in demo_users:
        cursor.execute('''
            INSERT OR IGNORE INTO demo_users (username, password, name, role, team, developer_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (username, password, name, role, team, dev_id))

    conn.commit()
    conn.close()


# ============================================
# USER OPERATIONS
# ============================================

def get_user_by_github_id(github_id):
    """Fetch a user by their GitHub ID."""
    conn = get_connection()
    user = conn.execute('SELECT * FROM users WHERE github_id = ?', (github_id,)).fetchone()
    conn.close()
    return dict(user) if user else None


def get_user_by_username(username):
    """Fetch a user by GitHub username."""
    conn = get_connection()
    user = conn.execute('SELECT * FROM users WHERE github_username = ?', (username,)).fetchone()
    conn.close()
    return dict(user) if user else None


def create_user(github_id, github_username, name, email, avatar_url):
    """Create a new user. First user becomes admin."""
    conn = get_connection()
    cursor = conn.cursor()

    # Check if this is the first user
    count = cursor.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    role = 'admin' if count == 0 else 'developer'

    cursor.execute('''
        INSERT INTO users (github_id, github_username, name, email, avatar_url, role, last_login)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (github_id, github_username, name, email, avatar_url, role, datetime.now()))

    conn.commit()
    user_id = cursor.lastrowid
    user = cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return dict(user)


def update_user_login(github_id):
    """Update last login timestamp."""
    conn = get_connection()
    conn.execute('UPDATE users SET last_login = ? WHERE github_id = ?', (datetime.now(), github_id))
    conn.commit()
    conn.close()


def update_user_role(user_id, new_role):
    """Update a user's role (admin only)."""
    conn = get_connection()
    conn.execute('UPDATE users SET role = ? WHERE id = ?', (new_role, user_id))
    conn.commit()
    conn.close()


def update_user_team(user_id, team):
    """Update a user's team assignment."""
    conn = get_connection()
    conn.execute('UPDATE users SET team = ? WHERE id = ?', (team, user_id))
    conn.commit()
    conn.close()


def update_user_developer_id(user_id, developer_id):
    """Map a user to a developer record from the dataset."""
    conn = get_connection()
    conn.execute('UPDATE users SET developer_id = ? WHERE id = ?', (developer_id, user_id))
    conn.commit()
    conn.close()


def get_all_users():
    """Get all registered users."""
    conn = get_connection()
    users = conn.execute('SELECT * FROM users ORDER BY created_at DESC').fetchall()
    conn.close()
    return [dict(u) for u in users]


def get_team_members(team):
    """Get all users in a specific team."""
    conn = get_connection()
    users = conn.execute('SELECT * FROM users WHERE team = ?', (team,)).fetchall()
    conn.close()
    return [dict(u) for u in users]


def get_all_teams():
    """Get unique team names."""
    conn = get_connection()
    teams = conn.execute('SELECT DISTINCT team FROM users WHERE team IS NOT NULL').fetchall()
    conn.close()
    return [t['team'] for t in teams]


def delete_user(user_id):
    """Delete a user."""
    conn = get_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()


# ============================================
# DEMO USER OPERATIONS
# ============================================

def verify_demo_user(username, password):
    """Verify demo user credentials."""
    conn = get_connection()
    user = conn.execute(
        'SELECT * FROM demo_users WHERE username = ? AND password = ?',
        (username, password)
    ).fetchone()
    conn.close()
    return dict(user) if user else None


def get_all_demo_users():
    """Get all demo users."""
    conn = get_connection()
    users = conn.execute('SELECT * FROM demo_users ORDER BY id').fetchall()
    conn.close()
    return [dict(u) for u in users]


def update_demo_user_role(user_id, new_role):
    """Update a demo user's role."""
    conn = get_connection()
    conn.execute('UPDATE demo_users SET role = ? WHERE id = ?', (new_role, user_id))
    conn.commit()
    conn.close()


def update_demo_user_team(user_id, team):
    """Update a demo user's team."""
    conn = get_connection()
    conn.execute('UPDATE demo_users SET team = ? WHERE id = ?', (team, user_id))
    conn.commit()
    conn.close()


def update_demo_user_developer_id(user_id, developer_id):
    """Map a demo user to a developer record."""
    conn = get_connection()
    conn.execute('UPDATE demo_users SET developer_id = ? WHERE id = ?', (developer_id, user_id))
    conn.commit()
    conn.close()


# Initialize the database on import
init_db()
