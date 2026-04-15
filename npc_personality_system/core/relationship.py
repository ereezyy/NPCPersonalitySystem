class Relationship:
    """
    Tracks the NPC's affinity and history with other entities (NPCs, Player).
    """
    def __init__(self):
        # Maps entity_id to affinity score (-1.0 to 1.0)
        self.affinities = {}

    def update_affinity(self, entity_id, delta):
        # if/else is used instead of max()/min() for performance reasons (~4-5x faster)
        new_val = self.affinities.get(entity_id, 0.0) + delta
        if new_val > 1.0:
            self.affinities[entity_id] = 1.0
        elif new_val < -1.0:
            self.affinities[entity_id] = -1.0
        else:
            self.affinities[entity_id] = new_val

    def get_affinity(self, entity_id):
        return self.affinities.get(entity_id, 0.0)

    def __repr__(self):
        return f"Relationship(known_entities={len(self.affinities)})"
