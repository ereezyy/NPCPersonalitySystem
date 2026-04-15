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
        self._dominant = "neutral"
        self._dominant_val = 0.0

    def update_emotion(self, emotion_name, delta):
        """Updates the intensity of an emotion, keeping it within 0.0 and 1.0."""
        if not delta:
            return

        try:
            curr_val = self.emotions[emotion_name]
        except KeyError:
            raise ValueError(f"Unknown emotion: {emotion_name}")

        new_val = curr_val + delta
        if new_val > 1.0:
            new_val = 1.0
        elif new_val < 0.0:
            new_val = 0.0

        if new_val == curr_val:
            return

        self.emotions[emotion_name] = new_val

        # Cache the dominant emotion
        if new_val > self._dominant_val:
            self._dominant = emotion_name
            self._dominant_val = new_val
        elif emotion_name == self._dominant and new_val < self._dominant_val:
            # The dominant emotion decreased, recalculate
            best = "neutral"
            best_val = 0.0
            for k, v in self.emotions.items():
                if v > best_val:
                    best = k
                    best_val = v
            self._dominant = best
            self._dominant_val = best_val

    def get_dominant_emotion(self):
        """Returns the emotion with the highest intensity."""
        return self._dominant

    def __repr__(self):
        return f"EmotionState(dominant='{self.get_dominant_emotion()}')"
