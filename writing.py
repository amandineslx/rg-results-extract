import csv

def get_csv_line_from_entity_general_json(entity, category, display_name, my_club, first_entity_total, previous_entity_total, multiple_apparatuses):
    """
    Generate a line to be written in the CSV file from the different structures built from the extraction and merging.
    """
    return get_csv_line(
        category=category.label,
        apparatus=display_name,
        rank=entity.rank,
        event=entity.event_label,
        initial_rank=entity.initial_rank,
        name=entity.name,
        club=entity.club,
        my_club='x' if entity.club == my_club else '',
        db='',
        da='',
        artistry='',
        execution='',
        penalty='',
        apparatus_total='',
        total=entity.total,
        diff_prec=round(entity.total - previous_entity_total, 3),
        diff_cumul=round(entity.total - first_entity_total, 3)
        )

def get_csv_line_from_entity_apparatus_json(entity, category, apparatus_name, my_club, first_entity_total, previous_entity_total, multiple_apparatuses):
    """
    Generate a line to be written in the CSV file from the different structures built from the extraction and merging.
    """
    apparatus = entity.apparatuses[apparatus_name]
    return get_csv_line(
        category=category.label,
        apparatus=apparatus_name if multiple_apparatuses else 'general/' + apparatus_name,
        rank=entity.rank,
        event=entity.event_label,
        initial_rank=entity.initial_rank,
        name=entity.name,
        club=entity.club,
        my_club='x' if entity.club == my_club else '',
        db=apparatus.db,
        da=apparatus.da,
        artistry=apparatus.artistry,
        execution=apparatus.execution,
        penalty=apparatus.penalty,
        apparatus_total=apparatus.total,
        total='',
        diff_prec=round(apparatus.total - previous_entity_total, 3),
        diff_cumul=round(apparatus.total - first_entity_total, 3)
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

def write_general(category, ranking, writer, config, multiple_apparatuses):
    my_club = config.my_club

    first_entity = ranking[0][0]

    previous_entity_total = -1

    if multiple_apparatuses:
        writing_method = get_csv_line_from_entity_general_json
        apparatus = 'general'
    else:
        writing_method = get_csv_line_from_entity_apparatus_json
        apparatus = category.get_apparatus_names()[0]

    # for each rank in the category
    rank = 1
    for entities in ranking:
        # if the gymnast/team is the first one of the category, keep its score to compute the cumulated total difference
        if previous_entity_total == -1:
            first_entity_total = entities[0].total
            previous_entity_total = first_entity_total

        # for each gymnast/team in this rank
        for entity in entities:
            # write score of the gymnast/team apparatus
            entity.rank = rank
            writer.writerow(writing_method(entity, category, apparatus, my_club, first_entity_total, previous_entity_total, multiple_apparatuses))

            # keep this gymnast/team score as the previous total to compute the difference between this gymnast/team and the next one
            previous_entity_total = entity.total
            rank += 1

def write_apparatus(category, apparatus_name, ranking, writer, config):
    my_club = config.my_club

    first_entity = ranking[0]
    previous_entity_total = -1

    # for each rank in the category
    rank = 1
    for entity in ranking:
        # if the gymnast/team is the first one of the category, keep its score to compute the cumulated total difference
        if previous_entity_total == -1:
            first_entity_total = entity.apparatuses[apparatus_name].total
            previous_entity_total = first_entity_total

        # write score of the gymnast/team apparatus
        entity.rank = rank
        writer.writerow(get_csv_line_from_entity_apparatus_json(entity, category, apparatus_name, my_club, first_entity_total, previous_entity_total, multiple_apparatuses=True))

        # keep this gymnast/team score as the previous total to compute the difference between this gymnast/team and the next one
        previous_entity_total = entity.apparatuses[apparatus_name].total
        rank += 1

def write_results(event, config):
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
        categorie_names = event.get_category_names()
        categorie_names.sort()
        for category_name in categorie_names:
            # write header line
            category = event.categories[category_name]

            if category.is_empty():
                continue

            writer.writerow(get_csv_line())

            apparatuse_names = category.get_apparatus_names()

            multiple_apparatuses = False

            if len(apparatuse_names) > 1:
                multiple_apparatuses = True

                # for each apparatus in the category
                # (all gymnasts/teams in the same category have the same apparatuses)
                for apparatus_name in apparatuse_names:
                    write_apparatus(category, apparatus_name, category.apparatus_rankings[apparatus_name], writer, config)

            write_general(category, category.general_ranking, writer, config, multiple_apparatuses)
