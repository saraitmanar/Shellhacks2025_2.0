import streamlit as st
from PIL import Image, ImageDraw
from streamlit_image_coordinates import streamlit_image_coordinates
from pages.gradeBands import BANDS

st.set_page_config(page_title="K-12 Anatomy Click Bot", page_icon="🫀", layout="centered")

IMG_PATH = "assets/body_shell.jpg"

# Heart bounding box in normalized coords (x_min, y_min, x_max, y_max)
# Tweak after checking the debug box below.
BRAIN_BBOX_NORM  = (0.43, 0.04, 0.56, 0.12)
HEART_BBOX_NORM  = (0.43, 0.2, 0.56, 0.22)
LUNGS_BBOX_NORM = (0.38, 0.13, 0.61, 0.2)
STOMACH_BBOX_NORM = (0.42, 0.25, 0.57, 0.32)

def in_bbox(px_norm: float, py_norm: float, bbox_norm: tuple[float, float, float, float]) -> bool:
    x0, y0, x1, y1 = bbox_norm
    return x0 <= px_norm <= x1 and y0 <= py_norm <= y1

st.title("Click the Body to Learn 🧠🫀")
grade_key = st.radio("Grade band", list(BANDS.keys()), horizontal=True)
band = BANDS[grade_key]

img = Image.open(IMG_PATH)
w, h = img.size
coords = streamlit_image_coordinates(img, key="body")

if coords:
    x_px, y_px = coords["x"], coords["y"]
    x_n, y_n = x_px / w, y_px / h

    with st.expander("Debug (hide for class)"):
        st.write({"clicked_pixels": (x_px, y_px),
                  "clicked_normalized": (round(x_n, 3), round(y_n, 3)),
                  "image_size_px": (w, h)})

    if in_bbox(x_n, y_n, HEART_BBOX_NORM):
        fact = band.fact("heart")
        if fact:
            st.success(f"🫀 Heart — {fact}")
        else:
            st.info("No fact defined for this grade band yet.")
    else:
        st.info("Try clicking the upper-left chest area (heart).")

st.caption("Dev note: add more organs by defining more normalized bounding boxes in app.py and adding facts in gradeBands.py.")
