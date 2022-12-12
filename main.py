from extraction import get_results_events
from merging import get_vertical_ranking
from writing import write_results

EVENT_IDS = {
  "la_colle_2022": [],
  "sollies_2022": ["13579", "13580"],
  "vitrolles_2022": ["14130"]
}

def generate_results_file(event_ids):
    results = get_results_events(event_ids)
    vertical_ranking = get_vertical_ranking(results)
    write_results(vertical_ranking)
    print("Finished!")

generate_results_file(EVENT_IDS['vitrolles_2022'])
