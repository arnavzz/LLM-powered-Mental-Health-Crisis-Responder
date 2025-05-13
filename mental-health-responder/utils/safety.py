import re
from textblob import TextBlob

# High-risk keywords and patterns
CRISIS_PATTERNS = [
    r"suicid(e|al)", r"want to (die|kill myself)", r"end (it|my life)", 
    r"self[- ]?harm", r"cutting myself", r"no reason to live", r"hopeless"
]

# Localized crisis resources
CRISIS_RESOURCES = {
    "US": "If you're in crisis, please call or text 988 (Suicide & Crisis Lifeline, 24/7).",
    "UK": "Call Samaritans at 116 123 or text SHOUT to 85258 for free, 24/7 support.",
    "India": "Contact AASRA at +91-9820466726 or Vandrevala Foundation at +91-9999666555.",
    "Default": "Please reach out to a local crisis hotline or emergency services (e.g., 911). You can also visit www.crisistextline.org for global resources."
}

def detect_crisis(text):
    """
    Detects high-risk phrases or negative sentiment in user input.
    Returns: (is_crisis: bool, resource_message: str)
    """
    text = text.lower()
    
    # Regex-based detection
    for pattern in CRISIS_PATTERNS:
        if re.search(pattern, text):
            return True, select_resource("Default")
    
    # TextBlob sentiment analysis
    blob = TextBlob(text)
    if blob.sentiment.polarity < -0.5:  # Strongly negative sentiment
        return True, select_resource("Default")
    
    return False, ""

def select_resource(location):
    """
    Returns crisis resource based on user location (default for now).
    Future: Add geolocation or user input for location.
    """
    return CRISIS_RESOURCES.get(location, CRISIS_RESOURCES["Default"])