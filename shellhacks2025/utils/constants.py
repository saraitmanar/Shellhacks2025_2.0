# utils/constants.py
# Application constants and configuration

# App Configuration
APP_TITLE = "Women's Health Education"
APP_ICON = "🌸"
APP_LAYOUT = "centered"

# User roles and permissions
ALLOWED_CHAT_BANDS = ["middle", "high"]
ELEMENTARY_REDIRECT_MESSAGE = "Chat is available for Middle and High school students. Explore the 3D Body instead!"

# Body regions for educational content
BODY_REGIONS = {
    "Uterus": {
        "what": "Where a pregnancy can grow; the lining sheds during periods.",
        "help": "Severe pain or very heavy bleeding → tell a trusted adult / nurse."
    },
    "Breast": {
        "what": "Changes during puberty; tenderness is common.",
        "help": "New hard lumps or skin changes → see a clinician."
    },
    "Lower Abdomen": {
        "what": "Period cramps may be felt here.",
        "help": "Severe/sudden pain with fever/vomiting → medical help."
    }
}

# 3D Model HTML template
MODEL_VIEWER_HTML = """
<script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
<model-viewer src="https://modelviewer.dev/shared-assets/models/Astronaut.glb"
              camera-controls auto-rotate
              style="width:100%;height:{height}px;background:#f6f6f6;border-radius:12px;">
</model-viewer>
"""