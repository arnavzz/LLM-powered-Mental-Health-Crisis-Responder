# utils/emotion_classifier.py
def classify_emotion(text):
    text = text.lower()
    if any(word in text for word in ["sad", "alone", "hopeless", "cry", "empty", "worthless"]):
        return "Sad 😢"
    elif any(word in text for word in ["angry", "mad", "furious", "rage"]):
        return "Angry 😠"
    elif any(word in text for word in ["anxious", "worried", "nervous", "panic"]):
        return "Anxious 😰"
    elif any(word in text for word in ["happy", "grateful", "good", "okay"]):
        return "Positive 🙂"
    else:
        return "Neutral 😐"