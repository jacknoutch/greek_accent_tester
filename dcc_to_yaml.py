# Convert the DCC data to YAML format

import pandas as pd
import string, sys, yaml

from utilities import get_paradigm_from_principal_parts

# Open the DCC core Greek vocabulary CSV file
path = "~/data/dcc/greek_core_vocabulary/greek-core-list.csv"
df = pd.read_csv(path, encoding="utf-8")

# The YAML structure is as follows:
# δεσπότης:
#   nom_sg: "δεσπότης"
#   gen_sg: "δεσπότου"
#   gender: "m"
#   paradigm: "1e"
#   gloss: "master"
#   exceptions:
#     - case: "vocative"
#       form: "δεσπότα"

# For now, only take the first declension nouns
df = df[df['Part of Speech'] == "noun: 1st declension"].copy()

# Clean up the headword by removing punctuation
df["Headword"] = df["Headword"].str.translate(str.maketrans('', '', string.punctuation))

# Extract the lemma, genitive singular, gender, and paradigm
df["Lemma"] = df["Headword"].str.split(" ").str[0]
df["gen_sg"] = df["Headword"].str.split(" ").str[1]
df["gender"] = df["Headword"].str.split(" ").str[-1]
df["paradigm"] = df["Headword"].apply(get_paradigm_from_principal_parts)

# Create a dictionary to hold the words
words = {}

for row in df.itertuples():
    lemma = row.Lemma

    words[lemma] = {
        "nom_sg": lemma,
        "gen_sg": row.gen_sg,
        "gender": row.gender,
        "paradigm": row.paradigm,
        "gloss": row.DEFINITION,
        "exceptions": [],
    }

# Handle exceptions
words["δεσπότης"]["exceptions"].append({
    "slot": "sg_voc",
    "word_form": "δέσποτα"
})

# Save to YAML file
with open("dcc_core_vocab.yaml", "w", encoding="utf-8") as f:
    yaml.safe_dump(words, f, allow_unicode=True, sort_keys=False)