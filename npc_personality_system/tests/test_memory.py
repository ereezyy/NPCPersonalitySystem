import unittest
from npc_personality_system.core.memory import Memory

class TestMemory(unittest.TestCase):
    def test_add_event_and_recall(self):
        m = Memory(capacity=10)
        m.add_event("Saw a cat", importance=0.1, tags=["animal", "sighting"])
        m.add_event("Fought a goblin", importance=0.9, tags=["combat", "enemy", "goblin"])
        m.add_event("Found a coin", importance=0.2, tags=["item", "loot"])

        # Test recall with tag
        animal_events = m.recall("animal")
        self.assertEqual(len(animal_events), 1)
        self.assertEqual(animal_events[0].description, "Saw a cat")

        # Test recall with no matching tag
        dragon_events = m.recall("dragon")
        self.assertEqual(len(dragon_events), 0)

        # Test recall all
        all_events = m.recall()
        self.assertEqual(len(all_events), 3)

    def test_eviction(self):
        m = Memory(capacity=3)
        m.add_event("Event 1", importance=0.5, tags=["t1"])
        m.add_event("Event 2", importance=0.6, tags=["t2"])
        m.add_event("Event 3", importance=0.7, tags=["t3"])

        # Now add a 4th event, should evict the least important one (Event 1)
        m.add_event("Event 4", importance=0.8, tags=["t4"])

        self.assertEqual(len(m.events), 3)
        self.assertNotIn("Event 1", [item[2].description for item in m.events])

        # Check that it's removed from tag index
        self.assertEqual(len(m.recall("t1")), 0)
        self.assertEqual(len(m.recall("t4")), 1)

    def test_eviction_removes_from_all_tags(self):
        m = Memory(capacity=2)
        m.add_event("Low imp", importance=0.1, tags=["shared_tag", "unique_tag_low"])
        m.add_event("Med imp", importance=0.5, tags=["shared_tag", "unique_tag_med"])

        # Add high importance event, evicting "Low imp"
        m.add_event("High imp", importance=0.9, tags=["unique_tag_high"])

        self.assertEqual(len(m.recall("shared_tag")), 1)
        self.assertEqual(m.recall("shared_tag")[0].description, "Med imp")
        self.assertEqual(len(m.recall("unique_tag_low")), 0)

if __name__ == '__main__':
    unittest.main()
