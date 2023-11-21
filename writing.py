import csv,json

def get_csv_line_from_entity_general_json(entity_json, category, display_name, my_club, first_entity_total, previous_entity_total):
    """
    Generate a line to be written in the CSV file from the different structures built from the extraction and merging.
    """
    return get_csv_line(
        category=category,
        apparatus=display_name,
        rank=entity_json['rank'],
        event=entity_json['event'],
        initial_rank=entity_json['initial_rank'],
        name=entity_json['name'],
        club=entity_json['club'],
        my_club='x' if entity_json['club'] == my_club else '',
        db='',
        da='',
        artistry='',
        execution='',
        penalty='',
        apparatus_total='',
        total=entity_json['total'],
        diff_prec=round(entity_json['total'] - previous_entity_total, 3),
        diff_cumul=round(entity_json['total'] - first_entity_total, 3)
        )

def get_csv_line_from_entity_apparatus_json(entity_json, category, apparatus, my_club, first_entity_total, previous_entity_total):
    """
    Generate a line to be written in the CSV file from the different structures built from the extraction and merging.
    """
    apparatus_json = entity_json['apparatuses'][apparatus]
    return get_csv_line(
        category=category,
        apparatus=apparatus,
        rank=entity_json['rank'],
        event=entity_json['event'],
        initial_rank=entity_json['initial_rank'],
        name=entity_json['name'],
        club=entity_json['club'],
        my_club='x' if entity_json['club'] == my_club else '',
        db=apparatus_json['DB'],
        da=apparatus_json.get('DA', ''),
        artistry=apparatus_json['A'],
        execution=apparatus_json['E'],
        penalty=apparatus_json['P'],
        apparatus_total=apparatus_json['total'],
        total='',
        diff_prec=round(apparatus_json['total'] - previous_entity_total, 3),
        diff_cumul=round(apparatus_json['total'] - first_entity_total, 3)
        )

def get_csv_line(
    category='Categorie',
    apparatus='Engin',
    rank='Rang',
    event='Evenement',
    initial_rank='Rang init',
    name='Nom',
    club='Club',
    my_club='Mon club',
    db='DB',
    da='DA',
    artistry='A',
    execution='EXE',
    penalty='Pen',
    apparatus_total='Total engin',
    total='Total',
    diff_prec='Diff prec',
    diff_cumul='Diff cumul'):
    """
    Generate a line to be written in the CSV file with all caracteristics for an apparatus of a gymnast/team. Keeping the default values generates a header line.
    """
    return [category, apparatus, rank, event, initial_rank, name, club, my_club, db, da, artistry, execution, penalty, apparatus_total, total, diff_prec, diff_cumul]

def write_general(category, display_name, ranking, writer, config, writing_method):
    my_club = config.my_club

    first_entity = ranking[0][0]

    previous_entity_total = -1

    # for each rank in the category
    rank = 1
    for entities in ranking:
        # if the gymnast/team is the first one of the category, keep its score to compute the cumulated total difference
        if previous_entity_total == -1:
            first_entity_total = entities[0]['total']
            previous_entity_total = first_entity_total

        # for each gymnast/team in this rank
        for entity in entities:
            # write score of the gymnast/team apparatus
            entity['rank'] = rank

            writer.writerow(writing_method(entity, category, display_name, my_club, first_entity_total, previous_entity_total))

            # keep this gymnast/team score as the previous total to compute the difference between this gymnast/team and the next one
            previous_entity_total = entity['total']
            rank += 1

def write_apparatus(category, apparatus, ranking, writer, config):
    my_club = config.my_club

    first_entity = ranking[0]
    previous_entity_total = -1

    # for each rank in the category
    rank = 1
    for entity in ranking:
        # if the gymnast/team is the first one of the category, keep its score to compute the cumulated total difference
        if previous_entity_total == -1:
            first_entity_total = entity['apparatuses'][apparatus]['total']
            previous_entity_total = first_entity_total

        # write score of the gymnast/team apparatus
        entity['rank'] = rank
        writer.writerow(get_csv_line_from_entity_apparatus_json(entity, category, apparatus, my_club, first_entity_total, previous_entity_total))

        # keep this gymnast/team score as the previous total to compute the difference between this gymnast/team and the next one
        previous_entity_total = entity['apparatuses'][apparatus]['total']
        rank += 1

def write_results(results_json, config):
    """
    Write the event results to a CSV file.
    """
    file_name = f"results_{config.title}.csv"

    # create output file
    with open('./results/'+file_name, 'w', encoding='cp1252') as f:
        writer = csv.writer(f)

        first_entity_total = 0
        previous_entity_total = 0

        # for each category in the event
        for category in results_json['categories'].keys():
            # write header line
            category_json = results_json['categories'][category]

            if len(category_json['general'][0]) == 0:
                continue

            writer.writerow(get_csv_line())

            apparatuses = list(category_json['general'][0][0]['apparatuses'].keys())

            if len(apparatuses) > 1:
                # for each apparatus in the category
                # (all gymnasts/teams in the same category have the same apparatuses)
                for apparatus in apparatuses:
                    write_apparatus(category, apparatus, category_json['apparatuses'][apparatus], writer, config)

                write_general(category, 'general', results_json['categories'][category]['general'], writer, config, get_csv_line_from_entity_general_json)

            else:
                write_general(category, apparatuses[0], results_json['categories'][category]['general'], writer, config, get_csv_line_from_entity_apparatus_json)
