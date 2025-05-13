import streamlit as st
from dotenv import load_dotenv
import os
from utils.groq_client import query_groq

load_dotenv()

st.set_page_config(page_title="Mental Health Responder", page_icon="🌿", layout="centered")

# Custom CSS for aesthetic design
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    .stApp {
        background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Roboto', sans-serif;
    }
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        max-width: 800px;
        margin: auto;
    }
    .title {
        color: #1F2937;
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .subtitle {
        color: #4B5563;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 300;
        margin-bottom: 2rem;
    }
    .chat-message-user {
        background: #3B82F6;
        color: #FFFFFF;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        max-width: 70%;
        margin-left: auto;
        text-align: right;
    }
    .chat-message-responder {
        background: #E5E7EB;
        color: #1F2937;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        max-width: 70%;
        margin-right: auto;
    }
    .crisis-box {
        background: #FEE2E2;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
        border: 1px solid #EF4444;
    }
    .crisis-box strong {
        color: #B91C1C;
    }
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #D1D5DB;
        padding: 1rem;
        font-size: 1rem;
    }
    .stButton>button {
        background: #3B82F6;
        color: #FFFFFF;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 400;
        border: none;
        transition: background 0.3s;
    }
    .stButton>button:hover {
        background: #2563EB;
    }
    .crisis-button>button {
        background: #EF4444;
        color: #FFFFFF;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        font-weight: 400;
        border: none;
        transition: background 0.3s;
    }
    .crisis-button>button:hover {
        background: #DC2626;
    }
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main container
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown('<h1 class="title">🌿 Mental Health Responder</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">A safe space to share how you’re feeling. I’m here to listen.</p>', unsafe_allow_html=True)

    # Initialize session state for conversation history
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    # Get Help Now button
    st.markdown('<div class="crisis-button">', unsafe_allow_html=True)
    if st.button("Get Help Now", key="crisis_button"):
        st.markdown(
            """
            <div class='crisis-box'>
            <strong>You're not alone.</strong> Please reach out to a crisis hotline or professional support:
            <ul>
                <li>US: Call or text 988 (Suicide & Crisis Lifeline)</li>
                <li>UK: Call Samaritans at 116 123 or text SHOUT to 85258</li>
                <li>India: Call AASRA at +91-9820466726</li>
                <li>Global: Visit <a href="https://www.crisistextline.org">www.crisistextline.org</a> for more resources</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # Display conversation history
    if st.session_state.conversation_history:
        st.markdown("### Your Conversation")
        for msg in st.session_state.conversation_history:
            st.markdown(
                f'<div class="chat-message-user">{msg["user"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="chat-message-responder fade-in">{msg["assistant"]} <em>({msg["emotion"]})</em></div>',
                unsafe_allow_html=True,
            )

    # User input
    st.markdown("### Share Your Thoughts")
    user_input = st.text_area(
        "", 
        placeholder="Type how you’re feeling or what’s on your mind...", 
        height=150, 
        key="user_input"
    )

    if st.button("Send", key="send_button") and user_input:
        with st.spinner("Crafting a caring response..."):
            reply, emotion, is_crisis, resource_message = query_groq(user_input, st.session_state.conversation_history)
            
            # Store in conversation history (limit to 5 messages)
            st.session_state.conversation_history.append({
                "user": user_input,
                "assistant": reply,
                "emotion": emotion
            })
            if len(st.session_state.conversation_history) > 5:
                st.session_state.conversation_history.pop(0)
            
            # Display response
            st.markdown(f'### Response <em>({emotion})</em>')
            st.markdown(f'<div class="chat-message-responder fade-in">{reply}</div>', unsafe_allow_html=True)
            if is_crisis:
                st.markdown(
                    f'<div class="crisis-box"><strong>We care about you.</strong> {resource_message}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown('</div>', unsafe_allow_html=True)