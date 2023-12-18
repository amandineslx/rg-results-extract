import json

def enrich_with_apparatus_rankings(results):
    for category_name in results['categories'].keys():
        category = results['categories'][category_name]
        first_entity = category['general'][0][0]

        if len(first_entity['apparatuses'].keys()) == 1:
            continue

        category['apparatuses'] = {}

        for apparatus in first_entity['apparatuses'].keys():
            entities = []

            # put all the gymnasts in there
            for rank in category['general']:
                for entity in rank:
                    if apparatus in entity['apparatuses']:
                        entities.append(entity)
                    else:
                        print("/!\ Gymnast [%s] in category [%s] has been excluded from ranking with apparatus [%s] as she did not perform with it" % (entity["name"], category_name, apparatus))

            entities.sort(key=lambda e: float(e['apparatuses'][apparatus]['total']), reverse=True)

            category['apparatuses'][apparatus] = entities

    return results
