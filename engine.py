# Create a set of exercises for Ancient Greek accents, using the DCC core vocabulary

### Imports

# Standard library imports
from pprint import pprint as pp
import enum

# Third party imports
from greek_normalisation.normalise import Normaliser

# Local imports
from greek_accentuation.characters import strip_length, strip_accents, add_diacritic, Length
from greek_accentuation.syllabify import syllabify, nucleus
from greek_accentuation.accentuation import Accentuation, get_accentuation, persistent
from greek_accentuation.rules import Rule

normalise = Normaliser().normalise

class Gender(enum.Enum):
    MASC = "m"
    FEM = "f"
    NEU = "n"
    COM = "c"  # Common


class Case(enum.Enum):
    NOM = "nom"
    ACC = "acc"
    GEN = "gen"
    DAT = "dat"
    VOC = "voc"
    ALL = [NOM, ACC, GEN, DAT, VOC]


class Number(enum.Enum):
    SG = "sg"
    PL = "pl"
    DUAL = "dual"
    ALL = [SG, PL, DUAL]


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
        "1f": { # e.g. νεᾱνίᾱς
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
        "2a": { # e.g. λόγος 
            Number.SG: {
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
        "2b": { # e.g. νοῦς
            Number.SG: {
                Case.NOM: "ους",
                Case.ACC: "ουν",
                Case.GEN: "ου",
                Case.DAT: "ῳ",
                Case.VOC: "ου",
                },
            Number.PL: {
                Case.NOM: "οι",
                Case.ACC: "ους",
                Case.GEN: "ων",
                Case.DAT: "οις",
                },
        },
        "2c": { # e.g. δῶρον
            Number.SG: {
                Case.NOM: "ον",
                Case.ACC: "ον",
                Case.GEN: "ου",
                Case.DAT: "ῳ",
                },
            Number.PL: {
                Case.NOM: "α",
                Case.ACC: "α",
                Case.GEN: "ων",
                Case.DAT: "οις",
                },
        },
        "2d": { # e.g. ὀστοῦν
            Number.SG: {
                Case.NOM: "ουν",
                Case.ACC: "ουν",
                Case.GEN: "ου",
                Case.DAT: "ῳ",
                },
            Number.PL: {
                Case.NOM: "α",
                Case.ACC: "α",
                Case.GEN: "ων",
                Case.DAT: "οις",
                },
        },
        "2e": { # e.g. νεώς
            Number.SG: {
                Case.NOM: "ως",
                Case.ACC: "ων",
                Case.GEN: "ω",
                Case.DAT: "ῳ",
                },
            Number.PL: {
                Case.NOM: "ῳ",
                Case.ACC: "ως",
                Case.GEN: "ων",
                Case.DAT: "ῳς",
                },
        }
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


class DefiniteArtcle(Word):
    """
    Represents the definite article in Ancient Greek.
    """

    def __init__(self):
        super().__init__("ὁ")
        self.paradigm = {
            Gender.MASC: {
                Number.SG: {
                    Case.NOM: "ὁ",
                    Case.ACC: "τόν",
                    Case.GEN: "τοῦ",
                    Case.DAT: "τῷ",
                },
                Number.PL: {
                    Case.NOM: "οἱ",
                    Case.ACC: "τούς",
                    Case.GEN: "τῶν",
                    Case.DAT: "τοῖς",
                }
            },
            Gender.FEM: {
                Number.SG: {
                    Case.NOM: "ἡ",
                    Case.ACC: "τήν",
                    Case.GEN: "τῆς",
                    Case.DAT: "τῇ",
                },
                Number.PL: {
                    Case.NOM: "αἱ",
                    Case.ACC: "τάς",
                    Case.GEN: "τῶν",
                    Case.DAT: "ταῖς",
                }
            },
            Gender.NEU: {
                Number.SG: {
                    Case.NOM: "τό",
                    Case.ACC: "τό",
                    Case.GEN: "τοῦ",
                    Case.DAT: "τῷ",
                },
                Number.PL: {
                    Case.NOM: "τά",
                    Case.ACC: "τά",
                    Case.GEN: "τῶν",
                    Case.DAT: "τοῖς",
                }
            },
        }


class Noun(Word):
    """
    Each Noun must have one gender.
    Words with the same form but different genders (e.g. ὁ θεός/ἡ θεός) are separate instances.
    """

    def __init__(self, lemma, gender: Gender, declension, long_vowels=None, stem=None, overrides=None):
        super().__init__(lemma)
        self.gender = gender
        self.declension = declension
        self.paradigm = get_paradigm(declension)
        self.long_vowels = long_vowels
        self.stem = stem
        self.case = None
        self.number = None

        if overrides:
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
        Returns the stem of the noun, which is unaccented, marked with macrons where appropriate, and without any 
        endings.
        """
        if self.paradigm is None:
            raise ValueError("Paradigm not set for this noun.")
        
        nom_sg_ending = self.paradigm.get(Number.SG, {}).get(Case.NOM, None)
        if nom_sg_ending is None:
            raise ValueError("Nominal singular ending not found in paradigm.")
        
        unaccented_lemma = strip_accents(self.lemma)

        # If the lemma has a long vowel, we need to replace it with a macron.
        if self.long_vowels:
            syllables = syllabify(unaccented_lemma)
            for i, syllable in enumerate(syllables):
                if i + 1 in self.long_vowels:
                    syllables[i] = add_diacritic(syllable, Length.LONG)
            unaccented_lemma = ''.join(syllables)

        return unaccented_lemma[:-len(nom_sg_ending)]
    

    def decline(self, number=None, case=None):
        """
        Returns the declined word form for a given number and case, or None if no such word form exists in the paradigm.

        If number or case is not provided, it will give all word forms in the paradigm.
        """

        if self.paradigm is None:
            raise ValueError("Paradigm not set for this noun.")

        if self.stem is None:
            raise ValueError("Stem not set for this noun.")


        if number is None or case is None:
            # Return all forms in the paradigm
            return {n: {c: self.decline(n, c) for c in self.paradigm[n]} for n in self.paradigm.keys()}


        ending = self.paradigm.get(number, None).get(case, None)

        # Forms may be overridden where an Override exists in the place of a standard ending.
        if type(ending) is Override:
            return ending.word_form

        try:
            declined_form = self.stem + ending

        # If the word's paradigm does not have the requested number or case, return None.
        except TypeError:

            # But if the case requested is Vocative, use the nominative instead.
            if case == Case.VOC:
                return self.decline(number=number, case=Case.NOM)
            
            print(f"NB: Declension for {self.lemma} does not have {number} {case}.")
            return None
        
        exception_rules = self.get_exception_rules(number, case)

        accented_form = strip_length(persistent(declined_form, self.lemma, exception_rule=exception_rules))

        return accented_form


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


    def get_exception_rules(self, number, case):
        """
        Returns the exception rules for the given number and case.
        """

        accentuation = get_accentuation(self.lemma)

        if self.declension[0] == "1":
            if accentuation == Accentuation.OXYTONE and case in {Case.GEN, Case.DAT}:
                return Rule("First declension oxytone nouns in genitive and dative are perispomenon", Accentuation.PERISPOMENON)
            elif number == Number.PL and case == Case.GEN:
                return Rule("First declension nouns in genitive plural are perispomenon", Accentuation.PERISPOMENON)
        if self.declension == "1a" \
            and accentuation == Accentuation.PERISPOMENON \
            and case == Case.NOM \
            and number == Number.PL:
            # Perispomenon first declension nouns keep their accent throughout the whole paradigm
            return Rule("First declension perispomenon nouns in nominative plural are always perispomenon", Accentuation.PERISPOMENON)
        if self.declension in ["2a", "2b", "2c", "2d"]:
            if accentuation == Accentuation.OXYTONE and case in {Case.GEN, Case.DAT}:
                return Rule("Second declension oxytone nouns in genitive and dative are perispomenon", Accentuation.PERISPOMENON)
        if self.declension == "2b":
            accentuation = get_accentuation(self.lemma)
            if accentuation == Accentuation.PERISPOMENON:
                # This overrides the typical rule that the -οι ending in the nominative plural is short
                return Rule("Second declension perispomenon contract nouns remain perispomenon", Accentuation.PERISPOMENON)
        if self.declension == "2e":
            accentuation = get_accentuation(self.lemma)
            if accentuation == Accentuation.PROPAROXYTONE:
                return Rule("Attic second declension nouns do not obey the law of limitation", accentuation)
        