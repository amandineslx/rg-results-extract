from extraction import get_results_events
from merging import get_vertical_ranking
from writing import write_results

EVENT_IDS = {
  "la_colle_2022": ["13441"],
  "sollies_2022": ["13579", "13580"],
  "vitrolles_2022": ["14130"],
  "mouans_2023": ["14425"],
  "aix_2023": ["14715", "14716"]
}

def generate_results_file(event_ids):
    """
    Take the event IDs as input, build a structure containing the information about the different apparatuses for the different gymnasts in the different categories, merge the event results together and write the consolidated results in a CSV file.
    """
    results = get_results_events(event_ids)
    vertical_ranking = get_vertical_ranking(results)
    write_results(vertical_ranking)
    print("Finished!")

generate_results_file(EVENT_IDS['mouans_2023'])
