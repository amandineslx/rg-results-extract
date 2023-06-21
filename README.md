# Rhythmic Gymnastics results extraction

## Purpose

Extract, enrich and display the results from a rhythmic gymnastics competition from the FFGym website.

In particular, during inter-departemental competitions, gymnasts from French departments 04-05-06-98-84 and the ones from 13-83 are judged by the same jury and both the rankings can be mixed in order to have an idea of the potential ranking for the regional competition (qualifications for the France championship).

## Execution

* add configuration file with expected format in `configs` folder
* add it in the mapping table in `main.py`
* change the target of the `main.py` (last line)
* run `python main.py` (Python 3.9 OK)

## Data source

JSON returned by the FFGym website when requesting the PDF display of the results.
URL: https://resultats.ffgym.fr/api/palmares/evenement/{id}
