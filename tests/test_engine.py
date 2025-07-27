from unittest import TestCase
from engine import *

class TestEngine(TestCase):

    def test_noun_decline(self):
        # Test the decline method of a Noun class

        paradigm = get_paradigm("1a")
        nike = Noun("νίκη", Gender.FEM, 1, paradigm, stem="νῑκ")
        self.assertEqual(nike.decline(number=Number.PL, case=Case.NOM), "νῖκαι")


    def test_noun_decline_full_paradigm(self):
        # Test declining a noun with no such number or case > should result in a full paradigm
        paradigm = get_paradigm("1a")
        nike = Noun("νίκη", Gender.FEM, 1, paradigm, stem="νῑκ")
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

        time = Noun("τιμή", Gender.FEM, 1, paradigm)
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
        paradigm = get_paradigm("2a")
        theos = Noun("θεός", Gender.MASC, 2, paradigm)
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
        paradigm = get_paradigm("2a")
        polos = Noun("πῶλος", Gender.MASC, 2, paradigm)
        self.assertEqual(polos.decline(number=Number.SG, case=Case.NOM), "πῶλος")
        self.assertEqual(polos.decline(number=Number.SG, case=Case.ACC), "πῶλον")
        self.assertEqual(polos.decline(number=Number.SG, case=Case.GEN), "πώλου")
        self.assertEqual(polos.decline(number=Number.SG, case=Case.DAT), "πώλῳ")
        self.assertEqual(polos.decline(number=Number.PL, case=Case.NOM), "πῶλοι")
        self.assertEqual(polos.decline(number=Number.PL, case=Case.ACC), "πώλους")
        self.assertEqual(polos.decline(number=Number.PL, case=Case.GEN), "πώλων")
        self.assertEqual(polos.decline(number=Number.PL, case=Case.DAT), "πώλοις")


    def test_attic_vocative_adelphos(self):
        # Test the irregulare vocative singular form for ἀδελφός in Attic Greek
        paradigm = get_paradigm("2a")
        override = Override("ἄδελφε", (Number.SG, Case.VOC))
        adelphos = Noun("ἀδελφός", Gender.MASC, 1, paradigm, overrides=[override])
        self.assertEqual(adelphos.decline(number=Number.SG, case=Case.VOC), "ἄδελφε")


    def test_noun_decline_explicit_vocative(self):
        # Test declining a noun with an explicit vocative form
        paradigm = get_paradigm("1f")
        nike = Noun("νεανίας", Gender.FEM, 1, paradigm, stem="νεᾱνι")
        self.assertEqual(nike.decline(number=Number.SG, case=Case.VOC), "νεανία")


    def test_noun_decline_implied_vocative(self):
        # Test declining a noun with an implied vocative
        # Some nouns do not have an explicit vocative form, but the nominative is used instead.
        paradigm = get_paradigm("1a")
        nike = Noun("νίκη", Gender.FEM, 1, paradigm, stem="νῑκ")
        self.assertEqual(nike.decline(number=Number.SG, case=Case.VOC), "νίκη")
        self.assertEqual(nike.decline(number=Number.PL, case=Case.VOC), "νῖκαι")
