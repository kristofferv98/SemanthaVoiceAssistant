query_web_schema = {
  "name": "query_web",
  "description": "Automates web browsing based on natural language guidance, enabling the execution of web queries through a conversational interface. The function leverages a WebSurferAgent to interpret and act upon user tasks, querying the web and returning results. It supports an optional copilot mode for expanded search capabilities and optionally clears chat history before each task.",
  "parameters": {
    "type": "object",
    "properties": {
      "task_description_input": {
        "type": "string",
        "description": "The natural language description of the task to be performed by the WebSurferAgent. This could range from searching for information, automating interactions on web pages, to collecting data from specific sites."
      },
      "should_clear_history": {
        "type": "boolean",
        "description": "Determines whether the chat history should be cleared before initiating a new task. This is useful for ensuring that each query is treated as a separate session without interference from previous interactions.",
        "default": "false"
      },
      "copilot": {
        "type": "boolean",
        "description": "Enables copilot assistance to expand the search with additional details. When enabled, the search query is augmented with preformatted information derived from the initial task description, enhancing the scope and relevance of the web query.",
        "default": "false"
      }
    },
    "required": [
      "task_description_input"
    ]
  }
}

fetch_and_read_pdf_schema = {
  "name": "fetch_and_read_pdf",
  "description": "Fetch a PDF from a given URL, read its text content, and return the text as a single string. Uses a temporary file to avoid leaving behind downloaded files.",
  "parameters": {
    "type": "object",
    "properties": {
      "url": {
        "type": "string",
        "description": "The URL from where the PDF will be fetched."
      }
    },
    "required": [
      "url"
    ]
  }
}
