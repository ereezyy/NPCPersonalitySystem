import unittest
from npc_personality_system.core.memory import Memory

class TestMemory2(unittest.TestCase):
    def test_eviction_low_priority_item(self):
        m = Memory(capacity=3)
        m.add_event("Event 1", importance=0.5, tags=["t1"])
        m.add_event("Event 2", importance=0.6, tags=["t2"])
        m.add_event("Event 3", importance=0.7, tags=["t3"])

        # Now add a 4th event, but it has lower priority.
        # It shouldn't be added to the queue!
        m.add_event("Event 4", importance=0.1, tags=["t4"])

        self.assertEqual(len(m.events), 3)
        self.assertNotIn("Event 4", [item[2].description for item in m.events])
        self.assertEqual(len(m.recall("t4")), 0)
        self.assertIn("Event 1", [item[2].description for item in m.events])

if __name__ == '__main__':
    unittest.main()
