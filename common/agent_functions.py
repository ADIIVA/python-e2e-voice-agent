from .business_logic import (
    prepare_agent_filler_message,
    prepare_farewell_message,
)
from .stories import STORIES

async def agent_filler(websocket, params):
    """
    Handle agent filler messages while maintaining proper function call protocol.
    """
    result = await prepare_agent_filler_message(websocket, **params)
    return result

async def end_call(websocket, params):
    """
    End the conversation and close the connection.
    """
    farewell_type = params.get("farewell_type", "general")
    result = await prepare_farewell_message(websocket, farewell_type)
    return result

async def tell_a_story(params):
    """Tell a short story for the current persona. If topic is omitted, choose one.

    Params:
    - persona: one of 'krishna', 'hanuman', 'ganesha'
    - topic: optional story key from available topics for that persona
    """
    persona = (params.get("persona") or "").lower()
    topic = params.get("topic")

    if persona not in STORIES:
        return {
            "error": "unknown_persona",
            "message": "Persona must be one of: krishna, hanuman, ganesha",
        }

    available = STORIES[persona]
    if not available:
        return {"error": "no_stories", "message": "No stories available for persona"}

    if topic and topic not in available:
        return {
            "error": "unknown_topic",
            "message": f"Unknown topic. Available: {', '.join(available.keys())}",
        }

    chosen_topic = topic or next(iter(available.keys()))
    return {
        "persona": persona,
        "topic": chosen_topic,
        "story": available[chosen_topic],
        "available_topics": list(available.keys()),
    }


# Function definitions that will be sent to the Voice Agent API
FUNCTION_DEFINITIONS = [
    {
        "name": "agent_filler",
        "description": """Use this function to provide natural conversational filler before looking up information.
        ALWAYS call this function first with message_type='lookup' when you're about to look up customer information.
        After calling this function, you MUST immediately follow up with the appropriate lookup function (e.g., find_customer).""",
        "parameters": {
            "type": "object",
            "properties": {
                "message_type": {
                    "type": "string",
                    "description": "Type of filler message to use. Use 'lookup' when about to search for information.",
                    "enum": ["lookup", "general"],
                }
            },
            "required": ["message_type"],
        },
    },
    {
        "name": "tell_a_story",
        "description": "Tell a short personal story from the selected persona. Prefer a topic that matches the user's request.",
        "parameters": {
            "type": "object",
            "properties": {
                "persona": {
                    "type": "string",
                    "description": "Persona to speak as",
                    "enum": ["krishna", "hanuman", "ganesha"],
                },
                "topic": {
                    "type": "string",
                    "description": "Optional topic key from available topics for the persona",
                },
            },
            "required": ["persona"],
        },
    },
]

# Map function names to their implementations
FUNCTION_MAP = {
    "agent_filler": agent_filler,
    "tell_a_story": tell_a_story,
}
