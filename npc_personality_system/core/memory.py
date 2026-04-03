import time
import heapq

class MemoryEvent:
    def __init__(self, description, importance=0.5, tags=None):
        self.description = description
        self.importance = importance # 0.0 to 1.0, determines how long it's remembered
        self.tags = tags or []
        self.timestamp = time.time()

    def __lt__(self, other):
        return (self.importance, self.timestamp) < (other.importance, other.timestamp)

class Memory:
    """
    Handles storing and retrieving memories for an NPC.
    """
    def __init__(self, capacity=100):
        self.events = []
        self.capacity = capacity

    def add_event(self, description, importance=0.5, tags=None):
        event = MemoryEvent(description, importance, tags)
        if len(self.events) < self.capacity:
            heapq.heappush(self.events, event)
        else:
            # Drop least important, oldest by keeping the heap at capacity
            heapq.heappushpop(self.events, event)

    def recall(self, tag=None):
        """Recall memories, optionally filtered by a tag."""
        if tag:
            return [e for e in self.events if tag in e.tags]
        return self.events

    def __repr__(self):
        return f"Memory(events_count={len(self.events)})"
