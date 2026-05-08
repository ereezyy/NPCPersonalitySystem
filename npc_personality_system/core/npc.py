from .personality import Personality
from .emotion import EmotionState
from .memory import Memory
from .relationship import Relationship

class NPC:
    """
    Main class representing a Non-Player Character.
    Integrates Personality, EmotionState, Memory, and Relationships.
    """
    __slots__ = ('name', 'personality', 'emotions', 'memory', 'relationships')

    def __init__(self, name, personality=None):
        self.name = name
        self.personality = personality or Personality()
        self.emotions = EmotionState()
        self.memory = Memory()
        self.relationships = Relationship()

    def interact(self, entity_id, action, context=None):
        """
        Process an interaction with another entity.
        The NPC will react based on its personality, current emotional state,
        past memories, and relationship with the entity.
        """
        # A simple interaction logic for demonstration purposes
        reaction = "neutral"
        affinity = self.relationships.get_affinity(entity_id)

        if action == "greet":
            if affinity > 0.3:
                reaction = "friendly"
                self.emotions.update_emotion("joy", 0.1)
            elif affinity < -0.3:
                reaction = "hostile"
                self.emotions.update_emotion("anger", 0.1)
            else:
                if self.personality.extraversion > 0.6:
                    reaction = "warm"
                    self.emotions.update_emotion("joy", 0.05)
                else:
                    reaction = "reserved"

            self.memory.add_event(f"Was greeted by {entity_id}", importance=0.1, tags=("interaction", entity_id))

        elif action == "attack":
            reaction = "defensive"
            self.relationships.update_affinity(entity_id, -0.5)
            self.emotions.update_emotion("anger", 0.8)
            self.emotions.update_emotion("fear", 0.5)
            self.memory.add_event(f"Was attacked by {entity_id}", importance=0.9, tags=("combat", "negative", entity_id))

        elif action == "gift":
            reaction = "grateful"
            affinity_increase = 0.2
            if self.personality.agreeableness < 0.3:
                affinity_increase = 0.05 # Less agreeable NPCs are harder to please
            self.relationships.update_affinity(entity_id, affinity_increase)
            self.emotions.update_emotion("joy", 0.3)
            self.memory.add_event(f"Received a gift from {entity_id}", importance=0.4, tags=("interaction", "positive", entity_id))

        return {
            "reaction": reaction,
            "dominant_emotion": self.emotions.get_dominant_emotion(),
            "affinity": self.relationships.get_affinity(entity_id)
        }

    def __repr__(self):
        return f"NPC(name='{self.name}', {self.personality}, {self.emotions})"
