import streamlit as st
from pathlib import Path
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
