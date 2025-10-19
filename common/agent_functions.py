from .business_logic import (
    prepare_agent_filler_message,
    prepare_farewell_message,
)
from .stories import STORIES
import os
import wave
from .hanuman_chalisa import HANUMAN_CHALISA_STEPS

# Base directory for audio assets; can be set via env var
AUDIO_BASE_DIR = os.environ.get("AUDIO_BASE_DIR", "/Users/admin/Desktop/projects/flask-agent-function-calling-demo/common")

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


async def teach_hanuman_chalisa(params):
    """Teach Hanuman Chalisa step-by-step. Only for persona 'hanuman'.

    Params:
    - persona: must be 'hanuman'
    - step_index: optional integer (0-based). If omitted, start from 0.
    """
    persona = (params.get("persona") or "").lower()
    step_index = params.get("step_index")

    if persona != "hanuman":
        return {
            "error": "unsupported_persona",
            "message": "This function is only available for the Hanuman persona.",
        }

    steps = HANUMAN_CHALISA_STEPS
    total = len(steps)
    index = step_index if isinstance(step_index, int) and 0 <= step_index < total else 0

    step = steps[index]
    next_index = index + 1 if index + 1 < total else None

    # Teaching pattern: playback (if available) -> say verse -> meaning in English -> ask a question / repeat
    engage = "Would you like to repeat this line with me?"
    verse_line = step.get("text_english") or step.get("text_hindi") or ""
    meaning_en = step.get("translation_english") or ""

    # Resolve playback path if present (support absolute or relative under AUDIO_BASE_DIR)
    playback = step.get("playback_audio_path")
    if playback and not os.path.isabs(playback):
        playback = os.path.join(AUDIO_BASE_DIR, playback)
    
    print(f"playback: {playback}")

    speech = (
        ("Title: " + step["title"] + "\n")
        + ("Text in English: " + step.get("text_english") + "\n")
        + ("Translation in English: " + step["translation_english"] + "\n")
        + ("Learning in English: " + step["learning_english"] + "\n")
        + f"Now, {engage}"
    )

    return {
        "persona": persona,
        "index": index,
        "total": total,
        "output": speech,
        "next_step_index": next_index,
    }


async def play_hanuman_chalisa(params):
    """Play a Hanuman Chalisa audio file (browser playback). Only for persona 'hanuman'.

    Params:
    - persona: must be 'hanuman'
    - path: absolute or relative path (under AUDIO_BASE_DIR) to a mono 16kHz PCM WAV file
    """
    persona = (params.get("persona") or "").lower()
    audio_path = params.get("path")

    if persona != "hanuman":
        return {
            "error": "unsupported_persona",
            "message": "This function is only available for the Hanuman persona.",
        }

    if not audio_path or not isinstance(audio_path, str):
        return {"error": "invalid_path", "message": "Provide 'path' to an audio file"}

    # Resolve relative paths
    if not os.path.isabs(audio_path):
        audio_path = os.path.join(AUDIO_BASE_DIR, audio_path)

    if not os.path.exists(audio_path):
        return {"error": "not_found", "message": f"File not found: {audio_path}"}

    # Only wav PCM is streamed sample-perfect; for mp3, return metadata to let UI/server handle decoding later
    ext = os.path.splitext(audio_path)[1].lower()
    if ext != ".wav":
        return {
            "persona": persona,
            "path": audio_path,
            "format": ext.lstrip("."),
            "note": "Non-WAV provided; client/server should decode to PCM for playback",
        }

    try:
        with wave.open(audio_path, "rb") as wf:
            nchannels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            comptype = wf.getcomptype()

            if comptype != "NONE":
                return {"error": "unsupported_format", "message": "Compressed WAV not supported"}
            if nchannels != 1 or sampwidth != 2 or framerate != 16000:
                return {
                    "error": "unsupported_format",
                    "message": "Audio must be mono 16-bit PCM at 16000 Hz",
                }

            frames_per_chunk = 16000
            chunks = []
            while True:
                frames = wf.readframes(frames_per_chunk)
                if not frames:
                    break
                chunks.append(frames)

        return {
            "persona": persona,
            "path": audio_path,
            "audio_chunks": chunks,
            "sample_rate": 16000,
        }
    except Exception as e:
        return {"error": "read_error", "message": str(e)}

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
    {
        "name": "teach_hanuman_chalisa",
        "description": "Teach the Hanuman Chalisa step-by-step (Hanuman persona only). Return one step at a time with optional playback path, then verse, meaning in English, and an engagement prompt.",
        "parameters": {
            "type": "object",
            "properties": {
                "persona": {
                    "type": "string",
                    "description": "Must be 'hanuman'",
                    "enum": ["hanuman"],
                },
                "step_index": {
                    "type": "integer",
                    "description": "0-based index for the step; omit to start from the beginning",
                },
            },
            "required": ["persona"],
        },
    },
    # {
    #     "name": "play_hanuman_chalisa",
    #     "description": "Play a Hanuman Chalisa audio file to the user (Hanuman persona only). Accepts absolute or relative path (under AUDIO_BASE_DIR).",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "persona": {
    #                 "type": "string",
    #                 "description": "Must be 'hanuman'",
    #                 "enum": ["hanuman"],
    #             },
    #             "path": {
    #                 "type": "string",
    #                 "description": "Path to audio file. WAV is streamed; other formats returned for client decoding.",
    #             },
    #         },
    #         "required": ["persona", "path"],
    #     },
    # },
]

# Map function names to their implementations
FUNCTION_MAP = {
    "agent_filler": agent_filler,
    "tell_a_story": tell_a_story,
    "teach_hanuman_chalisa": teach_hanuman_chalisa
    # "play_hanuman_chalisa": play_hanuman_chalisa,
}
