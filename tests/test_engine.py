from unittest import TestCase
from engine import *

class TestEngine(TestCase):

    def test_noun_decline(self):
        # Test the decline method of a Noun class

        paradigm = get_paradigm("1a")
        nike = Noun("νίκη", Gender.FEM, paradigm, stem="νῑκ")
        self.assertEqual(nike.decline(number=Number.PL, case=Case.NOM), "νῖκαι")


    def test_noun_decline_full_paradigm(self):
        # Test declining a noun with no such number or case > should result in a full paradigm
        paradigm = get_paradigm("1a")
        nike = Noun("νίκη", Gender.FEM, paradigm, stem="νῑκ")
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

        time = Noun("τιμή", Gender.FEM, paradigm)
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



    def test_noun_decline_explicit_vocative(self):
        # Test declining a noun with an explicit vocative form
        paradigm = get_paradigm("1f")
        nike = Noun("νεανίας", Gender.FEM, paradigm, stem="νεᾱνι")
        self.assertEqual(nike.decline(number=Number.SG, case=Case.VOC), "νεανία")


    def test_noun_decline_implied_vocative(self):
        # Test declining a noun with an implied vocative
        # Some nouns do not have an explicit vocative form, but the nominative is used instead.
        paradigm = get_paradigm("1a")
        nike = Noun("νίκη", Gender.FEM, paradigm, stem="νῑκ")
        self.assertEqual(nike.decline(number=Number.SG, case=Case.VOC), "νίκη")
        self.assertEqual(nike.decline(number=Number.PL, case=Case.VOC), "νῖκαι")
