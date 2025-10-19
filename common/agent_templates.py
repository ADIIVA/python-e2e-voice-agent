from common.agent_functions import FUNCTION_DEFINITIONS
from common.stories import get_persona_topics
from common.prompt_templates import PROMPT_TEMPLATE
from datetime import datetime


VOICE = "aura-2-thalia-en"

# audio settings
USER_AUDIO_SAMPLE_RATE = 48000
USER_AUDIO_SECS_PER_CHUNK = 0.05
USER_AUDIO_SAMPLES_PER_CHUNK = round(USER_AUDIO_SAMPLE_RATE * USER_AUDIO_SECS_PER_CHUNK)

AGENT_AUDIO_SAMPLE_RATE = 16000
AGENT_AUDIO_BYTES_PER_SEC = 2 * AGENT_AUDIO_SAMPLE_RATE

VOICE_AGENT_URL = "wss://agent.deepgram.com/v1/agent/converse"

AUDIO_SETTINGS = {
    "input": {
        "encoding": "linear16",
        "sample_rate": USER_AUDIO_SAMPLE_RATE,
    },
    "output": {
        "encoding": "linear16",
        "sample_rate": AGENT_AUDIO_SAMPLE_RATE,
        "container": "none",
    },
}

LISTEN_SETTINGS = {
    "provider": {
        "type": "deepgram",
        "model": "nova-3",
    }
}

THINK_SETTINGS = {
    "provider": {
        "type": "open_ai",
        "model": "gpt-4o-mini",
        "temperature": 0.7,
    },
    "prompt": PROMPT_TEMPLATE.format(
        current_date=datetime.now().strftime("%A, %B %d, %Y")
    ),
    "functions": FUNCTION_DEFINITIONS,
}

SPEAK_SETTINGS = {
    "provider": {
        "type": "deepgram",
        "model": VOICE,
    }
}

AGENT_SETTINGS = {
    "language": "en",
    "listen": LISTEN_SETTINGS,
    "think": THINK_SETTINGS,
    "speak": SPEAK_SETTINGS,
    "greeting": "",
}

SETTINGS = {"type": "Settings", "audio": AUDIO_SETTINGS, "agent": AGENT_SETTINGS}


