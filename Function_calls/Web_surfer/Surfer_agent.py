import os
import tempfile
from datetime import datetime
import autogen
import requests
from autogen.agentchat.contrib.web_surfer import WebSurferAgent
import shutil
import fitz

from dotenv import load_dotenv
from openai import OpenAI

from SemanthaVoiceAssistant.Config.Config_list import config_list

load_dotenv()
perplexity_apikey = os.getenv("PERPLEXITY_API_KEY")


def fetch_and_read_pdf(url):
    """
    Fetch a PDF from a given URL, read its text content, and return the text as a single string.
    Uses a temporary file to avoid leaving behind downloaded files.
    """
    # Fetch the PDF content from the URL
    response = requests.get(url)
    if response.status_code == 200:
        # Create a temporary file to hold the PDF
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            tmp.write(response.content)
            tmp.seek(0)  # Go to the beginning of the file to ensure proper reading

            # Open the temporary PDF file and read its text content
            doc = fitz.open(tmp.name)
            text = ""
            for page in doc:
                text += page.get_text()
            print(text)
            # Return the combined text from all pages
            return text
    else:
        return "Failed to fetch the PDF from the URL."


def query_preplexity_with_message(user_message):
    # Get the API key from the environment variable

    # Define the messages structure, including the system and user messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "take the concept and provide all information and relatable weblinks and links to pdfs."
            ),
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    # Initialize the OpenAI client with the Perplexity AI base URL
    client = OpenAI(api_key=perplexity_apikey, base_url="https://api.perplexity.ai")

    # Send the chat completion request without streaming
    response = client.chat.completions.create(
        model="pplx-70b-online",
        messages=messages,
    )
    # Extract and return only the content from the response
    response_content = response.choices[0].message.content if response.choices else "No response generated."
    return response_content


def create_simple_text_browser_config(clear_downloads_folder=False):
    """
    Initializes the SimpleTextBrowser with custom configuration and optionally clears the downloads folder.

    Parameters:
        clear_downloads_folder (bool): Whether to clear the downloads folder before initializing the browser.
    """
    bing_api_key = os.getenv("BING_API_KEY")  # Assuming the Bing API key is stored in an environment variable

    # Construct the downloads folder path relative to the current script
    current_script_dir = os.path.dirname(os.path.realpath(__file__))
    downloads_folder = os.path.join(current_script_dir, "downloads")

    # Clear the downloads folder if requested
    if clear_downloads_folder:
        clear_folder(downloads_folder)

    browser_config = {
        "start_page": "about:blank",
        "viewport_size": 1024 * 8,
        "downloads_folder": downloads_folder,
        "bing_api_key": bing_api_key,
    }

    return browser_config


def clear_folder(folder_path):
    """
    Clears all files and folders within a specified folder path.
    Creates the folder if it does not exist.

    Parameters:
        folder_path (str): The path to the folder to clear.
    """
    # Check if the folder exists, create if it does not
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    else:
        # Folder exists, clear its contents
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')


def create_web_surfer_agent():
    """
    Creates and configures a WebSurferAgent and a UserProxyAgent.

    Returns:
        tuple: A tuple containing instances of WebSurferAgent and UserProxyAgent.
    """
    llm_config = {
        "temperature": 0.0,
        "timeout": 600,
        "config_list": config_list,
    }

    web_surfer_config = {
        "config_list": config_list,
    }
    browser = create_simple_text_browser_config(clear_downloads_folder=True)

    surfer_agent = WebSurferAgent(
        name="web_surfer",
        llm_config=web_surfer_config,
        summarizer_llm_config=llm_config,
        code_execution_config={},
        browser_config=browser,
    )
    web_proxy_agent = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=0,
        system_message="An intelligent human admin agent designed for guiding the web_surfer assistant that "
                       "browses the web to navigate the internet. It in a consise sentance 3 max tells the webscraper "
                       "what link it must visit next while correcly including all the information of the original "
                       "query of the user. Provides a more conteqtual question with the aditional information provided.",

        code_execution_config={
            "work_dir": "coding",
            "use_docker": False,
        },
        llm_config=llm_config
    )

    return surfer_agent, web_proxy_agent


def initiate_task(task_description, task_time, clear_chat_history=False):
    """
    Initiates a task with the WebSurferAgent at a specified time.

    Parameters:
        task_description (str): Description of the task.
        task_time (datetime): Time at which the task is scheduled.
        clear_chat_history (bool): Whether to clear history before initiating the task.
    """
    formatted_task_description = f"{task_description}. Current time: {task_time.strftime('%Y-%m-%d %H:%M:%S')}"
    user_proxy_agent.initiate_chat(web_surfer_agent, message=formatted_task_description,
                                   clear_history=clear_chat_history, silent=False)
    latest_message_content = web_surfer_agent.last_message().get("content", "").strip()
    return latest_message_content


def query_web(task_description_input, should_clear_history=False, copilot=None):
    """
    Queries the web with a specified task description.

    Parameters:
        task_description_input (str): The task to be performed.
        should_clear_history (bool, optional): Whether to clear chat history before the task. Defaults to False.
        copilot (bool, optional): Whether to use Perplexity API for enhancing the query. Defaults to None.
    """
    if should_clear_history:
        print("CLEARING HISTORY")

    if not task_description_input:
        print("Error: 'task_description_input' must be a non-empty string.")
        return

    if copilot:
        print("ENABLED PERPLEXITY")
        try:
            Preformatted_information = query_preplexity_with_message(task_description_input)
            task_description_input = f"""Question: \n{task_description_input} \n\nInformation we have so far: \n{Preformatted_information}\n"""
        except Exception:
            print("No Perplexity API found. Please check https://docs.perplexity.ai for more information.")

    bing_api_key = os.getenv('BING_API')
    if bing_api_key is None:
        print(
            "BING_API environment variable not set. Please check https://www.microsoft.com/en-us/bing/apis/bing-web-search-api for more information.")

    current_time = datetime.now()
    try:
        response = initiate_task(task_description_input, current_time, clear_chat_history=should_clear_history)
        response_result = "RESULT:" + response
        return response_result
    except Exception as e:
        print(f"An error occurred while querying the web: {e}")


web_surfer_agent, user_proxy_agent = create_web_surfer_agent()

if __name__ == "__main__":
    while True:
        user_task_input = input("Type your input: ")
        query_web(user_task_input, should_clear_history=True, copilot=True)
