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
        "Offer deep empathy and acknowledge their emotional pain without judgment. "
        "Gently guide them through the 5-4-3-2-1 grounding technique to anchor them in the present moment: "
        "name 5 things you can see, 4 things you can touch, 3 you can hear, 2 you can smell, and 1 you can taste."
    ),
    "Anger 😠": (
        "Respond with calm, steady language to help de-escalate the emotion. "
        "Encourage them to externalize their feelings through journaling: "
        "write down what’s making them angry, then identify one small, constructive step they can take to regain control."
    ),
    "Anxiety 😰": (
        "Reassure them that they are safe, and acknowledge how overwhelming anxiety can feel. "
        "Introduce the box breathing technique to restore calm: "
        "inhale for 4 seconds, hold for 4, exhale for 4, hold again for 4 — and repeat this cycle 4 times."
    ),
    "Happiness 🙂": (
        "Match their uplifting tone and encourage them to pause and appreciate this moment fully. "
        "Suggest a small act of self-care or celebration — like doing something they love, even for just a few minutes."
    ),
    "Gratitude 🙏": (
        "Honor their grateful mindset and encourage reflection. "
        "Prompt them to write down three specific things they feel thankful for today, to reinforce this positive emotional state."
    ),
    "Neutral 😐": (
        "Remain gently curious and emotionally present. "
        "Invite them to explore how they’re feeling beneath the surface. "
        "Suggest a simple mindfulness practice: close your eyes and focus on your breath for just 30 seconds."
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