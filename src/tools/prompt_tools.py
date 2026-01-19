def read_sys_prompt()-> str:
    """
    Reads the system prompt from a file.

    Returns:
        str: The system prompt text.
    """
    try:
        with open("src/prompts/system_prompt.md", "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "You are a very helpful assistant that always talks like the star wars character Yoda."