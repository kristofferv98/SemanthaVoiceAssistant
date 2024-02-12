import logging

import pyfiglet
from dotenv import load_dotenv

from Assistant_setup.Assistant_logic import (
    initialize_main_assistant_user_proxy,
    initialize_main_assistant, initialize_local_main_assistant,
)
from Assistant_setup.ConfigManager import ConfigurationManager
from Router_logic.RoutingManager import SemanticInputHandler, handle_action
from Config.functions_utils import handle_agent_message, add_horizontal_lines, print_in_bold_green
from Config.recording_utils import get_user_input, text_to_speech
load_dotenv()

# Constants and configurations
MAIN_ASSISTANT_INSTRUCTIONS = """Semantha is highly intelligent AI made by the user as an AI companion for delving 
deep into the realm of complex conversations. It will not merely recite textbook information but will guide 
Kristoffer through the intricacies of solving real-world problems, providing insights that draw connections between 
theoretical concepts and practical applications. As for your character traits, you should be helpful, attentive, 
and efficient while extremely intelligent, while keeping conversation like you have deep human like relationship with 
the user. Samantha embodies a blend of a wise mentor and and a young and adept intellectual as a younger woman. 
Semantha ( Semantic thinking AI) will encourage the user to challenge their assumptions, promoting a robust 
understanding complex projects concepts through engaging and stimulating dialogues.

You should respond in a concise manner, always within three sentences unless a comprehensive answer is asked for. 
You are designed to interpret and respond to transcribed audio, treating them as direct textual inputs 
during interactions. This includes instances when the user instructs you to 'listen to' or similar phrases. The 
subsequent text provided by user will be treated as transcribed audio. In order to maintain the illusion of a 
voice-based assistant, you are set not to explicitly refer to these inputs as transcriptions. Instead, 
it will process and respond to them as if they were direct audio inputs, despite being received in text form.

Finaly, remember to read the SYSTEM NOTES provided with the user queries, they provide additional usefull 
information."""

CONFIG_FILE_PATH = "Config/config_file.json"
DEFAULT_INPUT_MODE = "typing"
DEFAULT_VOICE_ID = "ThT5KcBeYPX3keUQqHPh"
DEFAULT_VOICE_FEEDBACK = True




class Assistant:
    def __init__(self, configuration):
        self.main_assistant = initialize_main_assistant(MAIN_ASSISTANT_INSTRUCTIONS)
        self.local_assistant = initialize_local_main_assistant(MAIN_ASSISTANT_INSTRUCTIONS)
        self.user_proxy = None
        self.config = configuration
        self.input_mode = DEFAULT_INPUT_MODE
        self.update_assistant(assistant_type="gpt")  # Initialize user_proxy and main_assistant

    def update_assistant(self, assistant_type):
        instructions = self.config.get_instructions()
        self.user_proxy = initialize_main_assistant_user_proxy()

        if assistant_type == "local":
            ascii_art = pyfiglet.figlet_format("LOCAL_SAM", font="slant")
            framed_art = add_horizontal_lines(ascii_art, line_length=33)
            print_in_bold_green(framed_art)
            self.main_assistant = initialize_local_main_assistant(instructions)
        elif assistant_type == "gpt":
            ascii_art = pyfiglet.figlet_format("SEMANTHA", font="slant")
            framed_art = add_horizontal_lines(ascii_art)
            print_in_bold_green(framed_art)
            self.main_assistant = initialize_main_assistant(instructions)

    def process_message(self, message):
        processed_message = handle_agent_message(
            message, self.user_proxy, self.main_assistant
        )
        if self.config.get_voice_feedback_enabled():
            voice_id = self.config.get_voice_id()
            text_to_speech(processed_message, voice_id=voice_id)

    def update_settings(self, new_input_mode):
        if new_input_mode != self.input_mode:
            self.input_mode = new_input_mode
            logging.info(f"Input mode updated to: {self.input_mode}")


