# Standard library imports
import pandas as pd

# Local imports
from engine import *

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

# Declension, mapped from the lemma in a rough and ready manner; macrons/breves are required to split 1b and 1d
first_declension_nouns["Declension"] = first_declension_nouns["Lemma"].apply(strip_accents).apply(
    lambda x: "1a" if x.endswith("η") else
              "1b" if x.endswith("ρα") or x.endswith("ια") or x.endswith("εα") else
              "1c" if x.endswith("α") else
              "1d" if x.endswith("ᾰ") else
              "1e" if x.endswith("ης") else
              "1f" if x.endswith("ᾱς") else
              None
)

# The only correct required is ἀλήθεια which is 1d
first_declension_nouns.loc[first_declension_nouns["Headword"] == "ἀλήθεια ἀληθείας, ἡ", "Declension"] = "1d"


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