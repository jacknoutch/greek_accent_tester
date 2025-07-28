from unittest import TestCase
from engine import *

class TestEngine(TestCase):

    def test_noun_decline(self):
        # Test the decline method of a Noun class

        nike = Noun("νίκη", Gender.FEM, "1a", stem="νῑκ")
        self.assertEqual(nike.decline(number=Number.PL, case=Case.NOM), "νῖκαι")


    def test_noun_decline_full_paradigm(self):
        # Test declining a noun with no such number or case > should result in a full paradigm
        nike = Noun("νίκη", Gender.FEM, "1a", stem="νῑκ")
        self.assertDictEqual(nike.decline(), {
            Number.SG: {
                Case.NOM: "νίκη",
                Case.ACC: "νίκην",
                Case.GEN: "νίκης",
                Case.DAT: "νίκῃ",
            },
            Number.PL: {
                Case.NOM: "νῖκαι",
                Case.ACC: "νίκας",
                Case.GEN: "νικῶν",
                Case.DAT: "νίκαις",
            }
        })

        time = Noun("τιμή", Gender.FEM, "1a",)
        self.assertDictEqual(time.decline(), {
            Number.SG: {
                Case.NOM: "τιμή",
                Case.ACC: "τιμήν",
                Case.GEN: "τιμῆς",
                Case.DAT: "τιμῇ",
            },
            Number.PL: {
                Case.NOM: "τιμαί",
                Case.ACC: "τιμάς",
                Case.GEN: "τιμῶν",
                Case.DAT: "τιμαῖς",
            }
        })


    def test_noun_decline_second_declension(self):

        # Test declining a second declension noun
        theos = Noun("θεός", Gender.MASC, "2a",)
        self.assertEqual(theos.decline(number=Number.SG, case=Case.NOM), "θεός")
        self.assertEqual(theos.decline(number=Number.SG, case=Case.ACC), "θεόν")
        self.assertEqual(theos.decline(number=Number.SG, case=Case.GEN), "θεοῦ")
        self.assertEqual(theos.decline(number=Number.SG, case=Case.DAT), "θεῷ")
        self.assertEqual(theos.decline(number=Number.PL, case=Case.NOM), "θεοί")
        self.assertEqual(theos.decline(number=Number.PL, case=Case.ACC), "θεούς")
        self.assertEqual(theos.decline(number=Number.PL, case=Case.GEN), "θεῶν")
        self.assertEqual(theos.decline(number=Number.PL, case=Case.DAT), "θεοῖς")

        # Test declining a second declension paroxytone noun
        # NB this also tests the rule for short -οι in the nominative plural
        polos = Noun("πῶλος", Gender.MASC, "2a",)
        self.assertEqual(polos.decline(number=Number.SG, case=Case.NOM), "πῶλος")
        self.assertEqual(polos.decline(number=Number.SG, case=Case.VOC), "πῶλε")
        self.assertEqual(polos.decline(number=Number.SG, case=Case.ACC), "πῶλον")
        self.assertEqual(polos.decline(number=Number.SG, case=Case.GEN), "πώλου")
        self.assertEqual(polos.decline(number=Number.SG, case=Case.DAT), "πώλῳ")
        self.assertEqual(polos.decline(number=Number.PL, case=Case.NOM), "πῶλοι")
        self.assertEqual(polos.decline(number=Number.PL, case=Case.ACC), "πώλους")
        self.assertEqual(polos.decline(number=Number.PL, case=Case.GEN), "πώλων")
        self.assertEqual(polos.decline(number=Number.PL, case=Case.DAT), "πώλοις")


    def test_attic_vocative_adelphos(self):
        # Test the irregulare vocative singular form for ἀδελφός in Attic Greek
        override = Override("ἄδελφε", (Number.SG, Case.VOC))
        adelphos = Noun("ἀδελφός", Gender.MASC, "2a", overrides=[override])
        self.assertEqual(adelphos.decline(number=Number.SG, case=Case.VOC), "ἄδελφε")


    def test_2b_contract_nouns(self):
        # Test declining a second declension contract noun
        nous = Noun("νοῦς", Gender.MASC, "2b", stem="ν")
        self.assertEqual(nous.decline(number=Number.SG, case=Case.NOM), "νοῦς")
        self.assertEqual(nous.decline(number=Number.SG, case=Case.VOC), "νοῦ")
        self.assertEqual(nous.decline(number=Number.SG, case=Case.ACC), "νοῦν")
        self.assertEqual(nous.decline(number=Number.SG, case=Case.GEN), "νοῦ")
        self.assertEqual(nous.decline(number=Number.SG, case=Case.DAT), "νῷ")
        self.assertEqual(nous.decline(number=Number.PL, case=Case.NOM), "νοῖ")
        self.assertEqual(nous.decline(number=Number.PL, case=Case.ACC), "νοῦς")
        self.assertEqual(nous.decline(number=Number.PL, case=Case.GEN), "νῶν")
        self.assertEqual(nous.decline(number=Number.PL, case=Case.DAT), "νοῖς")


    def test_2c_neuter_nouns(self):
        # Test declining a second declension neuter noun
        doron = Noun("δῶρον", Gender.NEU, "2c")
        self.assertEqual(doron.decline(number=Number.SG, case=Case.NOM), "δῶρον")
        self.assertEqual(doron.decline(number=Number.SG, case=Case.ACC), "δῶρον")
        self.assertEqual(doron.decline(number=Number.SG, case=Case.GEN), "δώρου")
        self.assertEqual(doron.decline(number=Number.SG, case=Case.DAT), "δώρῳ")
        self.assertEqual(doron.decline(number=Number.PL, case=Case.NOM), "δῶρα")
        self.assertEqual(doron.decline(number=Number.PL, case=Case.ACC), "δῶρα")
        self.assertEqual(doron.decline(number=Number.PL, case=Case.GEN), "δώρων")
        self.assertEqual(doron.decline(number=Number.PL, case=Case.DAT), "δώροις")


    def test_2d_neuter_contract_nouns(self):
        # Test declining a second declension neuter contract noun
        ostoon = Noun("ὀστοῦν", Gender.NEU, "2d", stem="ὀστ")
        self.assertEqual(ostoon.decline(number=Number.SG, case=Case.NOM), "ὀστοῦν")
        self.assertEqual(ostoon.decline(number=Number.SG, case=Case.ACC), "ὀστοῦν")
        self.assertEqual(ostoon.decline(number=Number.SG, case=Case.GEN), "ὀστοῦ")
        self.assertEqual(ostoon.decline(number=Number.SG, case=Case.DAT), "ὀστῷ")
        self.assertEqual(ostoon.decline(number=Number.PL, case=Case.NOM), "ὀστᾶ")
        self.assertEqual(ostoon.decline(number=Number.PL, case=Case.ACC), "ὀστᾶ")
        self.assertEqual(ostoon.decline(number=Number.PL, case=Case.GEN), "ὀστῶν")
        self.assertEqual(ostoon.decline(number=Number.PL, case=Case.DAT), "ὀστοῖς")


    def test_2e_attic_nouns(self):
        # Test declining a second declension Attic noun
        neos = Noun("νεώς", Gender.MASC, "2e")
        self.assertEqual(neos.decline(number=Number.SG, case=Case.NOM), "νεώς")
        self.assertEqual(neos.decline(number=Number.SG, case=Case.VOC), "νεώς")
        self.assertEqual(neos.decline(number=Number.SG, case=Case.ACC), "νεών")
        self.assertEqual(neos.decline(number=Number.SG, case=Case.GEN), "νεώ")
        self.assertEqual(neos.decline(number=Number.SG, case=Case.DAT), "νεῴ")
        self.assertEqual(neos.decline(number=Number.PL, case=Case.NOM), "νεῴ")
        self.assertEqual(neos.decline(number=Number.PL, case=Case.ACC), "νεώς")
        self.assertEqual(neos.decline(number=Number.PL, case=Case.GEN), "νεών")
        self.assertEqual(neos.decline(number=Number.PL, case=Case.DAT), "νεῴς")


    def test_noun_decline_explicit_vocative(self):
        # Test declining a noun with an explicit vocative form
        nike = Noun("νεανίας", Gender.FEM, "1f", stem="νεᾱνι")
        self.assertEqual(nike.decline(number=Number.SG, case=Case.VOC), "νεανία")


    def test_noun_decline_implied_vocative(self):
        # Test declining a noun with an implied vocative
        # Some nouns do not have an explicit vocative form, but the nominative is used instead.
        nike = Noun("νίκη", Gender.FEM, "1a", stem="νῑκ")
        self.assertEqual(nike.decline(number=Number.SG, case=Case.VOC), "νίκη")
        self.assertEqual(nike.decline(number=Number.PL, case=Case.VOC), "νῖκαι")
