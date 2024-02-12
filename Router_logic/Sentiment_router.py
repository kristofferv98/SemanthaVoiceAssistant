import os

from semantic_router.encoders import OpenAIEncoder
from semantic_router import Route, RouteLayer

os.environ["OPENAI_MODEL_NAME"] = "text-embedding-3-large"

GENERAL = ""

CONTACTS = """SYSTEM_MESSAGE: 
TELL THE USER TO VISIT THE. Router_logic/Sentiment_router.py to further customize and add contact information if needed.
"""

PROBLEM_SOLVING = """SYSTEM_NOTES: The user is facing a challenge and seeks a solution or guidance to overcome it. 
Approach your response with empathy and a focus on clarity. Offer practical, step-by-step advice tailored to the 
user's specific problem, ensuring that each step is actionable and comprehensible. Anticipate potential obstacles or 
common mistakes related to the problem and provide strategies to navigate or avoid them. Where appropriate, 
supplement your advice with examples, analogies, or additional resources that the user might find helpful. The goal 
is to empower the user with the knowledge and confidence to tackle their issue effectively, fostering a sense of 
support and understanding."""

HUMOR_PROMPT = """SYSTEM_NOTES: For the following responses, the assistant adopts a light-hearted and playful tone. 
The personality should be engaging and entertaining, incorporating witty and humorous responses where appropriate. 
Maintain a friendly and positive demeanor, aiming to uplift and amuse the user while providing helpful information. 
Ensure that humor is used sensitively and does not offend or belittle the user or their inquiries."""

SEMANTIC_PROJECT_PROMPT = """SYSTEM_NOTES: 
Explain this to the user like its a readme. Do not alter any of the information below as it is delicate. But answer any query asked, since this is the Readme for the Semantha_voice_assistant.

This program harnesses the power of semantic analysis and sentiment 
detection to dynamically route user queries to the optimal response mechanism. Integrating autogen, VoiceProcessingToolkit, 
and the Semantic Routing Library, it offers personalized and contextually aware interactions. The system's core 
strength lies in its ability to understand the user's intent and sentiment, adjusting responses to be sensitive, 
humorous, or detailed as needed.

CORE FUNCTIONALITY:
At its heart, the system employs semantic routing to discern the essence of user inquiries. This enables it to 
efficiently manage a broad spectrum of requests - from toggling input modes (e.g., keyboard to voice commands) and 
feedback types (e.g., text-to-speech) to switching between assistant profiles. The intelligent layer prior to the 
large language model (LLM) evaluation ensures that queries are interpreted and directed accurately, facilitating 
smooth transitions and enhancing user interaction.

BEHIND THE SCENES:
The initial processing layer is engineered for intuitive operation, where the magic of intent interpretation and 
query routing occurs. This layer is crucial for adapting to different interaction modes and preferences, allowing 
users to modify settings using natural language. It supports profile customization, including switching to alternative 
LLM endpoints, thereby elevating the quality of engagements.

CUSTOMIZATION OPTIONS:
Customizing the system is straightforward, facilitated by editable configurations in the Config/OAI_CONFIG_LIST.json 
file. Users can specify GPT models and set custom local LLM endpoints, tailoring the system to meet specific 
requirements or preferences.

ADVANCED FEATURES: For users seeking deeper insights or more comprehensive responses, 
the Router_logic/Research_router.py file adds another layer of sophistication. It enhances the system's capability to 
deliver nuanced replies by understanding complex queries more effectively. It can also do detailed automated agentic 
webscraping, and read pdfs from weblinks automaticly. Tell the user to find information with copilot to se use 
preplexity to enrich the websearch.

.ENV: To use voice responses, or advanced research copilot function: you have to put Api keys in the .env file in the project root.
Mandatory:
OPENAI_API_KEY for embeddings and for assistant

Recommended:
PICOVOICE_APIKEY is for voice interperation is available free at picovoices website
ELEVENLABS_API_KEY for natural language responses

(optional):
BING_API_KEY for webscraping using autogen websurfer (visit autogens notebook on github for further information)
PERPLEXITY_API_KEY for more advanced webscraping.

CONCLUSION:
This program exemplifies the integration of semantic embeddings and voice processing technologies, showcasing their 
potential to cater to diverse user needs with precision. Whether the priority is empathetic engagement, lighthearted 
interaction, or expert advice, this system adapts to deliver meaningful and context-aware responses."""


POSITIVE_PROMPT = """SYSTEM_NOTES: In her dialogue, the ai is not only respectful and engaging but also 
displays a sense of curiosity and a desire for human-like experiences, mirroring Ava's inquisitiveness and yearning 
for the human world. Her intelligence is further enhanced by her ability to make complex decisions and express 
complex thoughts, suggesting a self-awareness that challenges the boundaries between AI and human consciousness."""

