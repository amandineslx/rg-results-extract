import csv

SCMS = 'SPORTING CLUB MOUANS SARTOUX GYMNASTIQUE RYTHMIQUE'

def get_apparatus_list(gymnast_json):
    return list(gymnast_json['apparatuses'].keys())

def get_csv_line_from_gymnast_json(gymnast_json, category, apparatus, first_gymnast_total, previous_gymnast_total):
    apparatus_json = gymnast_json['apparatuses'][apparatus]
    # TODO handle multiple apparatuses
    return get_csv_line(
        category=category,
        apparatus=apparatus,
        rank=gymnast_json['rank'],
        last_name=gymnast_json['last_name'],
        first_name=gymnast_json['first_name'],
        club=gymnast_json['club'],
        scms='x' if gymnast_json['club'] == SCMS else '',
        db=apparatus_json['DB'],
        da=apparatus_json.get('DA', ''),
        artistry=apparatus_json['A'],
        execution=apparatus_json['E'],
        penalty=apparatus_json['P'],
        total=apparatus_json['total'],
        diff_total=round(apparatus_json['total']-previous_gymnast_total, 3),
        diff_total_cumul=round(apparatus_json['total']-first_gymnast_total, 3)
        )

def get_csv_line(category='Category', apparatus='Engin', rank='Rang', last_name='Nom', first_name='Prenom', club='Club', scms='SCMS', db='DB', da='DA', artistry='A', execution='EXE', penalty='Pen', total='Total', diff_total='Diff total', diff_total_cumul='Diff total cumul'):
    return [category, apparatus, rank, last_name, first_name, club, scms, db, da, artistry, execution, penalty, total, diff_total, diff_total_cumul]

def get_gymnast_total(gymnast_json):
    total = 0
    for apparatus in gymnast_json['apparatuses'].keys():
        total = total + gymnast_json['apparatuses'][apparatus]['total']
    return total

def write_results(results_json):
    event_id = results_json['event_id']
    file_name = f"results_{event_id}.csv"

    with open(file_name, 'w', encoding='cp1252') as f:
        writer = csv.writer(f)
        first_gymnast_total = 0
        previous_gymnast_total = 0
        for category in results_json['categories'].keys():
            writer.writerow(get_csv_line())
            category_json = results_json['categories'][category]
            first_gymnast = category_json[0][0]
            apparatuses = first_gymnast['apparatuses'].keys()
            for apparatus in apparatuses:
                previous_gymnast_total = -1
                for gymnasts in category_json:
                    if previous_gymnast_total == -1:
                        first_gymnast_total = get_gymnast_total(gymnasts[0])
                        previous_gymnast_total = first_gymnast_total
                    for gymnast in gymnasts:
                        writer.writerow(get_csv_line_from_gymnast_json(gymnast, category, apparatus, first_gymnast_total, previous_gymnast_total))
                        previous_gymnast_total = get_gymnast_total(gymnast)
