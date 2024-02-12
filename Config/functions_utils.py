import logging
import os
import re

from Config.log_config import get_logger

logger = get_logger(log_level='ERROR')


def print_in_bold_green(text):
    # ANSI escape codes for green and bold text
    green = '\033[92m'
    bold = '\033[1m'
    reset = '\033[0m'
    print(f"{bold}{green}{text}{reset}")


def add_horizontal_lines(text, line_length=52):
    # Determine the width of the terminal
    try:
        width, _ = os.get_terminal_size()
    except OSError:
        width = 80  # Default width in case of non-terminal execution environments
    # Create the horizontal line
    line = '-' * line_length
    # Add the horizontal lines above and below the text with extra padding
    return f"{line}\n{text}{line}"


def strip_terminator(answer):
    """
    Removes Markdown, URLs, and formatting syntax from the answer.
    :param answer: The answer string to clean.
    :return: The cleaned answer string.
    """
    patterns = [
        r'!\[.*?]\(.*?\)',  # Markdown URL syntax
        r'\[.*?]\(.*?\)',  # Inline links
        r'http\S+',  # Standalone URLs
        r'(\*\*|__|\*|_|~~)',  # Bold, italic, strikethrough syntax
        r'\s?#+',  # Headers
        r'>+',  # Blockquotes
        r'`+'  # `code` syntax
    ]
    for pattern in patterns:
        answer = re.sub(pattern, '', answer)
    return answer.strip()


def is_termination_msg(content) -> bool:
    """
    Checks if the message content contains a termination keyword.
    :param content: The content of the message.
    :return: True if it contains a termination keyword, False otherwise.
    """
    return content.get("content", "").strip().endswith(("TERMINATE", "TERMINATE."))


def handle_agent_message(message, user_proxy, assistant):
    """
    Processes the message from the agent and returns the assistant's response.
    :param message: The message sent by the agent.
    :param user_proxy: The user proxy object.
    :param assistant: The assistant object.
    :return: The assistant's response or an error message.
    """
    if not message or not assistant or not user_proxy:
        logger.debug("Invalid input received in handle_agent_message")
        return None

    try:
        user_proxy.initiate_chat(recipient=assistant, message=message, clear_history=False)
        latest_message = assistant.last_message().get("content", "").strip()
        answer = strip_terminator(latest_message)
        logger.debug(answer)
        return answer
    except Exception as e:
        logger.debug(f"An error occurred in handle_agent_message: {e}")
        return None


def handle_error(exception):
    logging.error(f"Error in main loop: {exception}", exc_info=True)
