"""Wrapper for the Ollama model"""

from ollama import Client, ProgressResponsegit

from .base import AbstractModel
from .tags import ModelTag
from ..templates import Template


class OllamaModel(AbstractModel):
    """Wrapper class for the Ollama model"""

    model_tag_key = "ollama"

    def __init__(self, model_tag: ModelTag, filter_thoughts: bool = True):
        super().__init__(model_tag)
        self._client = Client(host="http://localhost:11434")
        self._filter_thoughts = filter_thoughts

    def prompt(self, input_string: str) -> str:
        self._touch_model()
        response = self._client.chat(
            model=self.model_tag,
            messages=[
                {"role": "user", "content": input_string},
            ],
        )
        return self.filter_output(response.message.content, supress_thoughts=self._filter_thoughts)

    def prompt_template(self, template: Template) -> str:
        return self.prompt(template.compose())

    def _touch_model(self) -> None:
        """Checks if the requested model is locally available and if not pulls it"""
        model_name_list = [m.model for m in self._client.list().models]
        if self.model_tag not in model_name_list:
            print(f"Start pulling model ({self.model_tag})")
            for progress in self._client.pull(self.model_tag, stream=True):
                if progress.completed is not None and progress.total is not None:
                    print(self._get_pull_progress_string(progress), end="\r")
            print()
            print("Finished pulling model")
        else:
            print(f"Cached ({self.model_tag})")

    @staticmethod
    def _get_pull_progress_string(progress: ProgressResponse) -> str:
        progress_percent = progress.completed / progress.total
        progress_completed_gb = round(progress.completed / (2**30), 2)
        progress_total_gb = round(progress.total / (2**30), 2)
        progress_bar_stops = 60
        progress_bar = "".join(
            [
                OllamaModel._get_pull_progress_bar_char(progress_percent, i, progress_bar_stops)
                for i in range(progress_bar_stops)
            ]
        )
        # progress_bar = ""
        return f" ▕{progress_bar}▏{int(progress_percent * 100)}% [{progress_completed_gb}GB/{progress_total_gb}GB]"

    @staticmethod
    def _get_pull_progress_bar_char(percent: float, position: int, total: int) -> str:
        chars = ["▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
        step_size = (100 / total) / 100
        char = " "
        step = position / total
        if percent > step:
            if percent <= step + step_size:
                char = chars[int(((percent - step) / step_size) * (len(chars) - 1))]
            else:
                char = chars[-1]
        return char

    @staticmethod
    def filter_output(unfiltered_output: str, supress_thoughts: bool = True) -> str:
        filtered = unfiltered_output
        if "Answer:" in filtered:
            filtered = filtered.replace("Answer:", "", 1).strip()
        filtered = filtered.removeprefix('"')
        filtered = filtered.removesuffix('"')
        # Only for deepseek r1 COT model to hide thought process
        if supress_thoughts:
            filtered = filtered.split("</think>")[1].strip()
        return filtered