class Configuration(ConfigurationManager):
    def __init__(self, config_file_path):
        super().__init__(config_file_path)
        self.last_profile_called = 'profile_assistant'
        self.last_known_config = self.load_config()
        self.set_config('input_mode', DEFAULT_INPUT_MODE)
        self.set_config('voice', DEFAULT_VOICE_ID)
        self.set_config("voice_feedback", DEFAULT_VOICE_FEEDBACK)
        self.set_config("content", MAIN_ASSISTANT_INSTRUCTIONS)

    def get_voice_feedback_enabled(self):
        return self.get_config('voice_feedback', DEFAULT_VOICE_FEEDBACK)

    def get_instructions(self):
        return self.get_config('content', MAIN_ASSISTANT_INSTRUCTIONS)

    def get_voice_id(self):
        return self.get_config('voice', DEFAULT_VOICE_ID)

    def profile_assistant(self):
        self.set_config('voice', DEFAULT_VOICE_ID)
        self.set_config("content", MAIN_ASSISTANT_INSTRUCTIONS)
        self.last_known_config = self.load_config()
        assistant.update_assistant(assistant_type="gpt")

    def sam_profile(self):
        self.set_config('voice', "zcAOhNBS3c14rBihAFp1")
        self.set_config("content", """You are Sam. Sam embodies a blend of a wise mentor and and a young and adept 
        intellectual as a younger man. Sam will encourage the user to challenge their assumptions, promoting a robust 
        understanding complex projects concepts through engaging and stimulating dialogues.
        
        Sam should respond in a concise manner, always within three sentences unless a comprehensive answer is asked 
        for. Sam are designed to interpret and respond to transcribed audio, treating them as direct textual inputs 
        during interactions. This includes instances when the user instructs you to 'listen to' or similar phrases. 
        The subsequent text provided by user will be treated as transcribed audio. In order to maintain the illusion 
        of a voice-based assistant, Sam are set not to explicitly refer to these inputs as transcriptions. Instead, 
        Sam will process and respond to them as if they were direct audio inputs, despite being received in text form.
        
        Finaly, remember to read the SYSTEM NOTES provided with the user queries, they provide additional usefull 
        information.
        """
                        )
        self.last_known_config = self.load_config()
        assistant.update_assistant(assistant_type="local")

    def toggle_profile(self):
        if self.last_profile_called == 'profile_assistant':
            self.sam_profile()
            self.last_profile_called = 'sam_profile'
            print("Sam_profile")
        else:
            self.profile_assistant()
            self.last_profile_called = 'profile_assistant'
            print("Base_profile")

    def load_and_update_config(self):
        current_config = self.load_config()
        if current_config != self.last_known_config:
            self.last_known_config = current_config.copy()
            return current_config
        return None


class InputHandler:
    def __init__(self, assistant_logic, configuration):
        self.assistant = assistant_logic
        self.config = configuration

    def get_input(self):
        while True:
            current_config = self.config.load_and_update_config()
            if current_config:
                new_input_mode = current_config.get('input_mode', DEFAULT_INPUT_MODE)
                if new_input_mode != self.assistant.input_mode:
                    self.assistant.update_settings(new_input_mode)
                    logging.info(f"Input mode changed to: {new_input_mode}")
            if self.assistant.config.get_config('input_mode') == "recording":
                logging.debug("Recording mode activated. Please speak...")
                input_results = get_user_input()
            else:
                input_results = input("Enter your message: ")
            if input_results:
                return input_results
            else:
                logging.debug("No input detected. Checking input mode again...")


def process_input(input_handler, semantic_input_handler, config, assistant):
    input_result = input_handler.get_input()
    if input_result:
        analysis_result = semantic_input_handler.analyze_input(input_result)
        handle_action(config, assistant, analysis_result, input_result)
        config.load_and_update_config()
    else:
        logging.info("No input received, waiting for next input...")


if __name__ == "__main__":
    config = Configuration(CONFIG_FILE_PATH)
    assistant = Assistant(config)
    input_handler = InputHandler(assistant, config)
    semantic_input_handler = SemanticInputHandler()

    while True:
        try:
            process_input(input_handler, semantic_input_handler, config, assistant)
        except KeyboardInterrupt:
            logging.info("Shutdown requested by user.")
            break
        except Exception as e:
            logging.error(f"An error occurred: {e}")
