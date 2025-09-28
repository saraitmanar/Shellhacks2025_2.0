# import os
# import streamlit as st
# import streamlit.components.v1 as components
# from google import genai  # pip install google-genai

# st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

# # -------- AUTH GATE --------
# user = st.session_state.get("user")
# if not user:
#     st.error("Please sign in first.")
#     st.page_link("app.py", label="Back to Sign in")
#     st.stop()

# # Only middle/high can use chat
# band = user.get("band")
# if band not in ("middle", "high"):
#     st.warning("Chat is available only for Middle and High school students.")
#     st.page_link("pages/0_Body.py", label="Explore the 3D Body ➜")
#     st.stop()

# # -------- STATE --------
# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "Hi! Ask a question about women's health."}]
# if "last_answer" not in st.session_state:
#     st.session_state["last_answer"] = None
# if "drawer_open" not in st.session_state:
#     st.session_state["drawer_open"] = False

# # -------- GEMINI CLIENT (from secrets or env) --------
# API_KEY = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
# if not API_KEY:
#     st.error("Missing GEMINI_API_KEY. Add it to .streamlit/secrets.toml or environment.")
#     st.stop()
# client = genai.Client(api_key=API_KEY)

# # -------- PROMPTS (her logic, tidy) --------
# def make_prompt(user_input: str) -> str:
#     return (
#         "You are a helpful, informative assistant, educating the user like a friendly teacher. "
#         "Make your responses compatible with an education setting, friendly and clear. "
#         "Start with a brief 2–3 sentence summary. "
#         "List sources (URLs or titles) you used. "
#         "If users stray from women's health, gently steer them back. "
#         "Include a disclaimer: you are not a professional medical provider and this is for general information only. "
#         f"User: {user_input}\n"
#         "Assistant:"
#     )

# def make_refinement_prompt(last_answer: str, refinement: str) -> str:
#     return (
#         f"The last assistant answer was:\n\n{last_answer}\n\n"
#         f"The user requests this refinement: {refinement}\n\n"
#         "Rewrite the answer accordingly, keeping citations and the disclaimer."
#     )

# # -------- HEADER --------
# left, right = st.columns([1, 1])
# with left:
#     st.title("💬 Chat")
# with right:
#     c1, c2 = st.columns([1, 1])
#     with c1:
#         if st.button("🧍 Body"):
#             st.session_state["drawer_open"] = not st.session_state["drawer_open"]
#     with c2:
#         st.caption(f"Signed in as {user['name']} ({band})")

# st.caption("Educational only — not medical advice.")

# # -------- LAYOUT (drawer toggles) --------
# if st.session_state["drawer_open"]:
#     main, drawer = st.columns([3, 2], gap="large")
# else:
#     main = st.container()
#     drawer = None

# # -------- MAIN: conversation (single loop) --------
# with main:
#     history = st.container(height=420, border=True)
#     with history:
#         for msg in st.session_state["messages"]:
#             with st.chat_message(msg["role"]):
#                 st.markdown(msg["content"])

#     # Input + call Gemini
#     user_input = st.chat_input("Ask a question about women's health...")
#     if user_input:
#         # show user message
#         st.session_state["messages"].append({"role": "user", "content": user_input})
#         with st.chat_message("user"):
#             st.markdown(user_input)

#         # pick prompt (refinement vs new)
#         if (
#             st.session_state["last_answer"]
#             and any(w in user_input.lower() for w in ["shorter", "longer", "simpler", "summarize", "expand"])
#         ):
#             prompt_text = make_refinement_prompt(st.session_state["last_answer"], user_input)
#         else:
#             prompt_text = make_prompt(user_input)

#         # generate with Gemini
#         with st.chat_message("assistant"):
#             with st.spinner("Generating answer..."):
#                 try:
#                     response = client.models.generate_content(
#                         model="gemini-2.5-flash",
#                         contents=prompt_text,
#                     )
#                     bot_reply = response.text
#                 except Exception as e:
#                     bot_reply = f"Sorry — I couldn't get an answer right now. ({e})"

#                 st.markdown(bot_reply)
#                 st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
#                 st.session_state["last_answer"] = bot_reply

# # -------- DRAWER: quick body view --------
# if drawer:
#     with drawer:
#         st.markdown("### 🧍 Body quick view")
#         with st.expander("3D Model (demo)", expanded=True):
#             html = """
#             <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>
#             <model-viewer src="https://modelviewer.dev/shared-assets/models/Astronaut.glb"
#                           camera-controls auto-rotate
#                           style="width:100%;height:300px;background:#f6f6f6;border-radius:12px;">
#             </model-viewer>
#             """
#             components.html(html, height=320)

#         st.divider()
#         st.subheader("Regions")
#         regions = {
#             "Uterus": {"what": "Where a pregnancy can grow; lining sheds during periods.",
#                        "help": "Severe pain or very heavy bleeding → tell a trusted adult / nurse."},
#             "Breast": {"what": "Changes during puberty; tenderness is common.",
#                        "help": "New hard lumps or skin changes → see a clinician."},
#             "Lower Abdomen": {"what": "Period cramps may be felt here.",
#                               "help": "Severe/sudden pain with fever/vomiting → medical help."},
#         }
#         choice = st.radio("Pick an area:", list(regions.keys()))
#         st.write("**What it does:**", regions[choice]["what"])
#         st.write("**When to ask for help:**", regions[choice]["help"])
#         st.button("Close", on_click=lambda: st.session_state.update(drawer_open=False))
