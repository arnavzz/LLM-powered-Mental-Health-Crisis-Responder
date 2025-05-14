import os
import requests
from utils.emotion_classifier import classify_emotion
from utils.safety import detect_crisis

def query_groq(user_input, conversation_history=None):
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    emotion = classify_emotion(user_input)
    
    
    is_crisis, resource_message = detect_crisis(user_input)
    
    #prompt
    prompt_style = {
        "Sadness 😢": (
            "Be deeply comforting and validate their pain. Suggest the 5-4-3-2-1 grounding technique: "
            "name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste."
        ),
        "Anger 😠": (
            "Use calm, de-escalating language. Suggest journaling: write down what’s upsetting you, "
            "then list one actionable step to address it."
        ),
        "Anxiety 😰": (
            "Be reassuring and emphasize safety. Suggest box breathing: inhale for 4 seconds, hold for 4, "
            "exhale for 4, hold for 4, repeat 4 times."
        ),
        "Happiness 🙂": (
            "Reflect their positivity and encourage self-care, like taking a moment to savor something they enjoy."
        ),
        "Gratitude 🙏": (
            "Celebrate their gratitude and suggest writing down three things they’re thankful for today."
        ),
        "Neutral 😐": (
            "Stay attentive, empathetic, and gently explore their feelings. Suggest a mindfulness exercise: "
            "focus on your breath for 30 seconds."
        )
    }
    
    prompt_prefix = prompt_style.get(emotion, "Be kind and attentive.")
    
    if is_crisis:
        prompt_prefix = (
            "The user may be in crisis. Respond with extreme care, validate their feelings, "
            "and gently encourage seeking professional help. Include this resource: " + resource_message
        )
    
    # Include conversation
    history_prompt = ""
    if conversation_history:
        history_prompt = "Previous conversation context:\n" + "\n".join(
            [f"User: {msg['user']}\nAssistant: {msg['assistant']}" for msg in conversation_history]
        ) + "\n\n"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    system_prompt = (
        f"You are a compassionate mental health companion. {prompt_prefix} "
        "Never diagnose or give medical advice. Respond in a warm, non-judgmental tone, "
        "mirroring the user’s emotional state. If appropriate, weave in the suggested coping strategy naturally. "
        f"{history_prompt}Current user message:"
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