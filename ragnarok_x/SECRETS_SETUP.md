# OAuth Setup Guide — Ragnarok X Tools

Each user authenticates with their own account, so builds are stored separately and never collide.

---

## Quick Setup: Google OAuth (Recommended)

### Step 1 — Create a Google Cloud project

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Click **Select a project** → **New Project** → name it → **Create**
3. Open the project, go to **APIs & Services → Library**
4. Search for and **Enable** _"Google Identity Toolkit API"_

### Step 2 — Configure OAuth consent screen

1. Go to **APIs & Services → OAuth consent screen**
2. Choose **External** → **Create**
3. Fill in:
   - App name: `Ragnarok X Tools`
   - Support email: _(your email)_
   - Developer contact: _(your email)_
4. Click **Save and Continue** through Scopes
5. On **Test users**: click **Add Users** → add _your_ Google email
   > ⚠️ Only test users can log in until you publish the app. Add your email here first.

### Step 3 — Create OAuth credentials

1. Go to **APIs & Services → Credentials**
2. **Create Credentials** → **OAuth client ID**
3. Application type: **Web application**, name it
4. Under **Authorized redirect URIs** add:
   ```
   https://streamlit.io/oauth2callback
   ```
5. Click **Create**
6. Copy the **Client ID** and **Client Secret**

### Step 4 — Add secrets to Streamlit Cloud

1. Open your app at [share.streamlit.io](https://share.streamlit.io)
2. Click **Settings** → **Secrets**
3. Paste this, substituting your values:

```toml
[auth]
provider             = "google"
google_client_id     = "YOUR_CLIENT_ID.apps.googleusercontent.com"
google_client_secret = "YOUR_CLIENT_SECRET"
enable_viewer_invites = true
allow_password_login  = false
```

4. **Save**

### Step 5 — Add yourself as a viewer (Streamlit Cloud)

1. In Streamlit Cloud, go to your app's **Settings → Sharing**
2. Invite your Google email as a **Viewer**

### Step 6 — Test

1. Open your app — you should see a **Log in with Google** button
2. Click it, sign in with your Google account
3. The `⚠️ Dev bypass active` warning will disappear
4. Each user's builds are now stored independently

---

## GitHub OAuth (Alternative)

### Step 1 — Register a GitHub OAuth App

1. Go to [github.com/settings/developers](https://github.com/settings/developers)
2. **New OAuth App**
3. Fill in:
   - Homepage URL: `https://your-app-name.streamlit.app`
   - Authorization callback URL: `https://streamlit.io/oauth2callback`
4. **Register application**
5. Copy **Client ID** → generate a new **Client Secret** → copy it

### Step 2 — Add secrets

```toml
[auth]
provider             = "github"
github_client_id     = "YOUR_CLIENT_ID"
github_client_secret = "YOUR_CLIENT_SECRET"
```

---

## Important Notes

| Topic | Detail |
|---|---|
| **Local dev** | Copy `.streamlit/secrets.toml` to your local `.streamlit/secrets.toml` to test auth locally |
| **.gitignore** | Make sure `secrets.toml` is gitignored — never commit real credentials |
| **Existing dev data** | After enabling auth, all `dev@localhost` build data is orphaned. Users start fresh. |
| **Publishing** | Until you publish the OAuth app in Google Cloud, only test users can log in |
| **Viewer invites** | `enable_viewer_invites = true` lets you add specific email addresses in Streamlit Cloud Sharing settings |

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `⚠️ Dev bypass active` still shows | Make sure `[auth]` is not commented out — no `#` before it |
| `Log in with Google` not shown | Reload the app after saving secrets |
| "Invalid client" after deploy | Verify redirect URI is exactly `https://streamlit.io/oauth2callback` |
| Can't log in at all | Confirm your email is a test user in Google Cloud OAuth consent screen |
| `st.user.get` errors | Requires Streamlit ≥ 1.41 and a real `[auth]` section in secrets |

---

Questions? See [Streamlit Auth Docs](https://docs.streamlit.io/develop/authentication).
