import streamlit as st
from client import call_llm
from retriever import Retriever
from ticket_system import TicketSystem
import base64
 
st.set_page_config(page_title="GDGC Info Chatbot", page_icon="logo.png", layout="centered")

# -------------------------------
# CSS STYLING
# -------------------------------
def add_custom_css():
    st.markdown("""
    <style>
        .bot-message {
            background-color: #1e1e1e;
            padding: 15px;
            border-radius: 12px;
            color: #fff;
            margin-bottom: 10px;
            border-left: 4px solid #4285F4;
        }
        .user-message {
            background-color: #2d2d2d;
            padding: 15px;
            border-radius: 12px;
            color: #fff;
            margin-bottom: 10px;
            text-align: right;
            border-right: 4px solid #34A853;
        }
        .header-title {
            text-align: center;
            font-size: 40px;
            font-weight: 700;
            color: #ffffff;
        }
        .subtitle {
            text-align: center;
            font-size: 16px;
            color: #cccccc;
            margin-bottom: 20px;
        }
        body {
            background-color: #0d0d0d;
        }
        .center-img {
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

def load_logo():
    with open("logo.png", "rb") as img:
        b64 = base64.b64encode(img.read()).decode()
        st.markdown(
            f"<div class='center-img'><img src='data:image/png;base64,{b64}' width='120'></div>",
            unsafe_allow_html=True
        )

add_custom_css()
load_logo()

# -------------------------------
# PAGE HEADER
# -------------------------------
st.markdown("<div class='header-title'>GDGC Information Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Powered by RAG + OpenRouter API</div>", unsafe_allow_html=True)

# -------------------------
# INITIALIZE SESSION STATE
# -------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "membership" not in st.session_state:
    st.session_state.membership = None  # None = not answered yet

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_team" not in st.session_state:
    st.session_state.user_team = ""

if "public_intro_shown" not in st.session_state:
    st.session_state.public_intro_shown = False

if "member_intro_shown" not in st.session_state:
    st.session_state.member_intro_shown = False

# -------------------------
# LOAD RETRIEVER & TICKETS
# -------------------------
retriever = Retriever()
ticket_available = True
ticket_system = TicketSystem()

# -------------------------
# WELCOME MESSAGE
# -------------------------
st.markdown("""
🌟 **Welcome!**  
Your personal assistant for everything related to **GDGC VIT Bhopal**.
""")

# -------------------------
# ASK MEMBERSHIP (ONLY ONCE)
# -------------------------
if st.session_state.membership is None:
    membership_choice = st.radio(
        "Are you a GDGC member?",
        options=["Select", "No, I'm not a member", "Yes, I'm a member"],
        index=0
    )

    if membership_choice == "No, I'm not a member":
        st.session_state.membership = False

    elif membership_choice == "Yes, I'm a member":
        st.session_state.membership = True

# -------------------------
# IF NOT A GDGC MEMBER
# -------------------------
if st.session_state.membership is False and not st.session_state.public_intro_shown:

    intro = (
        "✨ **Welcome to GDGC (Google Developer Groups on Campus)** at VIT Bhopal! "
        "We host workshops, hackathons, study jams, and provide mentorship & dev opportunities. "
        "Feel free to ask about events, teams, or how to join!"
    )

    st.session_state.messages.append({"role": "assistant", "content": intro})
    st.markdown(f"<div class='bot-message'>{intro}</div>", unsafe_allow_html=True)

    st.session_state.public_intro_shown = True

# -------------------------
# IF USER IS GDGC MEMBER
# -------------------------
if st.session_state.membership is True and not st.session_state.member_intro_shown:

    st.markdown("### Member Details (Optional)")
    name = st.text_input("Your name:")
    team = st.selectbox("Your team:", ["", "Machine Learning", "Web Development", "Women Techmakers", "Blockchain", "Videograhy", "Events & Outreach" "Design", "Content"])

    st.session_state.user_name = name
    st.session_state.user_team = team

    if st.button("Continue"):
      if name:
        msg = f"Hi {name}! 👋 Great to have someone from the **{team or 'GDGC'} Team**."
      else:
        msg = "Welcome GDGC member! 👋 How can I help you today?"

      st.session_state.messages.append({"role": "assistant", "content": msg})
      st.markdown(f"<div class='bot-message'>{msg}</div>", unsafe_allow_html=True)

      st.session_state.member_intro_shown = True


# -------------------------
# SHOW CHAT HISTORY
# -------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'>{msg['content']}</div>", unsafe_allow_html=True)

# -------------------------
# CHAT INPUT (ALWAYS AT BOTTOM)
# -------------------------
user_text = st.text_input("Ask me anything about GDGC...", key="chatbox")

if user_text:
    # Show user's message
    st.session_state.messages.append({"role": "user", "content": user_text})
    st.markdown(f"<div class='user-message'>{user_text}</div>", unsafe_allow_html=True)

    # Ticket detection
    keywords = ["help", "issue", "problem", "support", "not working"]

    if any(k in user_text.lower() for k in keywords) and ticket_available:
        tid = ticket_system.create_ticket(user_text)
        reply = f"📝 Your support ticket has been created! Ticket ID: **{tid}**."
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.markdown(f"<div class='bot-message'>{reply}</div>", unsafe_allow_html=True)

    else:
        # RAG response
        chunks = retriever.retrieve(user_text)
        bot_reply = call_llm(chunks, user_text)

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.markdown(f"<div class='bot-message'>{bot_reply}</div>", unsafe_allow_html=True)
