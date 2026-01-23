"""Wrapper for the Google Gemini model"""

import os
import dotenv
from typing import Optional

from google import genai

from ..templates import Template
from .base import AbstractModel
from .tags import ModelTag


class GoogleModel(AbstractModel):
    """Wrapper class for the Google model"""

    model_tag_key = "google"

    def __init__(self, model_tag: ModelTag, api_key: Optional[str] = None):
        super().__init__(model_tag)
        dotenv.load_dotenv()
        gemini_api_key = api_key if api_key is not None else os.environ.get("GEMINI_API_KEY")
        self._client = genai.Client(api_key=gemini_api_key)

    async def prompt(self, instructions_string: str, input_string: str) -> str:
        contents = "\n".join([instructions_string, input_string])
        response = await self._client.aio.models.generate_content(
            model=self.model_tag,
            contents=contents,
        )
        return GoogleModel.transform_output(response.text)

    async def prompt_template(self, template: Template) -> str:
        return await self.prompt(
            instructions_string=template.compose_instructions(),
            input_string=template.compose_input(),
        )

    @staticmethod
    def transform_output(unfiltered_output: str) -> str:
        return unfiltered_output
