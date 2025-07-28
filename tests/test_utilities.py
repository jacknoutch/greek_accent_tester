from unittest import TestCase, main
from engine import *

class TestUtilities(TestCase):

    def test_get_paradigm_from_principal_parts(self):
        from utilities import get_paradigm_from_principal_parts

        # Test cases for different principal parts
        self.assertEqual(get_paradigm_from_principal_parts("φυγή φυγῆς ἡ"), "1a")
        self.assertEqual(get_paradigm_from_principal_parts("χώρα χώρας ἡ"), "1b")
        self.assertEqual(get_paradigm_from_principal_parts("μοῦσα μούσης ἡ"), "1c")
        self.assertEqual(get_paradigm_from_principal_parts("ἀλήθεια ἀληθείας, ἡ"), "1d")
        self.assertEqual(get_paradigm_from_principal_parts("δεσπότης δεσπότου ὁ"), "1e")
        self.assertEqual(get_paradigm_from_principal_parts("νεανίας νεανίου ὁ"), "1f")
        self.assertEqual(get_paradigm_from_principal_parts("μοῖρα, -ης, ἡ"), "1d")
        self.assertEqual(get_paradigm_from_principal_parts("ἄνθρωπος, ἀνθρώπου, ὁ"), "2a")
        self.assertEqual(get_paradigm_from_principal_parts("νοῦς (νόος) νοῦ (νόου), ὁ"), "2b")
        self.assertEqual(get_paradigm_from_principal_parts("παιδίον παιδίου τό"), "2c")
        self.assertEqual(get_paradigm_from_principal_parts("κανοῦν (κανέον), κανοῦ (κανέου), τό"), "2d")
        self.assertEqual(get_paradigm_from_principal_parts("Μενέλεως, εω, ὁ"), "2e")


    def test_process_overrides(self):
        from utilities import process_overrides

        overrides_data = [
            {"slot": "sg_voc", "word_form": "δέσποτα"},
            {"slot": "sg_dat", "word_form": "Διί"}
        ]
        processed = process_overrides(overrides_data)

        self.assertEqual(len(processed), 2)
        self.assertEqual(processed[0].slot, (Number.SG, Case.VOC))
        self.assertEqual(processed[0].word_form, "δέσποτα")
        self.assertEqual(processed[1].slot, (Number.SG, Case.DAT))
        self.assertEqual(processed[1].word_form, "Διί")