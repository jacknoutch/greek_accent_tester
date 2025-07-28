import random, string, yaml
from greek_accentuation.accentuation import *
from engine import *

# Determine the paradigm for first declension nouns from the principal parts


# Assume three parts to the principal parts, the nom.sg. form, the gen.sg form (probably shortened to just the ending), and the gender
def get_paradigm_from_principal_parts(principal_parts):

    split_parts = principal_parts.split(" ")
    clean_principal_parts = []
    for i, part in enumerate(split_parts):
        # Remove any commas or full stops from the parts
        part = part.strip(".,")
        if part:
            clean_principal_parts.append(part)


    if len(clean_principal_parts) == 5:
        # Check to see if the second and fourth parts are in parentheses, which is a common format for alternate forms
        if clean_principal_parts[1].startswith("(") \
            and clean_principal_parts[3].startswith("("):
            # If so, we can assume the second part is the genitive singular and the fourth part is the article
            clean_principal_parts = [clean_principal_parts[0], clean_principal_parts[2], clean_principal_parts[4]]

    if len(clean_principal_parts) != 3:
        raise ValueError("Principal parts must consist of three parts: nom_sg, gen_sg, and article. Provided: {}".format(principal_parts))

    nom_sg, gen_sg, article = clean_principal_parts
    
    nom_sg = nom_sg.translate(str.maketrans('', '', string.punctuation))
    unaccented_nom_sg = strip_accents(nom_sg)
    gen_sg = gen_sg.translate(str.maketrans('', '', string.punctuation))
    unaccented_gen_sg = strip_accents(gen_sg)

    article_to_gender = {
        "ἡ": Gender.FEM,
        "ὁ": Gender.MASC,
        "τό": Gender.NEU,
        "ὁ/ἡ": Gender.COM,
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
        elif unaccented_nom_sg.endswith("ως") and unaccented_gen_sg.endswith("ω"):
            return "2e"
    elif gender == Gender.NEU:
        if unaccented_nom_sg.endswith("ον") and unaccented_gen_sg.endswith("ου"):
            return "2c"
        elif unaccented_nom_sg.endswith("ουν") and unaccented_gen_sg.endswith("ου"):
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


def clean_input(prompt=""):
    """
    Clean the user input by stripping whitespace and converting oxiai to tonoi.
    """
    input_str = input(prompt).strip()
    accent_map = str.maketrans({"ά":"ά","έ":"έ","ί":"ί","ό":"ό","ύ":"ύ","ώ":"ώ","ή":"ή",})
    return input_str.translate(accent_map)


class Exercise:
    """
    Represents an exercise with a title, description, and a list of questions.
    """
    def __init__(self, id, title, description, questions):
        self.id = id
        self.title = title
        self.description = description
        self.questions = questions


class Question:
    """
    Represents a question in an exercise with a prompt and an answer.
    """
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer


def load_exercises(yaml_file):
    """
    Load an exercise from a YAML file.
    """
    with open(yaml_file, "r", encoding="utf-8") as f:
        exercise_data = yaml.safe_load(f)["exercises"]

    
    # A sample exercise data structure might look like this:
    # 
    # exercises:
    # - id: definite_article
    #     title: Definite Article
    #     description: |
    #     This exercise focusses on the definite article, all genders, cases, and numbers.
    #     questions:
    #     - prompt: της
    #         answer: τῆς
    #     - prompt: τα
    #         answer: τά

    exercises = []
    for exercise in exercise_data:
        # Create Exercise object
        exercise = Exercise(
            id=exercise['id'],
            title=exercise['title'],
            description=exercise['description'],
            questions=[
                Question(prompt=q['prompt'], answer=q['answer'])
                for q in exercise['questions']
            ]
        )
        exercises.append(exercise)
    
    return exercises