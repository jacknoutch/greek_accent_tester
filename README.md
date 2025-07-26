# Ancient Greek Accent Tester

## What is it?

A CLI application to test your knowledge of Ancient Greek accentuation.

## How complete is it?

The app will correctly test you on the accentuation for a small set of nouns from the first declension.

There is much more to come!

## Getting started

You will need to be able to type in [Polytonic Greek](https://patristica.net/graeca/how-to-type-in-greek/) to make use of this application.

- Clone this repo to your computer
- Install a virtual environment
- Install the requirements.txt file
- Run the command `python main.py` in the top level directory
- Answer the questions until you wish to stop!

## Acknowledgments

This module builds makes substantial use of James Tauber's (et al.) [`greek-accentuation`](https://github.com/jtauber/greek-accentuation) module. The pypi version of this is out of date (it says it is 1.2.0 but it lacks the most recent and very useful tools of 1.2.0 as per Github). This, together with my desire to use Github Actions sensible, requires that I incorporate the material into this repo. The module's README is found in that folder, as is LICENSE and AUTHORS, with the caveat that I have tweaked with one or two things.

I'm also using [DCC's Greek Core Vocabulary](https://dcc.dickinson.edu/greek-core-list) as a stock of simple vocabulary which can be used for the testing. This will need to grow at some point, especially since its stock of words will not illustrate the whole array of rules and intricacies of the accent system.

A mention should also be made to the [Greek Learner Texts Project](https://greek-learner-texts.org/) which is partly the inspiration for undertaking this expedition.

Two practical guides I would recommend to those who have a knowledge of Ancient Greek but whose journey thus far did not pass by the crags of accentuation:
- A. J. Koster, *A Practical Guide for the Writing of the Greek Accents*, Leiden Brill 1976
- P. Probert, *A New Short Guide to the Accentuation of Ancient Greek*, BCP 2003