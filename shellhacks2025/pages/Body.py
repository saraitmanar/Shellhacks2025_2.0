# pages/0_Body.py
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="3D Body", page_icon="🧍", layout="wide")

# --- auth gate (all roles allowed, but must be signed in) ---
user = st.session_state.get("user")
if not user:
    st.error("Please sign in first.")
    st.page_link("app.py", label="Back to Sign in")
    st.stop()

st.title("🧍 3D Body Viewer")

html = """
<script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
<model-viewer src="https://modelviewer.dev/shared-assets/models/Astronaut.glb"
              camera-controls auto-rotate
              style="width:100%;height:520px;background:#f6f6f6;border-radius:12px;">
</model-viewer>
"""
components.html(html, height=560)

st.sidebar.header("Learn about body areas")
regions = {
    "Uterus": {"what": "Where a pregnancy can grow; the lining sheds during periods.",
               "help": "Severe pain or very heavy bleeding → tell a trusted adult / nurse."},
    "Breast": {"what": "Changes during puberty; tenderness is common.",
               "help": "New hard lumps or skin changes → see a clinician."},
    "Lower Abdomen": {"what": "Period cramps may be felt here.",
                      "help": "Severe/sudden pain with fever/vomiting → medical help."},
}
choice = st.sidebar.radio("Pick an area:", list(regions.keys()))
st.subheader(choice)
st.write("**What it does:**", regions[choice]["what"])
st.write("**When to ask for help:**", regions[choice]["help"])
