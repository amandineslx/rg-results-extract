# Rhythmic Gymnastics results extraction
## Main script
### Purpose

Extract, enrich and display the results from a rhythmic gymnastics competition from the FFGym website.

In particular, during inter-departemental competitions, gymnasts from French departments 04-05-06-98-84 and the ones from 13-83 are judged by the same jury and both the rankings can be mixed in order to have an idea of the potential ranking for the regional competition (qualifications for the France championship).

### Execution

* add configuration file with expected format in `configs` folder
* run `python main.py {config_file_name}` (Python 3.9 OK)

## Coupe des clubs
### Purpose

Compute the results of the Coupe des clubs from a regional competition.

During the individual qualifications to France championship, gymnasts are directly qualified through the granted quotas. Then, among the remaining not qualified gymnasts, a team can be declared for each club. This team will be composed of the best not qualified gymnast in national category and the 3 best not qualified gymnast in federal category of the same club. The teams are ranked and a quota is granted per region to qualify these teams for a separated competition during the France championship.

### Execution

* add configuration file with expected format in `configs/coupe_des_clubs` folder
* run `python coupe_des_clubs.py {config_file_name}` (Python 3.9 OK)

## Data source

JSON returned by the FFGym website when requesting the PDF display of the results.
URL: https://resultats.ffgym.fr/api/palmares/evenement/{id}
