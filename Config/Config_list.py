# Setting configurations for autogen
import os

import autogen

# Absolute path to the JSON file
json_file_path = os.path.join(os.path.dirname(__file__), 'OAI_CONFIG_LIST.json')
config_list = autogen.config_list_from_json(
    env_or_file=json_file_path,
    filter_dict={
        "model": {
            "gpt-4-0125-preview",
            "gpt-4-1106-preview",
            "gpt-3.5-turbo-1106",
        }
    }
)

config_list_local = autogen.config_list_from_json(
    env_or_file=json_file_path,
    filter_dict={
        "model": {
            "local-model",
        }
    }
)

llm_config = {"temperature": 0.7, "timeout": 600, "cache_seed": 42, "config_list": config_list}

