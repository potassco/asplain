"""Wrapper for the OpenAI ChatGPT model"""

import os

from openai import OpenAI

from ..templates import Template
from .base import AbstractModel
from .tags import ModelTag


class OpenAIModel(AbstractModel):
    """Wrapper class for the OpenAI model"""

    model_tag_key = "openai"

    def __init__(self, model_tag: ModelTag):
        super().__init__(model_tag)
        self._client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def prompt(self, input_string: str) -> str:
        response = self._client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": input_string,
                }
            ],
            model=self.model_tag,
        )
        return OpenAIModel.filter_output(response)

    def prompt_template(self, template: Template) -> str:
        return self.prompt(template.compose())

    @staticmethod
    def filter_output(unfiltered_output: str) -> str:
        return unfiltered_output
