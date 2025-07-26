from engine import *
from utilities import *

DATA_PATH = "./data/dcc_core_vocab.yaml"


if __name__ == "__main__":

    nouns = load_lexicon(DATA_PATH)

    while True:
        
        noun = load_random_noun(nouns)
        case = load_random_case()
        number = load_random_number()

        accented_form = noun.decline(number, case)
        unaccented_form = strip_length(accented_form)

        print(f"Type the accented form of the noun '{unaccented_form}' in {case.name} {number.name}:")
        user_input = input().strip()

        if user_input == accented_form:
            print("Correct!")
        else:
            print(f"Incorrect. The correct form is: {accented_form}")

    # Process the nouns as needed
    for noun in nouns:
        noun.print_declension()