from extraction import get_results_event_json
import csv,json

CONFIG_FILE_NAME = "vitrolles_2023.yml"

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

EVENT_ID = 16178

def add_mark_for_club(club, gymnast_name, division, mark):
    if not club in COUPE_DES_CLUBS.keys():
        COUPE_DES_CLUBS[club] = Club()
    COUPE_DES_CLUBS[club].add_mark(gymnast_name, division, mark)

def format_gymnast_details(gymnast):
    return str(gymnast[0]) + " - " + gymnast[1]

def write_results(sorted_ranking):
    with open('./results/coupe des clubs '+str(EVENT_ID)+'.csv', 'w', encoding='cp1252') as f:
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

def main():
    config = json.load(open("./configs/coupe_des_clubs/" + CONFIG_FILE_NAME))
    event_json = get_results_event_json(EVENT_ID)
    for category_json in event_json['categories']:
        if not category_json['label'] in config.keys():
            continue
        quota_category = config[category_json['label']]['quota']
        category_without_qualified = category_json['entities'][quota_category:]
        for gymnast in category_without_qualified:
            add_mark_for_club(gymnast['club'], gymnast['firstname'] + ' ' + gymnast['lastname'] + ' (' + category_json['label'] + ')', config[category_json['label']]['division'], float(gymnast['mark']['value']))

    ranking = dict(sorted(COUPE_DES_CLUBS.items(), reverse=True, key=lambda c:c[1].get_result()['total']))

    write_results(ranking)

    print("Finished!")

main()
