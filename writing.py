import csv

SCMS = 'SPORTING CLUB MOUANS SARTOUX GYMNASTIQUE RYTHMIQUE'

def get_csv_line_from_gymnast_apparatus_json(gymnast_json, category, apparatus, first_gymnast_total, previous_gymnast_total):
    """
    Generate a line to be written in the CSV file from the different structures built from the extraction and merging.
    """
    apparatus_json = gymnast_json['apparatuses'][apparatus]
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
        apparatus_total=apparatus_json['total'],
        total=gymnast_json['total'],
        diff_total=round(gymnast_json['total'] - previous_gymnast_total, 3),
        diff_total_cumul=round(gymnast_json['total'] - first_gymnast_total, 3)
        )

def get_csv_line(
    category='Categorie',
    apparatus='Engin',
    rank='Rang',
    last_name='Nom',
    first_name='Prenom',
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
    Generate a line to be written in the CSV file with all caracteristics for an apparatus of a gymnast. Keeping the default values generates a header line.
    """
    return [category, apparatus, rank, last_name, first_name, club, scms, db, da, artistry, execution, penalty, apparatus_total, total, diff_total, diff_total_cumul]

def write_results(results_json):
    """
    Write the event results to a CSV file.
    """
    event_id = results_json['event_id']
    file_name = f"results_{event_id}.csv"

    # create output file
    with open(file_name, 'w', encoding='cp1252') as f:
        writer = csv.writer(f)

        first_gymnast_total = 0
        previous_gymnast_total = 0

        # for each category in the event
        for category in results_json['categories'].keys():
            # write header line
            writer.writerow(get_csv_line())

            category_json = results_json['categories'][category]
            first_gymnast = category_json[0][0]
            apparatuses = first_gymnast['apparatuses'].keys()

            # for each apparatus in the category
            # (all gymnast in the same category have the same apparatuses)
            for apparatus in apparatuses:
                previous_gymnast_total = -1

                # for each ranking in the category
                for gymnasts in category_json:
                    # if the gymnast is the first one of the category, keep its score to compute the cumulated total difference
                    if previous_gymnast_total == -1:
                        first_gymnast_total = gymnasts[0]['total']
                        previous_gymnast_total = first_gymnast_total

                    # for each gymnast in this ranking
                    for gymnast in gymnasts:
                        # write score of the gymnast apparatus
                        writer.writerow(get_csv_line_from_gymnast_apparatus_json(gymnast, category, apparatus, first_gymnast_total, previous_gymnast_total))
                        # keep this gymnast score as the previous total to compute the difference between this gymnast and the next one
                        previous_gymnast_total = gymnast['total']
