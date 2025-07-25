from unittest import TestCase, main
from utilities import get_paradigm_from_principal_parts

class TestUtilities(TestCase):

    def test_get_paradigm_from_principal_parts(self):

        # Test cases for different principal parts
        self.assertEqual(get_paradigm_from_principal_parts("φυγή φυγῆς ἡ"), "1a")
        self.assertEqual(get_paradigm_from_principal_parts("χώρα χώρας ἡ"), "1b")
        self.assertEqual(get_paradigm_from_principal_parts("μοῦσα μούσης ἡ"), "1c")
        self.assertEqual(get_paradigm_from_principal_parts("ἀλήθεια ἀληθείας, ἡ"), "1d")
        self.assertEqual(get_paradigm_from_principal_parts("δεσπότης δεσπότου ὁ"), "1e")
        self.assertEqual(get_paradigm_from_principal_parts("νεανίας νεανίου ὁ"), "1f")
        self.assertEqual(get_paradigm_from_principal_parts("μοῖρα, -ης, ἡ"), "1d")