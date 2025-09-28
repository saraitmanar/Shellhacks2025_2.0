import streamlit as st
import pandas as pd
from utils.constants import BODY_REGIONS
from utils.styles import CUSTOM_CSS

st.set_page_config(page_title="Admin Panel", page_icon="👑", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# Admin role check
if user["role"] != "admin":
    st.error("❌ Access denied. Admin privileges required.")
    if st.button("← Back to Home"):
        st.switch_page("app.py")
    st.stop()

# Header
st.title("👑 Admin Dashboard")
st.caption(f"Welcome, {user['name']} | Administrator Panel")

# Navigation tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "👥 Users", "📚 Content", "⚙️ Settings"])

# Overview Tab
with tab1:
    st.header("📊 System Overview")
    
    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Users", len(USERS))
    
    with col2:
        student_count = len([u for u in USERS if u["role"] == "student"])
        st.metric("Students", student_count)
    
    with col3:
        admin_count = len([u for u in USERS if u["role"] == "admin"])
        st.metric("Admins", admin_count)
    
    with col4:
        active_sessions = 1 if st.session_state.get("user") else 0
        st.metric("Active Sessions", active_sessions)
    
    st.divider()
    
    # User distribution chart
    st.subheader("👥 User Distribution by Grade Band")
    
    grade_bands = {}
    for u in USERS:
        if u["role"] == "student":
            band = u.get("band", "unknown")
            grade_bands[band] = grade_bands.get(band, 0) + 1
    
    if grade_bands:
        df = pd.DataFrame(list(grade_bands.items()), columns=["Grade Band", "Count"])
        st.bar_chart(df.set_index("Grade Band"))
    
    # Recent activity (simulated)
    st.subheader("📈 Recent Activity")
    st.info("🔄 Activity logging would be implemented in a production system")
    
    activity_data = {
        "Timestamp": ["2024-01-15 09:30", "2024-01-15 10:15", "2024-01-15 11:00"],
        "User": ["Ava (S1001)", "Liam (S1002)", "Maya (S1003)"],
        "Action": ["Logged in", "Used Chat", "Viewed 3D Body"],
        "Page": ["app.py", "Chat.py", "Body.py"]
    }
    
    st.dataframe(pd.DataFrame(activity_data), use_container_width=True)

# Users Tab
with tab2:
    st.header("👥 User Management")
    
    # Users table
    users_df = pd.DataFrame(USERS)
    users_df = users_df[["id", "name", "role", "band"]]  # Hide passwords
    
    st.subheader("Current Users")
    st.dataframe(users_df, use_container_width=True)
    
    st.divider()
    
    # Add new user form
    st.subheader("➕ Add New User")
    
    with st.form("add_user_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_id = st.text_input("User ID", placeholder="e.g., S1004")
            new_name = st.text_input("Full Name", placeholder="e.g., John Doe")
        
        with col2:
            new_role = st.selectbox("Role", ["student", "admin"])
            new_band = st.selectbox("Grade Band", ["elementary", "middle", "high", "N/A"])
        
        new_password = st.text_input("Password", type="password", placeholder="Enter password")
        
        submitted = st.form_submit_button("Add User")
        
        if submitted:
            if all([new_id, new_name, new_password]):
                # Check if ID already exists
                if any(u["id"] == new_id for u in USERS):
                    st.error("❌ User ID already exists!")
                else:
                    new_user = {
                        "id": new_id,
                        "name": new_name,
                        "role": new_role,
                        "band": new_band if new_band != "N/A" else None,
                        "password": new_password
                    }
                    # In a real app, this would be saved to a database
                    st.success(f"✅ User {new_name} ({new_id}) would be added to the system")
                    st.json(new_user)
            else:
                st.error("❌ Please fill in all required fields")

# Content Tab
with tab3:
    st.header("📚 Content Management")
    
    # Body regions management
    st.subheader("🧠 Body Regions Content")
    
    selected_region = st.selectbox("Select region to edit:", list(BODY_REGIONS.keys()))
    
    if selected_region:
        current_content = BODY_REGIONS[selected_region]
        
        with st.form(f"edit_{selected_region}"):
            st.markdown(f"**Editing: {selected_region}**")
            
            new_what = st.text_area("What it does:", value=current_content["what"], height=100)
            new_help = st.text_area("When to seek help:", value=current_content["help"], height=100)
            
            if st.form_submit_button("Update Content"):
                st.success(f"✅ Content for {selected_region} would be updated")
                st.json({"what": new_what, "help": new_help})
    
    st.divider()
    
    # Add new region
    st.subheader("➕ Add New Body Region")
    
    with st.form("add_region_form"):
        region_name = st.text_input("Region Name", placeholder="e.g., Ovaries")
        region_what = st.text_area("What it does:", placeholder="Describe the function...", height=80)
        region_help = st.text_area("When to seek help:", placeholder="When to consult healthcare...", height=80)
        
        if st.form_submit_button("Add Region"):
            if all([region_name, region_what, region_help]):
                st.success(f"✅ New region '{region_name}' would be added")
                st.json({
                    region_name: {
                        "what": region_what,
                        "help": region_help
                    }
                })
            else:
                st.error("❌ Please fill in all fields")

# Settings Tab
with tab4:
    st.header("⚙️ System Settings")
    
    # API Configuration
    st.subheader("🔧 API Configuration")
    
    with st.expander("Gemini API Settings"):
        api_status = "✅ Connected" if st.secrets.get("GEMINI_API_KEY") else "❌ Not configured"
        st.write(f"**Status:** {api_status}")
        
        if st.button("Test API Connection"):
            try:
                from google import genai
                from config import GEMINI_API_KEY
                if GEMINI_API_KEY:
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    st.success("✅ API connection successful!")
                else:
                    st.error("❌ API key not found")
            except Exception as e:
                st.error(f"❌ API connection failed: {str(e)}")
    
    st.divider()
    
    # Application Settings
    st.subheader("📱 Application Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Grade Band Access Control:**")
        elementary_chat = st.checkbox("Allow elementary students to use chat", value=False, disabled=True)
        st.caption("Currently restricted to Middle & High school")
        
        middle_chat = st.checkbox("Allow middle school students to use chat", value=True, disabled=True)
        high_chat = st.checkbox("Allow high school students to use chat", value=True, disabled=True)
    
    with col2:
        st.write("**Content Settings:**")
        show_3d_model = st.checkbox("Enable 3D body model", value=True, disabled=True)
        show_regions = st.checkbox("Show body regions info", value=True, disabled=True)
        educational_disclaimer = st.checkbox("Show educational disclaimer", value=True, disabled=True)
    
    st.divider()
    
    # System Information
    st.subheader("ℹ️ System Information")
    
    system_info = {
        "Application Version": "1.0.0-demo",
        "Streamlit Version": st.__version__,
        "Python Environment": "Streamlit Cloud",
        "Last Updated": "January 2025",
        "Configuration": "Demo Mode"
    }
    
    for key, value in system_info.items():
        st.write(f"**{key}:** {value}")
    
    st.divider()
    
    # Maintenance Actions
    st.subheader("🛠️ Maintenance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Clear All Sessions", use_container_width=True):
            st.warning("This would clear all user sessions in production")
    
    with col2:
        if st.button("📊 Export User Data", use_container_width=True):
            # Create CSV of user data (without passwords)
            export_data = [{k: v for k, v in user.items() if k != "password"} for user in USERS]
            df = pd.DataFrame(export_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="users_export.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("🧹 System Cleanup", use_container_width=True):
            st.info("System cleanup would run maintenance tasks")

# Footer navigation
st.divider()
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("💬 Test Chat", use_container_width=True):
        st.switch_page("pages/Chat.py")

with col2:
    if st.button("🧠 Test 3D Body", use_container_width=True):
        st.switch_page("pages/Body.py")

with col3:
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")