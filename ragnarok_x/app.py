from __future__ import annotations

import os
from pathlib import Path
import shutil
import secrets

import streamlit as st


def _first_env(*names: str) -> str | None:
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def _is_placeholder(value: str | None) -> bool:
    """Return True if value looks like a placeholder that should be replaced."""
    if value is None:
        return True
    placeholder_patterns = (
        "your_", "placeholder", "xxx", "TODO", "REPLACE",
    )
    lower = value.lower().strip()
    return any(p in lower for p in placeholder_patterns)


def _value_in_toml(content: str, key: str) -> str | None:
    """Extract the value for a toml key from file content. Returns None if not found."""
    import re
    # Match: key = "value" or key="value" with optional whitespace/comments
    pattern = rf'^{re.escape(key)}\s*=\s*["\']([^"\']*)["\']'
    match = re.search(pattern, content, re.MULTILINE)
    return match.group(1) if match else None


def _bootstrap_streamlit_secrets_from_env() -> None:
    """Create or update .streamlit/secrets.toml from env vars when needed.

    Only regenerates if:
    - File does not exist, OR
    - Env vars are set AND the corresponding secrets.toml values are placeholders
      (ignoring comments/documentation).
    """
    app_dir = Path(__file__).resolve().parent
    secrets_paths = [
        app_dir / ".streamlit" / "secrets.toml",
        app_dir.parent / ".streamlit" / "secrets.toml",
    ]

    google_client_id     = _first_env("GOOGLE_CLIENT_ID", "GOOGLE_AUTH_CLIENT_ID", "STREAMLIT_GOOGLE_CLIENT_ID")
    google_client_secret = _first_env("GOOGLE_CLIENT_SECRET", "GOOGLE_AUTH_CLIENT_SECRET", "STREAMLIT_GOOGLE_CLIENT_SECRET")
    cookie_secret        = _first_env("STREAMLIT_COOKIE_SECRET", "AUTH_COOKIE_SECRET", "COOKIE_SECRET")
    mongo_uri            = _first_env("MONGO_URI", "MONGODB_URI")

    # Check if we have anything useful to write
    has_auth_secrets = bool(google_client_id and google_client_secret)

    # File doesn't exist — create it if we have credentials
    primary_path = secrets_paths[0]
    if not primary_path.exists():
        if not has_auth_secrets:
            return  # Can't write useful config without credentials
        _write_secrets(primary_path, google_client_id, google_client_secret, cookie_secret, mongo_uri)
        _mirror_secrets(primary_path, secrets_paths[1:])
        return

    # File exists — check if it needs updating
    try:
        content = primary_path.read_text(encoding="utf-8")
    except Exception:
        return  # Can't read file, give up

    # Determine if we need to regenerate
    needs_regen = False

    # Check Google auth: only regenerate if env var is set AND file value is placeholder
    if google_client_id and google_client_secret:
        existing_id = _value_in_toml(content, "google_client_id")
        existing_secret = _value_in_toml(content, "google_client_secret")
        if _is_placeholder(existing_id) or _is_placeholder(existing_secret):
            needs_regen = True

    # Check MongoDB: only regenerate if env var is set AND file value is placeholder
    if mongo_uri and not needs_regen:
        existing_mongo = _value_in_toml(content, "uri")
        # For mongodb, check for "your_" in the value
        if existing_mongo and "your_" in existing_mongo.lower():
            needs_regen = True

    if not needs_regen:
        _mirror_secrets(primary_path, secrets_paths[1:])
        return

    _write_secrets(primary_path, google_client_id, google_client_secret, cookie_secret, mongo_uri)
    _mirror_secrets(primary_path, secrets_paths[1:])


def _mirror_secrets(source: Path, destinations: list[Path]) -> None:
    """Mirror generated secrets to wrapper launch roots used by Streamlit."""
    for destination in destinations:
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists() or destination.read_text(encoding="utf-8") != source.read_text(encoding="utf-8"):
                shutil.copyfile(source, destination)
        except Exception:
            pass


def _write_secrets(path: Path, google_client_id: str | None, google_client_secret: str | None, cookie_secret: str | None, mongo_uri: str | None) -> None:
    """Write the secrets.toml file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "[auth]",
        'provider              = "google"',
    ]
    if google_client_id:
        lines.append(f'google_client_id      = "{google_client_id}"')
    if google_client_secret:
        lines.append(f'google_client_secret = "{google_client_secret}"')
    lines.append(f'cookie_secret        = "{cookie_secret or secrets.token_urlsafe(32)}"')
    lines.extend([
        'redirect_uri          = "https://rox-priv-stats.streamlit.app/oauth2callback"',
        "allow_password_login  = false",
    ])
    if mongo_uri:
        lines.extend([
            "",
            "[mongodb]",
            f'uri = "{mongo_uri}"',
        ])

    path.write_text("\n".join(lines), encoding="utf-8")


_bootstrap_streamlit_secrets_from_env()

from build_store import render_sidebar

st.set_page_config(page_title="Privacy: Ragnarok X Tools", layout="centered")
render_sidebar()
assets_dir = Path(__file__).parent / "assets"

st.markdown(
    """<style>
    .home-title {
        white-space: nowrap;
        overflow: visible;
        margin: 0.2rem 0 0.75rem;
        font-size: clamp(1rem, 2vw, 1.55rem);
        line-height: 1.15;
    }
    [data-testid="stImage"] img {
        object-fit: contain !important;
        object-position: center top !important;
    }
    </style>""",
    unsafe_allow_html=True,
)

logo_path = assets_dir / "logo.webp"
if not logo_path.exists():
    logo_path = assets_dir / "logo.png"
if logo_path.exists():
    st.image(str(logo_path), width=260)

st.markdown('<h1 class="home-title">Privacy: Ragnarok X Tools</h1>', unsafe_allow_html=True)
st.markdown("""
Use the sidebar to navigate between tools.

### 🔧 Tools
- **Enchant Lookup** — Look up enchant stat values and quality probabilities.

### ⚔️ Build Testing
- **Build Editor** — Create and edit offensive and defensive stats for builds.
- **⤷ Damage Calculator** — Use builds to calculate exact damage output and compare multiple builds.
- **⤷ Stat Optimizer** — Find stat priorities to guide build investment.
""")
