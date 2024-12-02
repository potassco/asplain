from enum import Enum

import torch
from transformers import pipeline

from .base import AbstractModel

class HuggingFaceLanguageModel(Enum):
    LLAMA_3_2_1B = "meta-llama/Llama-3.2-1B"
    LLAMA_3_2_3B = "meta-llama/Llama-3.2-3B"

class HuggingFaceModel(AbstractModel):

    def __init__(self, model: HuggingFaceLanguageModel = HuggingFaceLanguageModel.LLAMA_3_2_1B):
        super().__init__()
        self._model_string: str = model.value
        self._pipeline = pipeline(
            "text-generation",
            model=self._model_string,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )

    def prompt(self, input_string: str) -> str:
        response = self._pipeline(input_string)
        return response