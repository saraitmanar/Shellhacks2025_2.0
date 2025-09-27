import streamlit as st
import utils.auth as auth
import pages as pages

st.set_page_config(page_title="Women's Health", page_icon="🌸", layout="centered")

# Simple theming (optional)
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #00000; }
[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
</style>
""", unsafe_allow_html=True)

st.title("🌸 Health")
st.subheader("K-12 Women’s Health (Demo)")
st.caption("Educational only — not medical advice.")

# Session bootstrap
if "user" not in st.session_state:
    st.session_state.user = None

# Role pick
role = st.radio(
    "I am a…",
    options=["Student", "Admin"],
    horizontal=True,
    label_visibility="visible",
)

with st.form("login"):
    student_id = st.text_input("Student/Admin ID", placeholder="e.g., S1001 or A0001")
    password   = st.text_input("Password", type="password", placeholder="••••••")
    submitted  = st.form_submit_button("Sign in")

if submitted:
    user = auth.verify_login(student_id.strip(), password.strip(), role)
    if user:
        st.session_state.user = user
        st.success(f"Welcome, {user['name']}! Redirecting…")
        # Try to route to the right page
        try:
            if user["role"] == "student":
                st.switch_page("pages/1_Student.py")
            else:
                st.switch_page("pages/2_Admin.py")
        except Exception:
            # Fallback: show page links if switch_page isn't available
            st.info("Use the sidebar to open your page.")
    else:
        st.error("Invalid credentials or wrong role. Try again.")

# If already logged in, show quick links
if st.session_state.user:
    u = st.session_state.user
    st.divider()
    st.write(f"You're signed in as **{u['name']}** ({u['role']}).")
    if u["role"] == "student":
        st.page_link("pages/1_Student.py", label="Go to Student page ➜")
    else:
        st.page_link("pages/2_Admin.py", label="Go to Admin dashboard ➜")
    if st.button("Sign out"):
        st.session_state.user = None
        st.experimental_rerun()
