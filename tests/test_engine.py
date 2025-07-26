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
            "sg": {
                "nom": "νίκη",
                "acc": "νίκην",
                "gen": "νίκης",
                "dat": "νίκῃ",
            },
            "pl": {
                "nom": "νῖκαι",
                "acc": "νίκας",
                "gen": "νίκων",
                "dat": "νίκαις",
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
