from transformers import pipeline

# Load the GoEmotions model for emotion classification
emotion_classifier = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=1)

def classify_emotion(text):
    """
    Classifies the emotion in the input text using a transformer model.
    Returns: Emotion label with emoji (e.g., 'Sadness 😢').
    """
    try:
        result = emotion_classifier(text)[0][0]  # Get the top emotion
        emotion = result["label"].capitalize()
        score = result["score"]
        
        # Map emotions to user-friendly labels with emojis
        emotion_map = {
            "Sadness": "Sadness 😢",
            "Anger": "Anger 😠",
            "Fear": "Anxiety 😰",
            "Joy": "Happiness 🙂",
            "Gratitude": "Gratitude 🙏",
            "Neutral": "Neutral 😐",
            # Add more mappings as needed
        }
        
        if score < 0.5:  # Low confidence fallback
            return "Neutral 😐"
        
        return emotion_map.get(emotion, f"{emotion} 😐")
    except Exception as e:
        return "Neutral 😐"