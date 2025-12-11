from extraction import get_results_event_json, get_results_events
from merging import merge_events, get_vertical_ranking
from main import Config
import csv,json,sys

class Club:
    def __init__(self):
        self.nat = []
        self.fed = []

    def get_result(self):
        nationales = sorted(self.nat, reverse=True)
        federales = sorted(self.fed, reverse=True)
        if not nationales or not federales or len(federales) < 3:
            return {"gymnasts": [], "total": 0}
        gymnasts = [nationales[0], federales[0], federales[1], federales[2]]
        return {"gymnasts": gymnasts, "total": sum(mark for mark,_ in gymnasts)}

    def add_mark(self, gymnast_name, division, mark):
        if division == 'fed':
            self.fed.append((mark, gymnast_name))
        elif division == 'nat':
            self.nat.append((mark, gymnast_name))

COUPE_DES_CLUBS = {}

def add_mark_for_club(club, gymnast_name, division, mark):
    if not club in COUPE_DES_CLUBS.keys():
        COUPE_DES_CLUBS[club] = Club()
    COUPE_DES_CLUBS[club].add_mark(gymnast_name, division, mark)

def format_gymnast_details(gymnast):
    return str(gymnast[0]) + " - " + gymnast[1]

def write_results(event_id, sorted_ranking):
    with open('./results/coupe des clubs '+str(event_id)+'.csv', 'w', encoding='cp1252') as f:
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
    results = get_results_events(config)
    return get_vertical_ranking(results)

def main(coupe_des_clubs_config_file):
    config = json.load(open("./configs/coupe_des_clubs/" + coupe_des_clubs_config_file))
    categories = config['categories']
    event_json = get_merged_event_results(coupe_des_clubs_config_file, config['eventIds'])
    for category_name in event_json['categories']:
        category_json = event_json['categories'][category_name]
        if not category_name in categories.keys():
            continue
        quota_category = categories[category_name]['quota']
        category_without_qualified = category_json['general'][quota_category:]
        for gymnast in category_without_qualified:
            add_mark_for_club(gymnast[0]['club'], gymnast[0]['name'] + ' (' + category_name + ')', categories[category_name]['division'], float(gymnast[0]['total']))

    ranking = dict(sorted(COUPE_DES_CLUBS.items(), reverse=True, key=lambda c:c[1].get_result()['total']))

    write_results(str(config['eventIds'][0]), ranking)

    print("Finished!")

if __name__ == "__main__":
    main(sys.argv[1])
