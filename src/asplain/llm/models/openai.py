"""Wrapper for the OpenAI ChatGPT model"""

import os
from typing import Optional

import dotenv
from openai import AsyncOpenAI, OpenAI

from ..templates import Template
from .base import AbstractModel
from .tags import ModelTag


class OpenAIModel(AbstractModel):
    """Wrapper class for the OpenAI model"""

    model_tag_key = "openai"

    def __init__(self, model_tag: ModelTag, api_key: Optional[str] = None):
        super().__init__(model_tag)
        dotenv.load_dotenv()
        openai_api_key = api_key if api_key is not None else os.environ.get("OPENAI_API_KEY")
        self._client = AsyncOpenAI(api_key=openai_api_key)
        self._client_sync = OpenAI(api_key=openai_api_key)

    async def prompt(self, instructions_string: str, input_string: str) -> str:
        response = await self._client.responses.create(
            model=self.model_tag,
            instructions=instructions_string,
            input=input_string,
        )
        return OpenAIModel.transform_output(response.output_text)

    def prompt_sync(self, instructions_string: str, input_string: str) -> str:
        """Prompts the OpenAI API in a synchronous manner"""

        response = self._client_sync.responses.create(
            model=self.model_tag,
            instructions=instructions_string,
            input=input_string,
        )
        return OpenAIModel.transform_output(response.output_text)

    async def prompt_template(self, template: Template) -> str:
        return await self.prompt(
            instructions_string=template.compose_instructions(),
            input_string=template.compose_input(),
        )

    def prompt_template_sync(self, template: Template) -> str:
        """Prompts the OpenAI API with a template in a synchronous manner"""

        return self.prompt_sync(
            instructions_string=template.compose_instructions(),
            input_string=template.compose_input(),
        )

    @staticmethod
    def transform_output(unfiltered_output: str) -> str:
        return unfiltered_output
