import autogen
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent

from SemanthaVoiceAssistant.Config.Config_list import config_list, config_list_local
from SemanthaVoiceAssistant.Config.log_config import get_logger
from SemanthaVoiceAssistant.Function_calls.Function_schema.function_schema import query_web_schema, fetch_and_read_pdf_schema
from SemanthaVoiceAssistant.Function_calls.Web_surfer.Surfer_agent import query_web, fetch_and_read_pdf

logger = get_logger(log_level='ERROR')


def initialize_main_assistant(main_assistant_instructions, agent_name="Assistant"):
    main_assistant_llm_config = {
        "config_list": config_list,
        "tools": [
            {"type": "code_interpreter"},
            {
                "type": "function",
                "function": query_web_schema,
            },
            {
                "type": "function",
                "function": fetch_and_read_pdf_schema,
            },
        ],
    }

    main_assistant = GPTAssistantAgent(
        name=agent_name,
        overwrite_instructions=True,
        overwrite_tools=True,
        instructions=main_assistant_instructions,
        llm_config=main_assistant_llm_config,
    )
    main_assistant.register_function(
        function_map=
        {"query_web": query_web,
         "fetch_and_read_pdf": fetch_and_read_pdf},
    )

    return main_assistant
def initialize_local_main_assistant(main_assistant_instructions, agent_name="Assistant"):
    local_assistant_llm_config = {
        "config_list": config_list_local,
        "tools": [
            {"type": "code_interpreter"},
        ],
    }
    local_main_assistant = autogen.ConversableAgent(
        name=agent_name,
        system_message=main_assistant_instructions,
        llm_config=local_assistant_llm_config,
    )
    return local_main_assistant

def initialize_main_assistant_user_proxy():
    # is_termination_msg = lambda x: "content" in x and x["content"] and x["content"].rstrip().endswith(("TERMINATE",
    # "TERMINATE."))
    main_assistant_user_proxy = autogen.UserProxyAgent(
        "User",
        max_consecutive_auto_reply=0,
        human_input_mode="NEVER",
        # is_termination_msg=is_termination_msg,
        code_execution_config={"work_dir": "coding", "use_docker": None},
        llm_config={"config_list": config_list},
    )
    return main_assistant_user_proxy
