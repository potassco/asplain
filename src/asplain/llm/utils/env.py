"""Helpers for loading LLM environment variables."""

import dotenv


def load_working_directory_dotenv() -> None:
    """Load a .env file by searching from the current working directory."""
    dotenv_path = dotenv.find_dotenv(usecwd=True)
    if dotenv_path:
        dotenv.load_dotenv(dotenv_path)
