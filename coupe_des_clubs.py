from extraction import get_results_event_json
import json,csv

CATEGORIES = {
  'Federale 10-11 ans GR': {'quota': 3, 'division': 'fed'},
  'Federale 12-13 ans GR': {'quota': 2, 'division': 'fed'},
  'Federale 14-15 ans GR': {'quota': 4, 'division': 'fed'},
  'Federale 16-17 ans GR': {'quota': 2, 'division': 'fed'},
  'Federale 18 ans et plus GR': {'quota': 3, 'division': 'fed'},
  'Nationale C 10-11 ans GR': {'quota': 5, 'division': 'nat'},
  'Nationale C 12-13 ans GR': {'quota': 3, 'division': 'nat'},
  'Nationale C 14-15 ans GR': {'quota': 3, 'division': 'nat'},
  'Nationale C 16-17 ans GR': {'quota': 4, 'division': 'nat'},
  'Nationale C 18 ans et plus GR': {'quota': 3, 'division': 'nat'}
}

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
    event_json = get_results_event_json(EVENT_ID)
    for category_json in event_json['categories']:
        if not category_json['label'] in CATEGORIES.keys():
            continue
        quota_category = CATEGORIES[category_json['label']]['quota']
        category_without_qualified = category_json['entities'][quota_category:]
        for gymnast in category_without_qualified:
            add_mark_for_club(gymnast['club'], gymnast['firstname'] + ' ' + gymnast['lastname'] + ' (' + category_json['label'] + ')', CATEGORIES[category_json['label']]['division'], float(gymnast['mark']['value']))

    ranking = dict(sorted(COUPE_DES_CLUBS.items(), reverse=True, key=lambda c:c[1].get_result()['total']))

    write_results(ranking)

    print("Finished!")

main()
