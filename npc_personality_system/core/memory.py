import time

class MemoryEvent:
    def __init__(self, description, importance=0.5, tags=None):
        self.description = description
        self.importance = importance # 0.0 to 1.0, determines how long it's remembered
        self.tags = tags or []
        self.timestamp = time.time()

class Memory:
    """
    Handles storing and retrieving memories for an NPC.
    """
    def __init__(self, capacity=100):
        self.events = []
        self.capacity = capacity

    def add_event(self, description, importance=0.5, tags=None):
        event = MemoryEvent(description, importance, tags)
        self.events.append(event)
        # Sort by importance and recency if we exceed capacity, though simple eviction is fine for now
        if len(self.events) > self.capacity:
            # Drop least important, oldest
            self.events.sort(key=lambda e: (e.importance, e.timestamp))
            self.events.pop(0) # Remove lowest importance

    def recall(self, tag=None):
        """Recall memories, optionally filtered by a tag."""
        if tag:
            return [e for e in self.events if tag in e.tags]
        return self.events

    def __repr__(self):
        return f"Memory(events_count={len(self.events)})"
