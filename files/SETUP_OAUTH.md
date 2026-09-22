# 🔐 Setting Up GitHub OAuth for Devlytics AI

## Step 1: Create a GitHub OAuth App

1. Go to **GitHub** → **Settings** → **Developer Settings** → **OAuth Apps**
   - Direct link: [https://github.com/settings/developers](https://github.com/settings/developers)
2. Click **"New OAuth App"**
3. Fill in the details:

| Field | Value |
|-------|-------|
| **Application name** | `Devlytics AI` |
| **Homepage URL** | `http://localhost:8501` |
| **Authorization callback URL** | `http://localhost:8501` |

4. Click **"Register application"**

## Step 2: Get Your Credentials

1. After creating the app, you'll see your **Client ID**
2. Click **"Generate a new client secret"** to get the **Client Secret**
3. ⚠️ **Copy the secret immediately** — it's only shown once!

## Step 3: Configure Environment

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and paste your credentials:
   ```env
   GITHUB_CLIENT_ID=your_actual_client_id
   GITHUB_CLIENT_SECRET=your_actual_client_secret
   GITHUB_REDIRECT_URI=http://localhost:8501
   ```

## Step 4: Run the App

```bash
streamlit run app.py
```

The login page will now show both:
- **"Sign in with GitHub"** button (OAuth)
- **Demo login** (for quick testing)

## 🔑 Demo Accounts (No Setup Required)

You can use these accounts immediately without GitHub OAuth:

| Role | Username | Password |
|------|----------|----------|
| **👑 Admin** | `admin` | `admin123` |
| **📋 Manager** | `manager` | `manager123` |
| **💻 Developer** | `developer` | `developer123` |

## Notes

- The **first GitHub user** to log in automatically becomes **Admin**
- All subsequent GitHub users get the **Developer** role by default
- Admins can change any user's role from the **User Management** page
