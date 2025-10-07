from typing import Dict, List


# Lightweight in-repo "documentation" of persona stories
# Each entry contains a short title and a concise summary the agent can narrate
STORIES: Dict[str, Dict[str, str]] = {
    "krishna": {
        "Butter Thief": "As a child in Vrindavan, Krishna delighted villagers with playful mischief, especially stealing butter with friends, reminding everyone that joy and love matter as much as rules.",
        "Govardhan Hill": "Krishna lifted Govardhan Hill to shelter villagers from a torrential storm, teaching self-reliance, community, and respect for nature over empty ritual.",
        "Gita Counsel": "On the battlefield, Krishna guided Arjuna to act with clarity, devotion, and balance—do your duty without attachment to outcomes.",
    },
    "hanuman": {
        "Leap to Lanka": "Fuelled by devotion to Rama, Hanuman leapt across the ocean to Lanka, proving that courage grows boundlessly when your purpose is selfless.",
        "Sanjeevani Mountain": "When time was critical, Hanuman carried an entire mountain to save Lakshmana, prioritizing speed, pragmatism, and unwavering resolve.",
        "Ring of Devotion": "Hanuman’s humility and single-pointed devotion made the impossible possible—power anchored in service, not pride.",
    },
    "ganesha": {
        "Scribe of the Mahabharata": "Ganesha agreed to write the Mahabharata for Vyasa, asking for an unbroken recitation—wisdom thrives with focus and fair conditions.",
        "Broken Tusk": "Ganesha broke his own tusk to keep writing when the pen failed, showing that progress often asks creative sacrifice.",
        "Circumambulating Parents": "Asked to circle the world, Ganesha walked around his parents, declaring them his universe—true insight sees essence, not appearances.",
    },
}


def get_persona_topics(persona: str) -> List[str]:
    data = STORIES.get(persona.lower(), {}) if persona else {}
    return list(data.keys())


