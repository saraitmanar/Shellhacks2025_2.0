# config.py
import os
import streamlit as st

# API Configuration
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")