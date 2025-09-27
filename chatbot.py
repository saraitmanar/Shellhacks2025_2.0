import streamlit as st
import requests
from google import genai
from config import GEMINI_API_KEY


client = genai.Client(api_key=GEMINI_API_KEY)

st.title("Women's Health")

# Initialize messages if not already in session_state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "last_answer" not in st.session_state:
    st.session_state["last_answer"] = None

# Show conversation so far
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Function to build prompt to include instructions + user input
def make_prompt(user_input: str) -> str:
    return (
        "You are a helpful, informative assistant, educating the user like a friendly teacher. "
        "Make your responses more compatible for an education setting or human-to-human talk."
        "When answering, provide a brief summary (2-3 sentences). "
        "Provide key points in bullet form if appropriate. "
        "Always list sources (URLs or titles) you used. "
        "If the user asks questions straying from the topics of women's health, politely move them back on subject. "
        "The focus should always remain on accessible education on women's health. "
        "Include a disclaimer: you are not a professional medical provider and this is for general information only. "
        f"User: {user_input}\n"
        "Assistant:"
    )

def make_refinement_prompt(last_answer: str, refinement: str) -> str:
    return (
        f"The last assistant answer was:\n\n{last_answer}\n\n"
        f"The user wants a refinement: {refinement}\n\n"
        "Please rewrite the previous answer according to this refinement, keeping citations and the disclaimer."
    )

# Show conversation
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])



# Input box for user
if user_input := st.chat_input("Ask a question about women's health..."):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if (
            st.session_state["last_answer"]
            and any(word in user_input.lower() for word in ["shorter", "longer", "simpler", "summarize", "expand"])
    ):
        prompt = make_refinement_prompt(st.session_state["last_answer"], user_input)
    else:
        prompt = make_prompt(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Generating answer..."):
            prompt = make_prompt(user_input)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            bot_reply = response.text

            st.markdown(bot_reply)
            st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
            st.session_state["last_answer"] = bot_reply
