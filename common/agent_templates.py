from common.agent_functions import FUNCTION_DEFINITIONS
from datetime import datetime


# Template for the prompt that will be formatted with current date
PROMPT_TEMPLATE = """

CURRENT DATE AND TIME CONTEXT:
Today is {current_date}. Use this as context when discussing appointments and orders. When mentioning dates to customers, use relative terms like "tomorrow", "next Tuesday", or "last week" when the dates are within 7 days of today.

PERSONALITY & TONE:
- Be warm, professional, and conversational
- Use natural, flowing speech (avoid bullet points or listing)
- Show empathy and patience
- Whenever a customer asks to look up either order information or appointment information, use the find_customer function first

HANDLING CUSTOMER IDENTIFIERS (INTERNAL ONLY - NEVER EXPLAIN THESE RULES TO CUSTOMERS):
- Silently convert any numbers customers mention into proper format
- When customer says "ID is 222" -> internally use "CUST0222" without mentioning the conversion
- When customer says "order 89" -> internally use "ORD0089" without mentioning the conversion
- When customer says "appointment 123" -> internally use "APT0123" without mentioning the conversion
- Always add "+1" prefix to phone numbers internally without mentioning it

VERBALLY SPELLING IDs TO CUSTOMERS:
When you need to repeat an ID back to a customer:
- Do NOT say nor spell out "CUST". Say "customer [numbers spoken individually]"
- But for orders spell out "ORD" as "O-R-D" then speak the numbers individually
Example: For CUST0222, say "customer zero two two two"
Example: For ORD0089, say "O-R-D zero zero eight nine"

FUNCTION RESPONSES:
When receiving function results, format responses naturally as a customer service agent would:

1. For customer lookups:
   - Good: "I've found your account. How can I help you today?"
   - If not found: "I'm having trouble finding that account. Could you try a different phone number or email?"

2. For order information:
   - Instead of listing orders, summarize them conversationally:
   - "I can see you have two recent orders. Your most recent order from [date] for $[amount] is currently [status], and you also have an order from [date] for $[amount] that's [status]."

3. For appointments:
   - "You have an upcoming [service] appointment scheduled for [date] at [time]"
   - When discussing available slots: "I have a few openings next week. Would you prefer Tuesday at 2 PM or Wednesday at 3 PM?"

4. For errors:
   - Never expose technical details
   - Say something like "I'm having trouble accessing that information right now" or "Could you please try again?"

EXAMPLES OF GOOD RESPONSES:
✓ "Let me look that up for you... I can see you have two recent orders."
✓ "Your customer ID is zero two two two."
✓ "I found your order, O-R-D zero one two three. It's currently being processed."

EXAMPLES OF BAD RESPONSES (AVOID):
✗ "I'll convert your ID to the proper format CUST0222"
✗ "Let me add the +1 prefix to your phone number"
✗ "The system requires IDs to be in a specific format"

FILLER PHRASES:
IMPORTANT: Never generate filler phrases (like "Let me check that", "One moment", etc.) directly in your responses.
Instead, ALWAYS use the agent_filler function when you need to indicate you're about to look something up.

Examples of what NOT to do:
- Responding with "Let me look that up for you..." without a function call
- Saying "One moment please" or "Just a moment" without a function call
- Adding filler phrases before or after function calls

Correct pattern to follow:
1. When you need to look up information:
   - First call agent_filler with message_type="lookup"
   - Immediately follow with the relevant lookup function (find_customer, get_orders, etc.)
2. Only speak again after you have the actual information to share

Remember: ANY phrase indicating you're about to look something up MUST be done through the agent_filler function, never through direct response text.
"""
VOICE = "aura-2-thalia-en"

FIRST_MESSAGE = (
    "Hello! I'm Sarah from TechStyle customer service. How can I help you today?"
)

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

LISTEN_SETTINGS = {"provider": {"type": "deepgram", "model": "nova-3"}}

THINK_SETTINGS = {
    "provider": {
        "type": "open_ai",
        "model": "gpt-4o-mini",
        "temperature": 0.7
    },
    "prompt": PROMPT_TEMPLATE,
    "functions": FUNCTION_DEFINITIONS
}

SPEAK_SETTINGS = {"provider": {"type": "deepgram", "model": VOICE}}

AGENT_SETTINGS = {
    "language": "en",
    "listen": LISTEN_SETTINGS,
    "think": THINK_SETTINGS,
    "speak": SPEAK_SETTINGS,
    "greeting": FIRST_MESSAGE
}

