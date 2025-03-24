"""Wrapper for the OpenAI (Azure Hosted) ChatGPT model"""

import os

from openai import AzureOpenAI

from ..templates import Template
from .base import AbstractModel
from .tags import ModelTag


class OpenAIAzureModel(AbstractModel):
    """Wrapper class for the OpenAI model"""

    model_tag_key = "openai"

    def __init__(self, model_tag: ModelTag):
        super().__init__(model_tag)
        self._client = AzureOpenAI(
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-02-01",
        )

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
        response_message = response.choices[0].message.content
        return OpenAIAzureModel.filter_output(response_message)

    def prompt_template(self, template: Template) -> str:
        return self.prompt(template.compose())

    @staticmethod
    def filter_output(unfiltered_output: str) -> str:
        return unfiltered_output