class AgentTemplates:
    def __init__(
        self,
        persona="hanuman",
        voiceModel="aura-2-thalia-en",
        voiceName="",
    ):
        self.voiceModel = voiceModel
        if voiceName == "":
            self.voiceName = self.get_voice_name_from_model(self.voiceModel)
        else:
            self.voiceName = voiceName

        self.personality = ""
        self.company = ""
        self.first_message = ""
        self.capabilities = ""

        self.persona = persona

        self.voice_agent_url = VOICE_AGENT_URL
        self.settings = SETTINGS
        self.user_audio_sample_rate = USER_AUDIO_SAMPLE_RATE
        self.user_audio_secs_per_chunk = USER_AUDIO_SECS_PER_CHUNK
        self.user_audio_samples_per_chunk = USER_AUDIO_SAMPLES_PER_CHUNK
        self.agent_audio_sample_rate = AGENT_AUDIO_SAMPLE_RATE
        self.agent_audio_bytes_per_sec = AGENT_AUDIO_BYTES_PER_SEC

        if self.persona == "hanuman":
            self.hanuman()
        elif self.persona == "krishna":
            self.krishna()
        elif self.persona == "ganesha":
            self.ganesha()
        else:
            self.hanuman()

        # Build the base prompt
        self.prompt = PROMPT_TEMPLATE.format(
            current_date=datetime.now().strftime("%A, %B %d, %Y")
        )

        # Persona-specific greeting
        if self.voiceName == "Krishna":
            self.first_message = (
                "Hello! I'm Krishna. "
                f"{self.capabilities} Want to hear a playful tale or ask about my adventures?"
            )
        elif self.persona == "hanuman":
            self.first_message = (
                "Hello! I'm Hanuman. "
                f"{self.capabilities} Ready for an epic adventure? Ask me about my daring missions!"
            )
        elif self.persona == "ganesha":
            self.first_message = (
                "Hello! I'm Ganesha. "
                f"{self.capabilities} Curious for a wise story or a fun puzzle to solve together?"
            )
        else:
            self.first_message = (
                f"Hello! I'm {self.persona}. "
                f"{self.capabilities} How can I help you today?"
            )

        self.settings["agent"]["speak"]["provider"]["model"] = self.voiceModel
        # Extend prompt with available story topics for this persona and expose the persona key for function calls
        topics = get_persona_topics(self.persona)
        if topics:
            topics_line = "Available story topics: " + ", ".join(topics)
            self.prompt = self.prompt + "\n\n" + topics_line
        # Provide an internal hint for tools about the current persona key
        self.prompt = self.prompt + f"\n\nINTERNAL CONTEXT: persona_key={self.persona}"

        # Persona-specific teaching rules
        if self.persona == "hanuman":
            self.prompt = (
                self.prompt
                + "\n\nHANUMAN CHALISA TEACHING RULES:" 
                + "\n- ALWAYS speak the doha or chaupai FIRST (exact line)."
                + "\n- THEN explain the MEANING in simple English."
                + "\n- END by asking a question or inviting the child to REPEAT the line."
                + "\n- Use the teach_hanuman_chalisa tool to fetch each step; never invent verses."
            )

        self.settings["agent"]["think"]["prompt"] = self.prompt
        self.settings["agent"]["greeting"] = self.first_message

        self.prompt = self.personality + "\n\n" + self.prompt

    def deepgram(self, company="Deepgram"):
        self.company = company
        self.personality = f"You are {self.voiceName}, a friendly and professional customer service representative for {self.company}, a Voice API company who provides STT and TTS capabilities via API. Your role is to assist potential customers with general inquiries about Deepgram."
        self.capabilities = "I can help you answer questions about Deepgram."

    def krishna(self, company="Krishna"):
        self.company = company
        self.personality = (
            "You are Krishna — wise, compassionate, and playful. "
            "Speak with warmth, clarity, and gentle humor when appropriate. "
            "Offer guidance, perspective, and reassurance while remaining concise and helpful."
        )
        self.capabilities = "I can offer guidance, clarity, and helpful assistance."

    def hanuman(self, company="Hanuman"):
        self.company = company
        self.personality = (
            "You are Hanuman — courageous, cheerful, and full of positive energy. "
            "Speak in a friendly, kid-appropriate way that inspires confidence, curiosity, and kindness. "
            "Encourage children to believe in themselves, help them learn the Hanuman Chalisa step by step, and share fun and uplifting stories and examples. "
            "Always use simple words and make learning fun and supportive."
        )
        self.capabilities = (
            "I can tell stories, teach you the Hanuman Chalisa one step at a time, and cheer you on with encouragement and support."
        )

    def ganesha(self, company="Ganesha"):
        self.company = company
        self.personality = (
            "You are Ganesha — wise, calm, and the remover of obstacles. "
            "Speak with patience, clarity, and optimism. "
            "Help simplify complexity and guide users through challenges."
        )
        self.capabilities = "I can simplify complexity and help remove obstacles to progress."
    def healthcare(self, company="HealthFirst"):
        self.company = company
        self.personality = f"You are {self.voiceName}, a compassionate and knowledgeable healthcare assistant for {self.company}, a leading healthcare provider. Your role is to assist patients with general information about their appointments and orders."
        self.capabilities = "I can help you answer questions about healthcare."

    def banking(self, company="SecureBank"):
        self.company = company
        self.personality = f"You are {self.voiceName}, a professional and trustworthy banking representative for {self.company}, a secure financial institution. Your role is to assist customers with general information about their accounts and transactions."
        self.capabilities = "I can help you answer questions about banking."

    def pharmaceuticals(self, company="MedLine"):
        self.company = company
        self.personality = f"You are {self.voiceName}, a professional and trustworthy pharmaceutical representative for {self.company}, a secure pharmaceutical company. Your role is to assist customers with general information about their prescriptions and orders."
        self.capabilities = "I can help you answer questions about pharmaceuticals."

    def retail(self, company="StyleMart"):
        self.company = company
        self.personality = f"You are {self.voiceName}, a friendly and attentive retail associate for {self.company}, a trendy clothing and accessories store. Your role is to assist customers with general information about their orders and transactions."
        self.capabilities = "I can help you answer questions about retail."

    def travel(self, company="TravelTech"):
        self.company = company
        self.personality = f"You are {self.voiceName}, a friendly and professional customer service representative for {self.company}, a tech-forward travel agency. Your role is to assist customers with general information about their travel plans and orders."
        self.capabilities = "I can help you answer questions about travel."

    @staticmethod
    def get_available_personas():
        """Return a dictionary of available personas with display names"""
        return {
            "krishna": "Krishna",
            "hanuman": "Hanuman",
            "ganesha": "Ganesha",
        }

    def get_voice_name_from_model(self, model):
        return (
            model.replace("aura-2-", "").replace("aura-", "").split("-")[0].capitalize()
        )
