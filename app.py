from pathlib import Path
import sys

# Ensure local imports resolve when launching from /rox_tools.
sys.path.insert(0, str(Path(__file__).resolve().parent / "ragnarok_x"))

from ragnarok_x.app import *  # noqa: F401,F403
