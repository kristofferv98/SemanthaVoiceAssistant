# Semantha Voice Assistant
Welcome to the Semantha Voice Assistant, a AI companion designed to provide personalized and context-aware 
interactions through the integration of autogen, semantic routing and, VoiceProcessingToolkit. This system is adept 
at understanding user intent and sentiment. Responses are tailored with semantic routing based RAG, websearch 
capabilities using autogen websurfer and perplexity, and changing functionability during usage. It also has support 
for Local LLm usage. It works seamlessly to create effortless communication with the assistant.

## Setup and Installation
Before installing the requirements, navigate to the SemanthaVoiceAssistant project directory:

Then, get started with Semantha Voice Assistant by following these steps:
1. Clone the project: `git clone https://github.com/kristofferv98/SemanthaVoiceAssistant.git`
2. Navigate to the project dir `cd SemanthaVoiceAssistant`
3. Install dependencies: `pip install -r requirements.txt`.
4. Set enviorment variables in `.env`
5. Start the assistant: `python main.py`.
6. Type for example "Explain the Samantha program to me. and tell me how to customize it for a demo and instruction of usage"
7. Type "change input", "toggle voice feedback" or similar to enable or disable voice feedback. 
8. Say "hey Computer" to trigger the voice based interaction when input is set to recording. (Visit https://github.com/kristofferv98/VoiceProcessingToolkit for details)

Recommended:
PICOVOICE_APIKEY is for voice interperation is available free at picovoices website
ELEVENLABS_API_KEY for natural language responses

(optional):
BING_API_KEY for webscraping using autogen websurfer (visit autogens notebook on github for further information)
PERPLEXITY_API_KEY for more advanced webscraping.

## Core Functionality
The Semantha Voice Assistant features a semantic routing core that accurately interprets the essence of user 
inquiries. This core functionality allows for efficient management of a wide range of requests, including toggling 
between input modes and feedback types, and switching between assistant profiles. An intelligent layer precedes the 
evaluation by large language models (LLMs), ensuring precise interpretation and routing of queries for optimal user 
interaction.

## Behind the Scenes
Semantha's initial processing layer is the backbone of the system, designed for seamless operation. It is here that 
user intent is interpreted and queries are routed. This layer adapts to various interaction modes and user 
preferences, allowing for adjustments through natural language commands and facilitating profile customization. 
Users can switch between different LLM endpoints, enhancing the quality of interactions.

## Customization Options
The system offers extensive customization options through editable configurations in the `Config/OAI_CONFIG_LIST.json` 
file. Users can specify their preferred GPT models and set up custom local LLM endpoints, tailoring the assistant 
to their specific needs and preferences.

## Advanced Features
For users seeking deeper insights, Semantha includes advanced features such as detailed automated agentic 
webscraping and the ability to read PDFs from web links. The `Router_logic/Research_router.py` module adds a layer 
of sophistication, enhancing the system's capability to provide nuanced replies and understand complex queries. 
The copilot feature, combined with perplexity analysis, enriches web searches, offering comprehensive responses.

## Environment Setup
To utilize voice responses or the advanced research copilot function, configure the necessary API keys in the `.env` 
file at the project's root. The following keys are mandatory:
- `OPENAI_API_KEY`: For embeddings and assistant functionalities.

## Conclusion
Semantha Voice Assistant exemplifies the seamless integration of semantic embeddings and voice processing 
technologies. It is designed to meet a wide range of user needs with precision, offering empathetic engagement, 
humor, or expert advice as needed. This system ensures a rich and personalized user experience through meaningful 
and context-aware responses.

## ACKNOWLEDGEMENTS:
Special thanks to James Briggs and his team for developing the semantic-routing library and showcasing its use case on the YouTube channel https://www.youtube.com/@jamesbriggs. 
Their contributions have been invaluable to the development of this project. The link to the library can be found here https://github.com/aurelio-labs/semantic-router.

For more information on voice processing and additional functionalities, visit my library at https://github.com/kristofferv98/VoiceProcessingToolkit.
