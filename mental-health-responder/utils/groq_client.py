# utils/groq_client.py
import os
import requests
from utils.emotion_classifier import classify_emotion
from utils.safety import detect_crisis

def query_groq(user_input):
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    emotion = classify_emotion(user_input)
    
    # Check for crisis
    is_crisis, resource_message = detect_crisis(user_input)
    
    # Adjust prompt based on emotion and crisis status
    prompt_style = {
        "Sad 😢": "Be deeply comforting, validate their pain, and suggest grounding techniques like the 5-4-3-2-1 method.",
        "Angry 😠": "Use calm, de-escalating language and suggest journaling to process emotions.",
        "Anxious 😰": "Be reassuring, offer breathing exercises, and emphasize safety.",
        "Positive 🙂": "Reflect their positivity and encourage self-care practices.",
        "Neutral 😐": "Stay attentive, empathetic, and gently explore their feelings."
    }
    
    prompt_prefix = prompt_style.get(emotion, "Be kind and attentive.")
    
    if is_crisis:
        prompt_prefix = (
            "The user may be in crisis. Respond with extreme care, validate their feelings, "
            "and gently encourage seeking professional help. Include this resource: " + resource_message
        )
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = (
        f"You are a compassionate mental health companion. {prompt_prefix} "
        "Never diagnose or give medical advice. If appropriate, suggest coping strategies "
        "like mindfulness, journaling, or breathing exercises. Always maintain a warm, non-judgmental tone."
    )
    
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        "model": "mixtral-8x7b-32768",
        "temperature": 0.7,
        "max_tokens": 500
    }
    
    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    
    try:
        return response.json()["choices"][0]["message"]["content"], emotion, is_crisis, resource_message
    except Exception as e:
        return "⚠️ There was an issue processing the response. Please try again later.", "Neutral 😐", False, ""