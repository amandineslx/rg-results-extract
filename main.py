from extraction import get_results_events
from merging import get_vertical_ranking
from writing import write_results

EVENT_IDS = {
  "la_colle_2022": ["13441"],
  "sollies_2022": ["13579", "13580"],
  "vitrolles_2022": ["14130"],
  "mouans_2023": ["14425"],
  "aix_2023": ["14715", "14716"],
  "istres_2023": ["14342"],
  "simu_france_2023": [
    "14342", # PROVENCE-ALPES-COTE D AZUR - GR / REGION SUD / CHPT ENSEMBLE - DUO NAT TF REG
    "14510", # AUVERGNE-RHONE-ALPES - GR / CHPT AURA / ENSEMBLES-DUO / FEDB&C-REG
    "14862", # BRETAGNE - GR / RGPT / FED B ET C / ENSEMBLES ET DUOS
    "14359", # CENTRE-VAL DE LOIRE - GR / REG CVL / CHPT REG / REG / FED / NAT / ENS ET DUO
    "14477", # CORSE - GR - TF ENSEMBLES ET DUOS
    "14459", # GRAND EST - GR / CHPT REGIONAL GRAND EST / PERFORMANCE ET FED B/C / ENSEMBLES
    "14771", # GUADELOUPE - COMPETITION SELECTIVE GR ENSEMBLE REGIONAL ET FEDERAL B
    "14789", # HAUTS-DE-FRANCE - GR ENSEMBLES TFB ET TFC ENSEMBLES ET DUOS NATIONAUX
    "14661", # ILE-DE-FRANCE - GR / CHPT REGIONAL IDF / ENS NAT, FED B, FED C
    "14586", # ILE-DE-FRANCE - GR / CHPT REGIONAL IDF / ENS DUOS FED A REG ET NAT 10/11 ANS
    "14907", # MARTINIQUE - CHAMPIONNAT MARTINIQUE DES ENSEMBLES GR
    "13890", # NORMANDIE - GR/REGION/NORMANDIE/CHPT REGIONAL/ENSEMBLES
    "13775", # NOUVELLE-AQUITAINE - GR / NV AQUITAINE / CHPT REGIONAL / FED B - FED C
    "14905", # OCCITANIE - GR / OCCITANIE / REGIONAL FEDERAL NATIONAL / ENSEMBLES ET EQUIPES
  ]
}

def generate_results_file(event_ids):
    """
    Take the event IDs as input, build a structure containing the information about the different apparatuses for the different gymnasts in the different categories, merge the event results together and write the consolidated results in a CSV file.
    """
    results = get_results_events(event_ids)
    vertical_ranking = get_vertical_ranking(results)
    write_results(vertical_ranking)
    print("Finished!")

generate_results_file(EVENT_IDS['simu_france_2023'])
