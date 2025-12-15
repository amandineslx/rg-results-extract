from extraction import get_results_events
from merging import merge_event_list
from model import Config, Club
from common import format_mark
import csv,json,sys

COUPE_DES_CLUBS = {}

def add_mark_for_club(club, gymnast_name, division, mark):
    if not club in COUPE_DES_CLUBS.keys():
        COUPE_DES_CLUBS[club] = Club()
    COUPE_DES_CLUBS[club].add_mark(gymnast_name, division, format_mark(mark))

def format_gymnast_details(gymnast):
    return str(gymnast[0]) + " - " + gymnast[1]

def write_results(year, sorted_ranking):
    with open('./results/coupe des clubs '+str(year)+'.csv', 'w', encoding='cp1252') as f:
        writer = csv.writer(f)
        writer.writerow(["Club", "Total", "Gymnast 1", "Gymnast 2", "Gymnast 3", "Gymnast 4"])
        for club in sorted_ranking.keys():
            club_result = sorted_ranking[club].get_result()
            row = [club, round(club_result['total'],3)]
            if len(club_result['gymnasts']) > 0:
                row.append(format_gymnast_details(club_result['gymnasts'][0]))
                row.append(format_gymnast_details(club_result['gymnasts'][1]))
                row.append(format_gymnast_details(club_result['gymnasts'][2]))
                row.append(format_gymnast_details(club_result['gymnasts'][3]))
            writer.writerow(row)

def get_merged_event_results(event_title, event_ids):
    config = Config(event_title)
    config.ignore_regionals = True
    for event_id in event_ids:
        config.add_event(str(event_id), str(event_id))
    events = get_results_events(config)
    return merge_event_list(events)

def main(coupe_des_clubs_config_file):
    config = json.load(open("./configs/coupe_des_clubs/" + coupe_des_clubs_config_file))
    config_categories = config['categories']
    event = get_merged_event_results(coupe_des_clubs_config_file, config['eventIds'])
    for category_name in event.get_category_names():
        category = event.categories[category_name]
        if not category_name in config_categories.keys():
            continue
        quota_category = config_categories[category_name]['quota']
        category_without_qualified = category.general_ranking[quota_category:]
        for rank in category_without_qualified:
            add_mark_for_club(rank[0].club, rank[0].name + ' (' + category_name + ')', config_categories[category_name]['division'], rank[0].total)

    ranking = dict(sorted(COUPE_DES_CLUBS.items(), reverse=True, key=lambda c:c[1].get_result()['total']))

    write_results(config['year'], ranking)

    print("Finished!")

if __name__ == "__main__":
    main(sys.argv[1])
