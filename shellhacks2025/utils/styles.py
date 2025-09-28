# utils/styles.py
# CSS styling for the application

CUSTOM_CSS = """
<style>
[data-testid="stAppViewContainer"] { 
    background-color: #fafafa; 
}
[data-testid="stHeader"] { 
    background-color: rgba(0,0,0,0); 
}
.stButton > button {
    background-color: #ff69b4;
    color: white;
    border-radius: 10px;
    border: none;
}
.stButton > button:hover {
    background-color: #ff1493;
    color: white;
}
</style>
"""