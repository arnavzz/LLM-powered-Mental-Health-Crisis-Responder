# app.py
# app.py
import streamlit as st
from dotenv import load_dotenv
import os
from utils.groq_client import query_groq

load_dotenv()

st.set_page_config(page_title="Mental Health Responder", page_icon="🧠", layout="centered")

# Custom CSS for calming design
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1506744038136-46273834b3fb");
        background-size: cover;
        background-attachment: fixed;
    }
    .crisis-box {
        background-color: #ffcccc;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧠 Mental Health Crisis Responder")
st.markdown("_I’m here to listen with care. What’s on your mind?_")

# Get Help Now button
if st.button("Get Help Now"):
    st.markdown(
        """
        <div class='crisis-box'>
        <strong>You're not alone.</strong> Please reach out to a crisis hotline or professional support:
        <ul>
            <li>US: Call or text 988 (Suicide & Crisis Lifeline)</li>
            <li>UK: Call Samaritans at 116 123 or text SHOUT to 85258</li>
            <li>India: Call AASRA at +91-9820466726</li>
            <li>Global: Visit www.crisistextline.org for more resources</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

# User input
user_input = st.text_area("Your message", placeholder="Type how you're feeling...", height=150)

if st.button("Send") and user_input:
    with st.spinner("Responding compassionately..."):
        reply, emotion, is_crisis, resource_message = query_groq(user_input)
        st.markdown(f"### 💬 Response ({emotion})")
        st.success(reply)
        if is_crisis:
            st.markdown(
                f"<div class='crisis-box'><strong>We care about you.</strong> {resource_message}</div>",
                unsafe_allow_html=True,
            )