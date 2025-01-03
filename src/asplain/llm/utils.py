import random
import time

from ..utils.logging import colored


def print_typewriter(message: str, speed: float = 1.0) -> None:
    for i in message:
        print(i, end="", flush=True)
        if i == " ":
            sleep_time = random.random() / 30
        elif i in "\n":
            sleep_time = random.random() / 5
        else:
            sleep_time = random.random() / 50
        time.sleep(sleep_time / speed)


def print_llm_message(message: str, author: str = "LLM", speed: float = 1.0) -> None:
    print(colored("BLUE", f"\n{author}:"))
    print_typewriter(colored("GREY", message) + "\n", speed)
    print()
