from yaml import Loader,load

import sys

from extraction import get_results_events
from merging import merge_event_list
from enriching import enrich_with_apparatus_rankings
from writing import write_results
from model import Config

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
    events = get_results_events(config)
    for event in events:
        print(event.to_string())
    merged_event = merge_event_list(events)
    enriched_results = enrich_with_apparatus_rankings(merged_event)
    write_results(enriched_results, config)
    print("Finished!")

if __name__ == "__main__":
    generate_results_file(sys.argv[1])
