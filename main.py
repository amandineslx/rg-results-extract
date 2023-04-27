from yaml import Loader, load

from extraction import get_results_events
from merging import get_vertical_ranking
from writing import write_results

EVENT_IDS = {
  "la_colle_2022": "indiv_dep_2022_la_colle.yml",
  "sollies_2022": "indiv_interdep_2022_sollies.yml",
  "vitrolles_2022": "indiv_regions_2022_vitrolles.yml",
  "mouans_2023": "ensembles_dep_2023_mouans.yml",
  "aix_2023": "ensembles_interdep_2023_aix.yml",
  "istres_2023": "ensembles_regions_2023_istres.yml",
  "simu_france_2023": "ensembles_simu_france_2023.yml"
}

class Config:
    def __init__(self, title):
        self.title = title
        self.ignore_regionals = False
        self.events = dict()

    def add_event(self, event_title, event_ids):
        for event_id in event_ids.split(','):
            self.events[event_id] = event_title

def build_config(event_config_file):
    config_yaml = load(open("./configs/" + event_config_file), Loader=Loader)
    config = Config(str(config_yaml['title']))
    reg_indicator = "false" if not 'ignore_regionals' in config_yaml else str(config_yaml['ignore_regionals'])
    config.ignore_regionals = False if not reg_indicator else reg_indicator == "True"
    for event in config_yaml['events']:
        config.add_event(str(event['title']), str(event['ids']))
    return config

def generate_results_file(config_file_name):
    """
    Take the event IDs as input, build a structure containing the information about the different apparatuses for the different gymnasts in the different categories, merge the event results together and write the consolidated results in a CSV file.
    """
    config = build_config(config_file_name)
    results = get_results_events(config)
    vertical_ranking = get_vertical_ranking(results)
    write_results(vertical_ranking, config)
    print("Finished!")

generate_results_file(EVENT_IDS['simu_france_2023'])
