import sys, yaml

from engine import *
from utilities import process_overrides

DATA_PATH = "./data/dcc_core_vocab.yaml"


if __name__ == "__main__":
    # Load the DCC core Greek vocabulary from YAML
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        dcc_core_vocab = yaml.safe_load(f)

    # Create a list of Noun objects from the DCC core vocabulary
    nouns = []
    for lemma, data in dcc_core_vocab.items():
        paradigm = get_paradigm(data['paradigm'])
        overrides = process_overrides(data.get('exceptions', []))
        noun = Noun(
            lemma=lemma,
            gender=data['gender'],
            paradigm=paradigm,
            overrides=overrides,
        )
        nouns.append(noun)

    # Process the nouns as needed
    for noun in nouns:
        noun.print_declension()