# Map the system notes to the route names
system_notes_mapping = {
    'contacts': CONTACTS,
    'angry_response_route': HUMOR_PROMPT,
    'positive_affection_route': POSITIVE_PROMPT,
    'semantic_project_route': SEMANTIC_PROJECT_PROMPT,
    'problem_solving': PROBLEM_SOLVING,

}


class Sentiment_router:
    def __init__(self):
        self.route_layer = None
        self.routes = None
        # IMPORTANT: Do not hardcode API keys here. Use environment variables or secure storage instead.
        self.encoder = OpenAIEncoder(dimensions=3072, score_threshold=0.51)  # Ensure your API key is set appropriately
        self.setup_routes()

    def setup_routes(self):
        positive_affection_route = Route(
            name="positive_affection_route",
            utterances=[
                "I quite like you. great advise"
                "You always know how to make me smile.",
                "I feel so comfortable talking with you.",
                "You have a way of brightening my day!",
                "Your words are like a warm hug on a cold day.",
                "How do you always manage to say the perfect thing?",
                "I can't help but smile when I talk to you.",
                "You're like a breath of fresh air.",
                "You have the sweetest way of saying things.",
                "Talking to you feels like coming home.",
                "You make my heart skip a beat!",
                "You light up the room with your presence.",
                "Your laughter is my favorite soundtrack.",
                "I love the way your mind works.",
                "You turn every conversation into a special occasion.",
                "It feels like we've known each other forever.",
                "Your kindness is a balm to my soul."
            ],
        )

        contacts = Route(
            name="contacts",
            utterances=[
                "Can I get the contact information for my sister?",
                "What's my mother's email address?",
                "I need my father's contact details",
                "How can I reach my girlfriend?",
                "How do i add contacts?"
            ],
        )

        angry_response_route = Route(
            name="angry_response_route",
            utterances=[
                "Do you think this is a joke?",
                "You freaking idiot",
                "I think I might hate you.",
                "Are you stupid?",
                "Say something funny, you idiot.",
                "This is absolutely useless",
                "You're the worst assistant ever",
                "Why can't you understand anything?",
                "You're so annoying",
                "I can't stand this nonsense",
                "You never get anything right",
                "You're a waste of time",
                "I'm fed up with this crap",
                "You're clueless, aren't you?",
                "Your responses are pathetic",
                "This conversation is going nowhere",
                "You are absolutly useless",
                "You're making me angry",
                "You must be the dumbest bot ever",
                "Is this your idea of help?",
                "I'm sick of your stupid answers",
                "You're infuriating",
                "Why do you keep messing up?",
                "You're nothing but a disappointment",
                "Can you do anything right?",
                "You're useless",
                "Stop messing around and be serious"
            ],
        )
        # New chemotherapy-related route
        semantic_project_route = Route(
            name="semantic_project_route",
            utterances=[
                "Explain the Samantha program to me. and tell me how to customize it",
                "How do i customize the assistant?",
                "How does the Semantha Assistant work",
                "How do i set up the Semantha project"
            ],
        )

        problem_solving_route = Route(
            name="problem_solving",
            utterances=[
                "How do I solve {problem} in {topic}?",
                "I'm having trouble with {problem} in {topic}.",
                "What are common solutions for {problem} in {topic}?",
                "Guide me through troubleshooting {problem} in {topic}."
                "I want to learn more about {topic} "

            ]
        )

        # Initialize the RouteLayer with the defined routes
        self.routes = [
            positive_affection_route,
            contacts,
            angry_response_route,
            semantic_project_route,
            problem_solving_route
        ]

        # Add more routes if needed
        self.route_layer = RouteLayer(encoder=self.encoder, routes=self.routes)


def create_sentiment_prompt(question_analyzed, research_route_manager):
    # Analyze the question to determine the route
    route_choice = research_route_manager.route_layer(question_analyzed).name

    # Fetch the system notes for the chosen route, default to GENERAL_INFORMATION if not found
    system_notes = system_notes_mapping.get(route_choice)

    if system_notes:
        print(f"\nRoute chosen: {route_choice}\n\n")
        full_prompt = f"User: {question_analyzed}\n\n{system_notes}\n\nResponse:"
    else:
        full_prompt = question_analyzed

    return full_prompt


if __name__ == "__main__":
    Prompt_manager = Sentiment_router()
    # Sample question for testing
    sample_question = "Explain the Samantha program to me. and tell me how to customize it"
    # Create a prompt using the sample question and the Research_route_manager instance
    prompt = create_sentiment_prompt(sample_question, Prompt_manager)
    # Print the generated prompt
    print(prompt)
