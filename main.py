from yaml import Loader, load

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
  "simu_france_2023": "simu-france-2023.yml"
}

class Config:
    def __init__(self, title):
        self.title = title
        self.events = dict()

    def add_event(self, event_title, event_ids):
        for event_id in str(event_ids).split(','):
            self.events[event_id] = event_title

def build_config(event_config_file):
    config_yaml = load(open("./configs/" + event_config_file), Loader=Loader)
    config = Config(config_yaml['title'])
    for event in config_yaml['events']:
        config.add_event(event['title'], event['ids'])
    return config

def generate_results_file(config_file_name):
    """
    Take the event IDs as input, build a structure containing the information about the different apparatuses for the different gymnasts in the different categories, merge the event results together and write the consolidated results in a CSV file.
    """
    config = build_config(config_file_name)
    results = get_results_events(config)
    vertical_ranking = get_vertical_ranking(results)
    write_results(vertical_ranking, config.title)
    print("Finished!")

generate_results_file(EVENT_IDS['simu_france_2023'])
