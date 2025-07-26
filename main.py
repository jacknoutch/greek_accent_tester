from engine import *
from utilities import process_overrides, load_lexicon

DATA_PATH = "./data/dcc_core_vocab.yaml"


if __name__ == "__main__":

    nouns = load_lexicon(DATA_PATH)
    

    # Process the nouns as needed
    for noun in nouns:
        noun.print_declension()