import logging
import os

from semantic_router import Route, RouteLayer
from semantic_router.encoders import OpenAIEncoder

from SemanthaVoiceAssistant.Config.log_config import get_logger
from SemanthaVoiceAssistant.Router_logic.Research_router import Research_route_manager, create_full_prompt
from SemanthaVoiceAssistant.Router_logic.Sentiment_router import create_sentiment_prompt, Sentiment_router

os.environ["OPENAI_MODEL_NAME"] = "text-embedding-3-large"

logger = get_logger(log_level='ERROR')

Prompt_manager = Research_route_manager()
Sentiment_manager = Sentiment_router()


class SemanticInputHandler:
    def __init__(self):
        self.route_layer = None
        self.routes = None
        # IMPORTANT: Do not hardcode API keys here. Use environment variables or secure storage instead.
        self.encoder = OpenAIEncoder(dimensions=256, score_threshold=0.51)  # Ensure your API key is set appropriately
        self.setup_routes()

    def setup_routes(self):
        # Define routes that trigger input mode changes
        change_input = Route(
            name="change_input",
            utterances=[
                "Change input method",
                "Change input",
                "Change the input method",
                "Can we change input"
            ],
        )

        toggle_profile = Route(
            name="toggle_profile",
            utterances=[
                "Change the system settings to toggle a profile",
                "Can we change the profile?",
                "Let's try another profile",
            ],
        )

        toggle_voice_feedback = Route(
            name="toggle_voice_feedback",
            utterances=[
                "Toggle voice feedback",
                "toggle of voice",
                "turn of speech",
                "toggle on voice",
                "turn on speach",
                "change the feedback method"
                "Change feedback"
            ],
        )

        request_router = Route(
            name="request_information",
            utterances=[
                "ok go ahead and in detail, explain the consept"
                "In detail, I need detailed information about <topic>.",
                "In detail, Can you provide an in-depth analysis of <company> and its CEO?",
                "In detail, Tell me more about the history and development of <technology>.",
                "In detail, I'm looking for a comprehensive overview of <company>'s market strategy.",
                "In detail, Explore the major milestones and future prospects of <technology>.",
                "In detail, Dissect the key elements and current research in <field>.",
                "In detail, I need a thorough breakdown of the market for <product>, including all critical aspects.",
                "In detail, Examine the evolution, current status, and contributions of <company> in <industry>.",
                "In detail, Provide a detailed historical context and analysis of <topic>.",
                "In detail, Unpack the complexities and main debates surrounding <current issue>.",
                "In detail, Conduct an extensive examination of <topic>, highlighting notable developments.",
                "In detail, I'm interested in a deep dive into the history and implications of <topic>.",
                "In detail, Compile a comprehensive report on the advancements in <field>, including major "
                "contributors and"
                "developments.",
                "In detail: Delve into an in-depth exploration of <technology>, considering its impact and future "
                "prospects.",
                "In detail, Analyze the current trends and future outlook of <industry>.",
                "In detail, Investigate the role and influence of <topic> in <context>.",
                "In detail, Detail the journey and breakthroughs in <field> over the last decade.",
                "In detail, Study the effects of <global issue> on <industry or topic>.",
                "In detail, Dissect recent advancements and the future potential of <technology>.",
                "In detail, Elaborate on the principles of <concept> and their application in <field>.",
                "In detail, Can you research more in-depth on the series you mentioned?",
                "In detail, Dig into the history of <topic>.",
                "In detail, I need insights on <current event or trend>.",
                "In detail, Explore the concept of <topic> further.",
                "In detail, Delve into the roots and development of <topic>.",
                "In detail, Shed light on <historical event or figure>.",
                "In detail, Uncover details about <recent discovery or innovation>.",
                "In detail, Analyze the data from <recent event or trend>.",
                "In detail, Break down the plot and themes of <book or movie>.",
                "In detail, Explain the theory behind <scientific concept>.",
                "In detail, Detail the workings and implications of <technology or system>.",
                "In detail, Survey the latest developments in <field or industry>.",
                "In detail, Profile the life and impact of <historical or influential figure>.",
                "In detail, Review the implications of <recent development or change> in <field or society>.",
                "In detail, Summarize the key points of <complex topic or event>.",
                "In detail, Clarify the steps and findings of <recent study or experiment>.",
                "In detail, Describe the features and impact of <new technology or update>.",
                "In detail, Illustrate the concept and significance of <philosophical theory or idea>.",
                "In detail, Trace the origins and evolution of <cultural practice or movement>.",
                "In detail, Explain the benefits and considerations of <lifestyle choice or diet>."
            ]
        )

        # Add more routes if needed
        self.routes = [change_input, request_router, toggle_voice_feedback, toggle_profile]
        self.route_layer = RouteLayer(encoder=self.encoder, routes=self.routes)

    def analyze_input(self, input_result):
        """
        Analyze the input to determine the appropriate action.

        Args:
            input_result (str): The user's input text.

        Returns:
            dict: A dictionary containing the action type and any relevant data.
        """
        route_result = self.route_layer(input_result).name
        if route_result == "change_input":
            print("change_input")
            return {"action": "toggle_input_mode"}
        elif route_result == "Research":
            print("toggle_input_mode")
            return {"action": "start_research"}
        elif route_result == "toggle_voice_feedback":
            print("toggle_voice_feedback")
            return {"action": "toggle_voice_feedback"}
        elif route_result == "request_information":
            print("request_information")
            return {"action": "request_information"}
        elif route_result == "toggle_profile":
            print("toggle_profile")
            return {"action": "toggle_profile"}
        else:
            return {"action": "none"}


def handle_action(config, assistant, analysis_result, input_result):
    match analysis_result["action"]:
        case "toggle_input_mode":
            config.toggle_input_mode()
        case "toggle_voice_feedback":
            config.toggle_voice_feedback()
        case "toggle_profile":
            config.toggle_profile()
        case "request_information":
            prompt = create_full_prompt(input_result, Prompt_manager)
            assistant.process_message(prompt)
            pass
        case "none":
            # Process the message and convert the response to speech
            prompt = create_sentiment_prompt(input_result, Sentiment_manager)
            print(prompt)
            assistant.process_message(prompt)
        case _:
            logging.warning(f"Unhandled action type: {analysis_result['action']}")
