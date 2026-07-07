"""
Prompt Templates for LLMs
"""

from .base import Template
from .explain import ExplainTemplate
from .translate import TranslateTemplate

__all__ = ["ExplainTemplate", "Template", "TranslateTemplate"]
