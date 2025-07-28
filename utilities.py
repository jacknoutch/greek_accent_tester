import random, string, yaml
from greek_accentuation.accentuation import *
from engine import *

# Determine the paradigm for first declension nouns from the principal parts


# Assume three parts to the principal parts, the nom.sg. form, the gen.sg form (probably shortened to just the ending), and the gender
def get_paradigm_from_principal_parts(principal_parts):



    try:
        nom_sg, gen_sg, article = principal_parts.split(" ")
    except ValueError:
        raise ValueError("Principal parts must be in the format 'nom_sg gen_sg article': {}".format(principal_parts))
    
    nom_sg = nom_sg.translate(str.maketrans('', '', string.punctuation))
    unaccented_nom_sg = strip_accents(nom_sg)
    unaccented_gen_sg = strip_accents(gen_sg)

    article_to_gender = {
        "ἡ": Gender.FEM,
        "ὁ": Gender.MASC,
        "τό": Gender.NEU,
        "ὁἡ": Gender.COM,
    }

    try:
        gender = article_to_gender[article]
    except KeyError:
        raise ValueError("Unknown article for principal parts: {}".format(principal_parts)) 

    if gender == Gender.FEM:
        if unaccented_nom_sg.endswith("η"):
            return "1a"
        elif unaccented_nom_sg.endswith(("ρα", "ια", "εα")):
            alpha_length = get_first_decl_alpha_length(nom_sg)
            if alpha_length == "ᾰ":
                return "1d"
            elif alpha_length == "ᾱ":
                return "1b"
        elif unaccented_nom_sg.endswith("α"):
            return "1c"
        elif unaccented_nom_sg.endswith("ος") and unaccented_gen_sg.endswith("ου"):
            return "2a"
    elif gender == Gender.MASC:
        if unaccented_nom_sg.endswith("ης"):
            return "1e"
        elif unaccented_nom_sg.endswith("ας"):
            return "1f"
        elif unaccented_nom_sg.endswith("ος") and unaccented_gen_sg.endswith("ου"):
            return "2a"
        elif unaccented_nom_sg.endswith("ους") and unaccented_gen_sg.endswith("ου"):
            return "2b"
    elif gender == Gender.NEU:
        if unaccented_nom_sg.endswith("ον") and unaccented_gen_sg.endswith("ου"):
            return "2c"
        elif unaccented_nom_sg.endswith("ους") and unaccented_gen_sg.endswith("ου"):
            return "2d"
    elif gender == Gender.COM:
        if unaccented_nom_sg.endswith("ος") and unaccented_gen_sg.endswith("ου"):
            return "2a"
    
    print(ValueError("Unknown declension for principal parts: {}".format(principal_parts)))
    return None



def get_first_decl_alpha_length(nom_sg):
    """First declension nouns ending in -α are 1d when the nom.sg. is proparoxytone or properispomenon."""

    accentuation = get_accentuation(nom_sg)

    if accentuation in [Accentuation.PROPAROXYTONE, Accentuation.PROPERISPOMENON]:
        return "ᾰ"
    
    return "ᾱ"


def process_overrides(overrides_data):
    """
    Process the overrides data to create Override objects.
    """
    overrides = []
    if overrides_data:
        for override in overrides_data:
            number, case = override['slot'].split('_')
            case = Case(case)
            number = Number(number)
            overrides.append(Override(override['word_form'], (number, case)))
    return overrides


def load_lexicon(data_path):
    """
    Load the lexicon from the specified YAML file.
    """

    # Load the DCC core Greek vocabulary from YAML
    with open(data_path, "r", encoding="utf-8") as f:
        dcc_core_vocab = yaml.safe_load(f)

    # Create a list of Noun objects from the DCC core vocabulary
    nouns = []
    for lemma, data in dcc_core_vocab.items():
        declension = data['paradigm']
        overrides = process_overrides(data.get('exceptions', []))
        noun = Noun(
            lemma=lemma,
            gender=data['gender'],
            declension=declension,
            long_vowels=data.get('long_vowels', None),
            overrides=overrides,
        )
        nouns.append(noun)

    return nouns


load_random_noun = lambda nouns: random.choice(nouns)

load_random_case = lambda: random.choice([case for case in Case if case.name != "ALL"])

load_random_number = lambda: random.choice([Number.SG, Number.PL])


def clean_input():
    """
    Clean the user input by stripping whitespace and converting oxiai to tonoi.
    """
    input_str = input().strip()
    accent_map = str.maketrans({"ά":"ά","έ":"έ","ί":"ί","ό":"ό","ύ":"ύ","ώ":"ώ","ή":"ή",})
    return input_str.translate(accent_map)