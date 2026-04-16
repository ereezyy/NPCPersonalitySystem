class Relationship:
    """
    Tracks the NPC's affinity and history with other entities (NPCs, Player).
    """
    def __init__(self):
        # Maps entity_id to affinity score (-1.0 to 1.0)
        self.affinities = {}

    def update_affinity(self, entity_id, delta):
        val = self.affinities.get(entity_id, 0.0) + delta
        if val > 1.0:
            self.affinities[entity_id] = 1.0
        elif val < -1.0:
            self.affinities[entity_id] = -1.0
        else:
            self.affinities[entity_id] = val

    def get_affinity(self, entity_id):
        return self.affinities.get(entity_id, 0.0)

    def __repr__(self):
        return f"Relationship(known_entities={len(self.affinities)})"
