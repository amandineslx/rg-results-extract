import csv

SCMS = 'SPORTING CLUB MOUANS SARTOUX GYMNASTIQUE RYTHMIQUE'

def get_csv_line_from_entity_apparatus_json(entity_json, category, apparatus, first_entity_total, previous_entity_total):
    """
    Generate a line to be written in the CSV file from the different structures built from the extraction and merging.
    """
    apparatus_json = entity_json['apparatuses'][apparatus]
    return get_csv_line(
        category=category,
        apparatus=apparatus,
        rank=entity_json['rank'],
        name=entity_json['name'],
        club=entity_json['club'],
        scms='x' if entity_json['club'] == SCMS else '',
        db=apparatus_json['DB'],
        da=apparatus_json.get('DA', ''),
        artistry=apparatus_json['A'],
        execution=apparatus_json['E'],
        penalty=apparatus_json['P'],
        apparatus_total=apparatus_json['total'],
        total=entity_json['total'],
        diff_total=round(entity_json['total'] - previous_entity_total, 3),
        diff_total_cumul=round(entity_json['total'] - first_entity_total, 3)
        )

def get_csv_line(
    category='Categorie',
    apparatus='Engin',
    rank='Rang',
    name='Nom',
    club='Club',
    scms='SCMS',
    db='DB',
    da='DA',
    artistry='A',
    execution='EXE',
    penalty='Pen',
    apparatus_total='Total engin',
    total='Total',
    diff_total='Diff total',
    diff_total_cumul='Diff total cumul'):
    """
    Generate a line to be written in the CSV file with all caracteristics for an apparatus of a gymnast/team. Keeping the default values generates a header line.
    """
    return [category, apparatus, rank, name, club, scms, db, da, artistry, execution, penalty, apparatus_total, total, diff_total, diff_total_cumul]

def write_results(results_json):
    """
    Write the event results to a CSV file.
    """
    event_id = results_json['event_id']
    file_name = f"results_{event_id}.csv"

    # create output file
    with open(file_name, 'w', encoding='cp1252') as f:
        writer = csv.writer(f)

        first_entity_total = 0
        previous_entity_total = 0

        # for each category in the event
        for category in results_json['categories'].keys():
            # write header line
            category_json = results_json['categories'][category]

            if len(category_json[0]) == 0:
                continue

            writer.writerow(get_csv_line())

            first_entity = category_json[0][0]
            apparatuses = first_entity['apparatuses'].keys()

            # for each apparatus in the category
            # (all gymnasts/teams in the same category have the same apparatuses)
            for apparatus in apparatuses:
                previous_entity_total = -1

                # for each ranking in the category
                for entities in category_json:
                    # if the gymnast/team is the first one of the category, keep its score to compute the cumulated total difference
                    if previous_entity_total == -1:
                        first_entity_total = entities[0]['total']
                        previous_entity_total = first_entity_total

                    # for each gymnast/team in this ranking
                    for entity in entities:
                        # write score of the gymnast/team apparatus
                        writer.writerow(get_csv_line_from_entity_apparatus_json(entity, category, apparatus, first_entity_total, previous_entity_total))
                        # keep this gymnast/team score as the previous total to compute the difference between this gymnast/team and the next one
                        previous_entity_total = entity['total']
