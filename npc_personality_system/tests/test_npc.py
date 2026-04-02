import unittest
from npc_personality_system.core.npc import NPC
from npc_personality_system.core.personality import Personality

class TestNPC(unittest.TestCase):
    def setUp(self):
        # Create an agreeable and extraverted NPC
        self.friendly_personality = Personality(agreeableness=0.8, extraversion=0.8)
        self.npc = NPC(name="Bob", personality=self.friendly_personality)

    def test_initialization(self):
        self.assertEqual(self.npc.name, "Bob")
        self.assertEqual(self.npc.emotions.get_dominant_emotion(), "neutral")
        self.assertEqual(self.npc.relationships.get_affinity("Player1"), 0.0)

    def test_interaction_greet(self):
        result = self.npc.interact("Player1", "greet")
        self.assertEqual(result["reaction"], "warm")
        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(len(self.npc.memory.recall(tag="interaction")), 1)

    def test_interaction_attack(self):
        result = self.npc.interact("Player1", "attack")
        self.assertEqual(result["reaction"], "defensive")
        self.assertEqual(result["dominant_emotion"], "anger")
        self.assertEqual(result["affinity"], -0.5)
        self.assertEqual(len(self.npc.memory.recall(tag="combat")), 1)

    def test_interaction_gift(self):
        result = self.npc.interact("Player1", "gift")
        self.assertEqual(result["reaction"], "grateful")
        self.assertEqual(result["dominant_emotion"], "joy")
        self.assertEqual(result["affinity"], 0.2)

    def test_grumpy_npc_gift(self):
        grumpy_personality = Personality(agreeableness=0.1)
        grumpy_npc = NPC(name="Grump", personality=grumpy_personality)
        result = grumpy_npc.interact("Player1", "gift")
        self.assertEqual(result["affinity"], 0.05) # Less affinity gained compared to agreeable NPC

if __name__ == '__main__':
    unittest.main()
