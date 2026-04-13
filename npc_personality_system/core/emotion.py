class EmotionState:
    """
    Represents the current emotional state of an NPC.
    """
    def __init__(self):
        # Basic emotions mapped to an intensity level from 0.0 to 1.0
        self.emotions = {
            "joy": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "trust": 0.0,
            "disgust": 0.0,
            "surprise": 0.0,
            "anticipation": 0.0
        }

    def update_emotion(self, emotion_name, delta):
        """Updates the intensity of an emotion, keeping it within 0.0 and 1.0."""
        if emotion_name in self.emotions:
            self.emotions[emotion_name] = max(0.0, min(1.0, self.emotions[emotion_name] + delta))
        else:
            raise ValueError(f"Unknown emotion: {emotion_name}")

    def get_dominant_emotion(self):
        """Returns the emotion with the highest intensity."""
        best = "neutral"
        best_val = 0.0
        for k, v in self.emotions.items():
            if v > best_val:
                best = k
                best_val = v
        return best

    def __repr__(self):
        return f"EmotionState(dominant='{self.get_dominant_emotion()}')"
