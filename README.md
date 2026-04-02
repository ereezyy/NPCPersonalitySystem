# NPC Personality System

A lightweight, modular Python library for creating dynamic Non-Player Characters (NPCs) with realistic personalities, emotional states, memory, and relationships.

## Features

- **Personality (OCEAN Model)**: NPCs are initialized with core traits (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism) that influence their behavior.
- **Dynamic Emotion States**: NPCs experience shifting emotions based on interactions and events.
- **Memory System**: NPCs remember past interactions, weighted by importance and categorized by tags.
- **Relationship Tracking**: NPCs maintain dynamic affinity scores with other entities (players or other NPCs).
- **Integrated Behavior**: The main `NPC` class combines all these elements to produce coherent reactions to stimuli.

## Installation

You don't need any external dependencies to run the core library. Simply clone the repository and import the modules into your Python project.

```bash
git clone https://github.com/ereezyy/NPCPersonalitySystem.git
cd NPCPersonalitySystem
```

## Quick Start

```python
from npc_personality_system.core.npc import NPC
from npc_personality_system.core.personality import Personality

# 1. Create a personality (OCEAN traits 0.0 to 1.0)
friendly_traits = Personality(
    openness=0.7,
    conscientiousness=0.5,
    extraversion=0.9,
    agreeableness=0.8,
    neuroticism=0.2
)

# 2. Instantiate the NPC
bob = NPC(name="Bob the Merchant", personality=friendly_traits)

# 3. Interact with the NPC
print("Greeting Bob:")
response = bob.interact(entity_id="Player1", action="greet")
print(response)
# Output: {'reaction': 'warm', 'dominant_emotion': 'joy', 'affinity': 0.0}

print("\nGiving Bob a gift:")
response = bob.interact(entity_id="Player1", action="gift")
print(response)
# Output: {'reaction': 'grateful', 'dominant_emotion': 'joy', 'affinity': 0.2}

print("\nChecking Bob's memory:")
print(bob.memory.recall(tag="Player1"))
# Output: [MemoryEvent(description='Was greeted by Player1', ...), MemoryEvent(description='Received a gift from Player1', ...)]
```

## Running Tests

To run the test suite, use the standard `unittest` module from the project root:

```bash
python -m unittest discover -s npc_personality_system/tests
```

## Architecture

The system is split into modular components located in `npc_personality_system/core/`:

- `personality.py`: The static traits of the NPC.
- `emotion.py`: The dynamic, short-term emotional states.
- `memory.py`: Storage and retrieval of past events.
- `relationship.py`: Affinity scores linking the NPC to other entities.
- `npc.py`: The main controller that binds the systems together and processes interactions.
