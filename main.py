from yaml import Loader, load

import sys

from extraction import get_results_events
from merging import get_vertical_ranking
from enriching import enrich_with_apparatus_rankings
from writing import write_results

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
    config.my_club = config_yaml['my_club']
    for event in config_yaml['events']:
        if 'ids' in event and event['ids']:
            config.add_event(str(event['title']), str(event['ids']))
    return config

def generate_results_file(config_file_name):
    """
    Take the event IDs as input, build a structure containing the information about the different apparatuses for the different gymnasts in the different categories, merge the event results together and write the consolidated results in a CSV file.
    """
    config = build_config(config_file_name)
    results = get_results_events(config)
    vertical_ranking = get_vertical_ranking(results)
    enriched_results = enrich_with_apparatus_rankings(vertical_ranking)
    write_results(enriched_results, config)
    print("Finished!")

if __name__ == "__main__":
    generate_results_file(sys.argv[1])
