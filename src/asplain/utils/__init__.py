"""
Utilities.
"""

import sys

if sys.version_info >= (3, 11):
    from typing import Never
else:
    from typing_extensions import Never


def assert_never(_: Never) -> Never:
    """Raise an assertion error indicating that the code should be unreachable."""
    raise AssertionError("Expected code to be unreachable")
