import streamlit as st
from client import call_llm
from retriever import Retriever
from ticket_system import TicketSystem
import base64
def set_membership():
    choice = st.session_state.member_choice

    if choice == "No, I'm not a member":
        st.session_state.membership = False
        st.session_state.public_intro_done = False

    elif choice == "Yes, I'm a member":
        st.session_state.membership = True
        st.session_state.member_intro_done = False


st.set_page_config(page_title="GDGC Info Chatbot", page_icon="logo.png", layout="centered")

# -------------------------------  
# CSS  
# -------------------------------
def add_css():
    st.markdown("""
        <style>
            body { background-color: #0d0d0d; }

            .header-title {
                text-align: center;
                font-size: 40px;
                font-weight: 700;
                color: white;
                margin-top: -10px;
            }

            .subtitle {
                text-align: center;
                font-size: 16px;
                color: #bbbbbb;
                margin-bottom: 25px;
            }

            .bot-message {
                background-color: #1e1e1e;
                padding: 15px;
                border-radius: 12px;
                margin-bottom: 10px;
                color: white;
                border-left: 4px solid #4285F4;
            }

            .user-message {
                background-color: #2b2b2b;
                padding: 15px;
                border-radius: 12px;
                margin-bottom: 10px;
                color: white;
                text-align: right;
                border-right: 4px solid #34A853;
            }

            .center-img {
                display: flex;
                justify-content: center;
                margin-bottom: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

def load_logo():
    try:
        with open("logo.png", "rb") as img:
            encoded = base64.b64encode(img.read()).decode()
            st.markdown(
                f"<div class='center-img'><img src='data:image/png;base64,{encoded}' width='130'></div>",
                unsafe_allow_html=True
            )
    except:
        pass

add_css()
load_logo()

# -------------------------------
# Header
# -------------------------------
st.markdown("<div class='header-title'>GDGC Information Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Powered by RAG + OpenRouter API</div>", unsafe_allow_html=True)

# -------------------------------
# Session State
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "membership" not in st.session_state:
    st.session_state.membership = None

if "name" not in st.session_state:
    st.session_state.name = ""

if "team" not in st.session_state:
    st.session_state.team = ""

if "member_intro_done" not in st.session_state:
    st.session_state.member_intro_done = False

if "public_intro_done" not in st.session_state:
    st.session_state.public_intro_done = False

# Load tools
retriever = Retriever()
ticket_system = TicketSystem()

if st.session_state.membership is None:

    st.radio(
        "Are you a GDGC member?",
        ["Select", "No, I'm not a member", "Yes, I'm a member"],
        index=0,
        key="member_choice",
        on_change=set_membership   
    )

    st.stop()

# -------------------------------
# FIXED — STEP 2 — NON-MEMBER INTRO
# -------------------------------
if st.session_state.membership is False and not st.session_state.public_intro_done:

    intro = (
        "✨ **Welcome to GDGC (Google Developer Groups on Campus) VIT Bhopal!**\n\n"
        "We conduct workshops, hackathons, study jams, and offer mentorship.\n"
        "Feel free to ask me anything about events, teams, roles, and how to join!"
    )

    st.session_state.messages.append({"role": "assistant", "content": intro})
    st.session_state.public_intro_done = True

# -------------------------------
# FIXED — STEP 2 — MEMBER DETAILS (OPTIONAL)
# -------------------------------
if st.session_state.membership is True and not st.session_state.member_intro_done:

    st.markdown("### Member Details (Optional)")

    name = st.text_input("Your name:", key="member_name")
    teams = [
        "Machine Learning", "Android", "Web Development", "Women Techmaker",
        "Content", "Design", "Videography", "Blockchain"
    ]
    team = st.selectbox("Your team:", [""] + teams, key="member_team")

    if st.button("Continue", key="member_continue"):
        st.session_state.name = name
        st.session_state.team = team

        # Personalized intro
        if name:
            intro = f"Hi {name}! 👋 Great to have someone from the **{team or 'GDGC'} Team**!"
        else:
            intro = "Welcome GDGC Member! 👋 How can I assist you today?"

        st.session_state.messages.append({"role": "assistant", "content": intro})
        st.session_state.member_intro_done = True

    st.stop()

# -------------------------------
# Show Chat History
# -------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'>{msg['content']}</div>", unsafe_allow_html=True)

# -------------------------------
# CHATBOX — Always Visible
# -------------------------------
user_input = st.text_input("Ask me anything about GDGC...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.markdown(f"<div class='user-message'>{user_input}</div>", unsafe_allow_html=True)

    # Ticket keywords
    help_keywords = ["help", "issue", "problem", "support", "not working", "raise a ticket"]

    if any(k in user_input.lower() for k in help_keywords):
        ticket_id = ticket_system.create_ticket(user_input)
        reply = f"📝 Your support ticket has been created! Ticket ID: **{ticket_id}**."
    else:
        chunks = retriever.retrieve(user_input)
        reply = call_llm(chunks, user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.markdown(f"<div class='bot-message'>{reply}</div>", unsafe_allow_html=True)
