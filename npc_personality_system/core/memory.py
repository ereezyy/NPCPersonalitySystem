import time
import heapq

class MemoryEvent:
    __slots__ = ('description', 'importance', 'tags', 'timestamp')

    def __init__(self, description, importance=0.5, tags=None):
        self.description = description
        self.importance = importance # 0.0 to 1.0, determines how long it's remembered
        self.tags = tags or []
        self.timestamp = time.time()

    def __lt__(self, other):
        return self.importance < other.importance if self.importance != other.importance else self.timestamp < other.timestamp

class Memory:
    """
    Handles storing and retrieving memories for an NPC.
    """
    def __init__(self, capacity=100):
        self.events = []
        self.capacity = capacity
        self.tag_index = {}

    def add_event(self, description, importance=0.5, tags=None):
        if len(self.events) >= self.capacity:
            if not self.events or importance < self.events[0].importance:
                return
            event = MemoryEvent(description, importance, tags)
            removed_event = heapq.heapreplace(self.events, event)

            if event.tags:
                for tag in event.tags:
                    if tag not in self.tag_index:
                        self.tag_index[tag] = set()
                    self.tag_index[tag].add(event)

            if removed_event.tags:
                for tag in removed_event.tags:
                    if tag in self.tag_index:
                        self.tag_index[tag].remove(removed_event)
                        if not self.tag_index[tag]:
                            del self.tag_index[tag]
        else:
            event = MemoryEvent(description, importance, tags)
            heapq.heappush(self.events, event)
            if event.tags:
                for tag in event.tags:
                    if tag not in self.tag_index:
                        self.tag_index[tag] = set()
                    self.tag_index[tag].add(event)

    def recall(self, tag=None):
        """Recall memories, optionally filtered by a tag."""
        if tag:
            return list(self.tag_index.get(tag, []))
        return list(self.events)

    def __repr__(self):
        return f"Memory(events_count={len(self.events)})"