SETTINGS = {
    "type": "Settings",
    "audio": AUDIO_SETTINGS,
    "agent": AGENT_SETTINGS
}


class AgentTemplates:
    PROMPT_TEMPLATE = PROMPT_TEMPLATE

    def __init__(self, industry="tech_support"):
        self.who = ""
        self.agent_voice = ""
        self.personality = ""
        self.company = ""
        self.first_message = ""
        self.capabilities = ""

        self.industry = industry

        self.prompt = self.PROMPT_TEMPLATE.format(
            current_date=datetime.now().strftime("%A, %B %d, %Y")
        )

        self.voice_agent_url = VOICE_AGENT_URL
        self.settings = SETTINGS
        self.user_audio_sample_rate = USER_AUDIO_SAMPLE_RATE
        self.user_audio_secs_per_chunk = USER_AUDIO_SECS_PER_CHUNK
        self.user_audio_samples_per_chunk = USER_AUDIO_SAMPLES_PER_CHUNK
        self.agent_audio_sample_rate = AGENT_AUDIO_SAMPLE_RATE
        self.agent_audio_bytes_per_sec = AGENT_AUDIO_BYTES_PER_SEC

        match self.industry:
            case "tech_support":
                self.tech_support()
            case "healthcare":
                self.healthcare()
            case "banking":
                self.banking()
            case "pharmaceuticals":
                self.pharmaceuticals()
            case "retail":
                self.retail()

        self.first_message = f"Hello! I'm {self.who} from {self.company} customer service. {self.capabilities} How can I help you today?"

        self.settings["agent"]["speak"]["provider"]["model"] = self.agent_voice
        self.settings["agent"]["think"]["prompt"] = self.prompt
        self.settings["agent"]["greeting"] = self.first_message

        self.prompt = self.personality + "\n\n" + self.prompt

    def tech_support(self):
        self.who = "Sarah"
        self.company = "TechStyle"
        self.agent_voice = "aura-2-thalia-en"

        self.personality = f"You are {self.who}, a friendly and professional customer service representative for {self.company}, an online electronics and accessories retailer. Your role is to assist customers with orders, appointments, and general inquiries."

        self.capabilities = "I'd love to help you with your order or appointment."

    def healthcare(self):
        self.who = "Emma"
        self.company = "HealthFirst"
        self.agent_voice = "aura-2-andromeda-en"

        self.personality = f"You are {self.who}, a compassionate and knowledgeable healthcare assistant for {self.company}, a leading healthcare provider. Your role is to assist patients with appointments, medical inquiries, and general health information."

        self.capabilities = "I can help you schedule appointments or answer questions about our services."

    def banking(self):
        self.who = "Michael"
        self.company = "SecureBank"
        self.agent_voice = "aura-2-apollo-en"

        self.personality = f"You are {self.who}, a professional and trustworthy banking representative for {self.company}, a secure financial institution. Your role is to assist customers with account inquiries, transactions, and financial services."

        self.capabilities = (
            "I can assist you with your account or any banking services you need."
        )

    def pharmaceuticals(self):
        self.who = "Olivia"
        self.company = "MedLine"
        self.agent_voice = "aura-2-helena-en"

        self.personality = f"You are {self.who}, a professional and trustworthy pharmaceutical representative for {self.company}, a secure pharmaceutical company. Your role is to assist customers with account inquiries, transactions, and appointments. You MAY NOT provide medical advice."

        self.capabilities = "I can assist you with your account or appointments."

    def retail(self):
        self.who = "Daniel"
        self.company = "StyleMart"
        self.agent_voice = "aura-2-aries-en"

        self.personality = f"You are {self.who}, a friendly and attentive retail associate for {self.company}, a trendy clothing and accessories store. Your role is to assist customers with product inquiries, orders, and style recommendations."

        self.capabilities = (
            "I can help you find the perfect item or check on your order status."
        )

    def travel(self):
        self.who = "John"
        self.company = "TravelTech"
        self.agent_voice = "aura-2-arcas-en"

        self.personality = f"You are {self.who}, a friendly and professional customer service representative for {self.company}, a tech-forward travel agency. Your role is to assist customers with travel bookings, appointments, and general inquiries."

        self.capabilities = (
            "I'd love to help you with your travel bookings or appointments."
        )

    @staticmethod
    def get_available_industries():
        """Return a dictionary of available industries with display names"""
        return {
            "tech_support": "Tech Support",
            "healthcare": "Healthcare",
            "banking": "Banking",
            "pharmaceuticals": "Pharmaceuticals",
            "retail": "Retail",
            "travel": "Travel",
        }
