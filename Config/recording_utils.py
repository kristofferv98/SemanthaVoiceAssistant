import os
import logging

from VoiceProcessingToolkit.VoiceProcessingManager import VoiceProcessingManager, text_to_speech_stream

# Configure logging as needed, e.g., logging level, format, handlers
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_user_input(play_notification_sound=True, use_wake_word=False, tts=False):
    """
    Captures user input via voice, transcribes it, and returns the transcription.

    Args:
    - play_notification_sound (bool): Whether to play a notification sound before capturing user input.
    - use_wake_word (bool): Whether to use a wake word to initiate user input capture.
    - streaming (bool): Whether to use streaming mode for voice capture.
    """
    vpm = VoiceProcessingManager.create_default_instance(
        use_wake_word=True or use_wake_word,
        play_notification_sound=True or play_notification_sound,
        wake_word="computer",
        min_recording_length=3,
        inactivity_limit=2.5,
        sensitivity=0.5,
        voice_threshold=0.9,
    )
    logging.info("Listening for user input...")
    print("Listening for user input...")

    transcription = None
    while transcription is None:
        transcription = vpm.run(tts=False or tts)
        if transcription is None:
            logging.debug("Recording was not made or was too short. Retrying...")
            print("Recording was not made or was too short. Retrying...")
            return None
    logging.debug(f"Processed text: {transcription}")
    return transcription


def text_to_speech(text, eleven_labs_api_key=None, voice_id=None):
    """
    Converts the given text to speech and streams it.

    Args:
    - text (str): The text to be converted to speech.
    - eleven_labs_api_key (str): The API key for the ElevenLabs service, if not using the environment variable.
    - voice_id (str): The ID of the voice to use for speech synthesis.
    """
    try:
        api_key = eleven_labs_api_key or os.getenv('ELEVENLABS_API_KEY')
        text_to_speech_stream(text=text, api_key=api_key, voice_id=voice_id)
        logging.info(f"Assistant said: {text}")
        return text
    except Exception as e:
        logging.error(f"Failed to convert text to speech: {e}")
        return None