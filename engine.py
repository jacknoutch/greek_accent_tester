# Create a set of exercises for Ancient Greek accents, using the DCC core vocabulary

### Imports

# Standard library imports
from pprint import pprint as pp
import sys

# Third party imports
from greek_normalisation.normalise import Normaliser

# Local imports
sys.path.append("/home/jacknoutch/projects/greek_accentuation/greek_accentuation")
from greek_accentuation.characters import *
from greek_accentuation.accentuation import *

normalise = Normaliser().normalise

class Gender:
    MASC = "m"
    FEM = "f"
    NEU = "n"


class Case:
    NOM = "nom"
    ACC = "acc"
    GEN = "gen"
    DAT = "dat"
    VOC = "voc"
    ALL = [NOM, ACC, GEN, DAT, VOC]

case_map = {
    "nom": Case.NOM,
    "acc": Case.ACC,
    "gen": Case.GEN,
    "dat": Case.DAT,
    "voc": Case.VOC
}

class Number:
    SG = "sg"
    PL = "pl"
    ALL = [SG, PL]

number_map = {
    "sg": Number.SG,
    "pl": Number.PL
}

def get_paradigm(paradigm_id):
    """
    Returns the standard paradigm for the given declension ID.
    """
    paradigms = {
        "1a": { # e.g. νίκη
            Number.SG: {
                Case.NOM: "η",
                Case.ACC: "ην",
                Case.GEN: "ης",
                Case.DAT: "ῃ",
                },
            Number.PL: {
                Case.NOM: "αι",
                Case.ACC: "ᾱς",
                Case.GEN: "ων",
                Case.DAT: "αις",
                }
        },
        "1b": { # e.g. χώρα
            Number.SG: {
                Case.NOM: "ᾱ",
                Case.ACC: "ᾱν",
                Case.GEN: "ᾱς",
                Case.DAT: "ᾳ",
                },
            Number.PL: {
                Case.NOM: "αι",
                Case.ACC: "ᾱς",
                Case.GEN: "ων",
                Case.DAT: "αις",
                }
        },
        "1c": { # e.g. μοῦσα
            Number.SG: {
                Case.NOM: "ᾰ",
                Case.ACC: "ᾰν",
                Case.GEN: "ης",
                Case.DAT: "ῃ",
                },
            Number.PL: {
                Case.NOM: "αι",
                Case.ACC: "ᾱς",
                Case.GEN: "ων",
                Case.DAT: "αις",
                },
        },
        "1d": { # e.g. διάνοια
            Number.SG: {
                Case.NOM: "ᾰ",
                Case.ACC: "ᾰν",
                Case.GEN: "ᾱς",
                Case.DAT: "ᾳ",
                },
            Number.PL: {
                Case.NOM: "αι",
                Case.ACC: "ᾱς",
                Case.GEN: "ων",
                Case.DAT: "αις",
                },
        },
        "1e": { # e.g. δεσπότης
            Number.SG: {
                Case.NOM: "ης",
                Case.VOC: "η",
                Case.ACC: "ην",
                Case.GEN: "ου",
                Case.DAT: "ῃ",
                },
            Number.PL: {
                Case.NOM: "αι",
                Case.ACC: "ᾱς",
                Case.GEN: "ων",
                Case.DAT: "αις",
                },
        },
        "1f": {  # e.g. νεᾱνίᾱς
            Number.SG: {
                Case.NOM: "ᾱς",
                Case.VOC: "ᾱ",
                Case.ACC: "ᾱν",
                Case.GEN: "ου",
                Case.DAT: "ᾳ",
                },
            Number.PL: {
                Case.NOM: "αι",
                Case.ACC: "ᾱς",
                Case.GEN: "ων",
                Case.DAT: "αις",
                },
        },
        "2a": {
            Number.SG: { # e.g. λόγος
                Case.NOM: "ος",
                Case.ACC: "ον",
                Case.GEN: "ου",
                Case.DAT: "ῳ",
                Case.VOC: "ε",
                },
            Number.PL: {
                Case.NOM: "οι",
                Case.ACC: "ους",
                Case.GEN: "ων",
                Case.DAT: "οις",
                },
        },
    }
    if paradigm_id in paradigms:
        return paradigms[paradigm_id]
    else:
        raise ValueError(f"Unknown declension ID: {paradigm_id}")

class Override:
    """
    A class to override the default ending for a specific case and number.
    This is used for cases where the standard paradigm does not apply, such as unique vocative.
    """
    
    def __init__(self, word_form, slot):
        self.word_form = word_form
        self.slot = slot  # e.g. (Number.SG, Case.VOC)

    def __repr__(self):
        return f"Override({self.word_form})"


class Word:
    def __init__(self, lemma):
        self.lemma = lemma
        pass


class Noun(Word):
    """
    Each Noun must have one gender.
    Words with the same form but different genders (e.g. ὁ θεός/ἡ θεός) are separate instances.
    """

    def __init__(self, lemma, gender: Gender, paradigm, stem=None, overrides=None):
        super().__init__(lemma)
        self.stem = stem
        self.gender = gender
        self.paradigm = paradigm
        self.case = None
        self.number = None

        for override in overrides:
            if isinstance(override, Override):
                number, case = override.slot
                self.paradigm[number][case] = override

        if self.stem is None:
            self.stem = self.get_stem()


    def __repr__(self):
        return f"Noun({self.lemma})"
    

    def get_stem(self):
        """
        Returns the stem of the noun, which is the form without any endings.
        """
        if self.paradigm is None:
            raise ValueError("Paradigm not set for this noun.")
        
        nom_sg_ending = self.paradigm.get(Number.SG, {}).get(Case.NOM, None)
        if nom_sg_ending is None:
            raise ValueError("Nominal singular ending not found in paradigm.")
        
        unaccented_lemma = strip_accents(self.lemma)
        print(unaccented_lemma)
        
        return unaccented_lemma[:-len(nom_sg_ending)]
    

    def decline(self, number=None, case=None, normalised=False):
        """
        Returns the declined form of the noun based on the number and case.

        If number or case is not provided, it will decline the whole paradigm for the given case.
        """
        if self.paradigm is None:
            raise ValueError("Padadigm not set for this noun.")

        if self.stem is None:
            raise ValueError("Stem not set for this noun.")

        if number is None or case is None:

            return {n: {c: self.decline(n, c, normalised) for c in self.paradigm[n]} for n in self.paradigm.keys()}

        self.number = number
        self.case = case

        ending = self.paradigm.get(number, None).get(case, None)

        if type(ending) is Override:
            return ending.word_form

        try:
            declined_form = self.stem + ending
        except TypeError as e:
            print(f"NB: Declension for {self.paradigm['name']} does not have {number} {case}.")
            return None

        declined_form = self.stem + ending

        return normalise(declined_form)[0] if normalised else declined_form


    def print_declension(self):
        """
        Prints the declension of the noun in the format typical for the UK.
        """
        pp(f"Declension for {self.lemma}:")
        declension = self.decline()

        numbers = sorted(
            declension.keys(), 
            key=lambda x: (x == Number.PL, x == Number.SG)
            )
        
        for number in numbers:
            pp(f"{number}:")
            cases = sorted(
                declension[number].keys(),
                key=lambda x: (
                    x == Case.DAT,
                    x == Case.GEN,
                    x == Case.ACC,
                    x == Case.VOC,
                    x == Case.NOM)
                )
            
            for case in cases:
                ending = declension[number][case]
                if ending is not None:
                    pp(f"  {case}: {ending}")
                else:
                    pp(f"  {case}: No ending found")