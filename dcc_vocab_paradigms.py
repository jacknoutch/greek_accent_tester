# Standard library imports
import pandas as pd
import sys

# Local imports
sys.path.append("/home/jacknoutch/projects/greek_accentuation/greek_accentuation")
from greek_accentuation.accentuation import *
from engine import *
from utilities import get_paradigm_from_principal_parts

# Load the DCC core Greek vocabulary
dcc_core_vocab_path = "~/data/dcc/greek_core_vocabulary/greek-core-list.csv"
dcc_core_vocab = pd.read_csv(dcc_core_vocab_path, encoding="utf-8")

# Filter for 1st declension nouns
first_declension_nouns = dcc_core_vocab[dcc_core_vocab['Part of Speech'] == "noun: 1st declension"]


# Each noun must specify a lemma, gender, declension, and any exceptions

# The lemma
first_declension_nouns['Lemma'] = first_declension_nouns['Headword'].str.split(" ").str[0]

# Gender, mapped from the article at the end of the headword
gender_map = {
    "ἡ": "f",
    "ὁ": "m",
    "τό": "n"
}
first_declension_nouns['Gender'] = first_declension_nouns['Headword'].str.split(" ").str[-1].map(gender_map)

# Declension
first_declension_nouns["Declension"] = first_declension_nouns["Headword"].apply(get_paradigm_from_principal_parts)


# Populate a list of nouns from the dataframe
nouns = []

for row in first_declension_nouns.itertuples():
    paradigm = get_paradigm(row.Declension)
    noun = Noun(
        lemma=row.Lemma,
        gender=Gender.FEM if row.Gender == "f" else Gender.MASC,
        paradigm=paradigm
    )
    nouns.append(noun)

# Print the paradigms
for noun in nouns:
    noun.print_declension()