import json

def enrich_with_apparatus_rankings(event):
    for category_name in event.categories.keys():
        category = event.get_category(category_name)
        first_entity = category.general_ranking[0][0]

        if first_entity.get_apparatuses_number() == 1:
            continue

        for apparatus in first_entity.get_apparatus_names():
            # put all the gymnasts in there
            for rank in category.general_ranking:
                for entity in rank:
                    if apparatus in entity.get_apparatus_names():
                        category.add_entity_apparatus_to_apparatus_ranking(apparatus, entity)
                    else:
                        print(f"/!\ Gymnast [{entity['name']}] in category [{category_name}] has been excluded from ranking with apparatus [{apparatus}] as she did not perform with it")

        category.sort_apparatus_rankings()

    return event
