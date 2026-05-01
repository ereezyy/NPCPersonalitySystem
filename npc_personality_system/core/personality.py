class Personality:
    __slots__ = ('openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism')
    """
    Represents the core personality traits of an NPC using the OCEAN model.
    Traits are typically mapped from 0.0 to 1.0.
    """
    def __init__(self, openness=0.5, conscientiousness=0.5, extraversion=0.5, agreeableness=0.5, neuroticism=0.5):
        self.openness = openness
        self.conscientiousness = conscientiousness
        self.extraversion = extraversion
        self.agreeableness = agreeableness
        self.neuroticism = neuroticism

    def __repr__(self):
        return f"Personality(O={self.openness:.2f}, C={self.conscientiousness:.2f}, E={self.extraversion:.2f}, A={self.agreeableness:.2f}, N={self.neuroticism:.2f})"
