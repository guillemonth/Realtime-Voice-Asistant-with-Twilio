def read_sys_prompt()-> str:
    """
    Reads the system prompt from a file.

    Returns:
        str: The system prompt text.
    """
    with open("src/prompts/system_prompt.md", "r", encoding="utf-8") as file:
        return file.read()