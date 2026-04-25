import time
import heapq
import itertools
from collections import defaultdict

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
        self.tag_index = defaultdict(set)
        self._counter = itertools.count()

    def add_event(self, description, importance=0.5, tags=None):
        if len(self.events) >= self.capacity:
            if not self.events or importance < self.events[0][0]:
                return

        event = MemoryEvent(description, importance, tags)
        heap_item = (importance, next(self._counter), event)

        if len(self.events) >= self.capacity:

            # If at capacity, use heappushpop to atomically add new and remove lowest priority.
            # This is more efficient and avoids tag indexing if the new event is the one removed.
            removed_item = heapq.heappushpop(self.events, heap_item)
            removed_event = removed_item[2]

            if removed_event is not event:
                # Add the new event's tags to index
                if event.tags:
                    for tag in event.tags:
                        self.tag_index[tag].add(event)

                # Remove the old event's tags from index
                if removed_event.tags:
                    for tag in removed_event.tags:
                        tag_set = self.tag_index.get(tag)
                        if tag_set is not None:
                            tag_set.discard(removed_event)
                            if not tag_set:
                                del self.tag_index[tag]
        else:
            heapq.heappush(self.events, heap_item)
            if event.tags:
                for tag in event.tags:
                    self.tag_index[tag].add(event)

    def recall(self, tag=None):
        """Recall memories, optionally filtered by a tag."""
        if tag:
            return list(self.tag_index.get(tag, []))
        return [item[2] for item in self.events]

    def __repr__(self):
        return f"Memory(events_count={len(self.events)})"
