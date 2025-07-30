from engine import *
from utilities import *

DATA_PATH = "./data/dcc_core_vocab.yaml"
EXERCISE_PATH = "./exercises/exercises.yaml"


if __name__ == "__main__":

    nouns = load_lexicon(DATA_PATH)

    # while True:
        
    #     noun = load_random_noun(nouns)
    #     case = load_random_case()
    #     number = load_random_number()

    #     accented_form = noun.decline(number, case)
    #     unaccented_form = strip_length(accented_form)

    #     print(f"Type the accented form of the noun '{noun.lemma}' in {case.name} {number.name}:")
    #     user_input = clean_input()

    #     if user_input == accented_form:
    #         print("Correct!")
    #     else:
    #         print(f"Incorrect. The correct form is: {accented_form}")

    # # Process the nouns as needed
    # for noun in nouns:
    #     noun.print_declension()

    exercises = load_exercises(EXERCISE_PATH)

    exercise = input("Which exercise would you like to do? (Enter the exercise #): ")

    while not exercise.isdigit() or int(exercise) < 1 or int(exercise) > len(exercises):
        exercise = input(f"Please enter a valid exercise number (1-{len(exercises)}): ")

    exercise = exercises[int(exercise) - 1]

    print(f"Exercise: {exercise.title}")

    for i, question in enumerate(exercise.questions):
        print(f"\n{i + 1}: {question.prompt}")
        print(f"Vocabulary:")
        for word in question.vocabulary:
            # find the word in the lexicon
            noun = next((n for n in nouns if n.lemma == word), None)
            if noun:
                print(f"- {noun.lemma}, {get_long_vowel_form(noun)}")

        user_answer = clean_input("\nYour answer: ")
        if user_answer == question.answer:
            print("Correct!")
        else:
            print(f"Incorrect. The correct answer: {question.answer}")
        
        print()
