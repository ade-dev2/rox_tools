import streamlit as st
from pathlib import Path
from build_store import render_sidebar

st.set_page_config(page_title="Ragnarok X Tools", layout="centered")
render_sidebar()
assets_dir = Path(__file__).parent / "assets"
logo_path = assets_dir / "logo.webp"
if not logo_path.exists():
    logo_path = assets_dir / "logo.png"
if logo_path.exists():
    st.image(str(logo_path), width=180)
st.title("Ragnarok X: Tools for Privacy Members")
st.markdown("""
Use the sidebar to navigate between tools.

### 🔧 Tools
- **Enchant Lookup** — Look up enchant stat values and quality probabilities.

### ⚔️ Build Testing
- **Build Editor** — Create and edit offensive and defensive stats for builds.
- **⤷ Damage Calculator** — Use builds to calculate exact damage output and compare multiple builds.
- **⤷ Stat Optimizer** — Find stat priorities to guide build investment.
""")
