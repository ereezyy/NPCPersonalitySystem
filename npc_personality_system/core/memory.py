import heapq
import itertools

class MemoryEvent:
    __slots__ = ('description', 'importance', 'tags')

    def __init__(self, description, importance=0.5, tags=None):
        self.description = description
        self.importance = importance # 0.0 to 1.0, determines how long it's remembered
        self.tags = tags or []

class Memory:
    """
    Handles storing and retrieving memories for an NPC.
    """
    def __init__(self, capacity=100):
        self.events = []
        self.capacity = capacity
        self.tag_index = {}
        self._counter = itertools.count()

    def add_event(self, description, importance=0.5, tags=None):
        events = self.events
        capacity = self.capacity

        if len(events) >= capacity:
            if not events or importance < events[0][0]:
                return

            event = MemoryEvent(description, importance, tags)
            heap_item = (importance, next(self._counter), event)

            # If at capacity, use heappushpop to atomically add new and remove lowest priority.
            # This is more efficient and avoids tag indexing if the new event is the one removed.
            removed_item = heapq.heappushpop(events, heap_item)
            removed_event = removed_item[2]

            if removed_event is not event:
                tag_index = self.tag_index

                # Add the new event's tags to index
                if event.tags:
                    for tag in event.tags:
                        s = tag_index.get(tag)
                        if s is None:
                            s = set()
                            tag_index[tag] = s
                        s.add(event)

                # Remove the old event's tags from index
                if removed_event.tags:
                    for tag in removed_event.tags:
                        try:
                            s = tag_index[tag]
                            s.remove(removed_event)
                            if not s:
                                del tag_index[tag]
                        except KeyError:
                            pass
        else:
            event = MemoryEvent(description, importance, tags)
            heap_item = (importance, next(self._counter), event)

            heapq.heappush(events, heap_item)
            if event.tags:
                tag_index = self.tag_index
                for tag in event.tags:
                    s = tag_index.get(tag)
                    if s is None:
                        s = set()
                        tag_index[tag] = s
                    s.add(event)

    def recall(self, tag=None):
        """Recall memories, optionally filtered by a tag."""
        if tag:
            return list(self.tag_index.get(tag, []))
        return [item[2] for item in self.events]

    def __repr__(self):
        return f"Memory(events_count={len(self.events)})"
