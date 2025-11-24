"""
Test cases for main application functionality.
"""

from unittest import TestCase

from asplain import contrast


class TestMain(TestCase):
    """
    Test cases for main application functionality.
    """

    def test_contrast(self) -> None:
        """
        Test the contrast functionality.
        """
        reference_pg = "node(atom(a))."
        contrast(
            number_of_foils=1,
            reference_pg=reference_pg,
        )
