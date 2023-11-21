import requests

URL_RESULTATS = "https://resultats.ffgym.fr/api/palmares/evenement/"
MARK_TYPES = {'DB': 'DB', 'DA': 'DA', 'Art.': 'A', 'Exé.': 'E', 'Pén.': 'P'}

# EXTRACTION FROM THE FFGYM WEBSITE
def get_results_event_json(event_id):
    """
    Retrieve the JSON file from the FFGym website containing the results for a given event.
    """
    url_event = URL_RESULTATS + str(event_id)
    response = requests.get(url = url_event)
    json = response.json()
    if not json:
        raise ValueError("No data associated to event %s, it is probably not published yet" % str(event_id))
    return json[0]

# EXTRACTION FROM THE JSON RETRIEVED FROM THE WEBSITE
def get_mark_type_label(mark_type):
    """
    Get the final mark type label corresponding to a FFGym mark type label.
    """
    return MARK_TYPES[mark_type]

def format_mark(mark):
    """
    Format the mark to remove additional decimals.
    """
    return float(mark)

def get_results_apparatus(passage):
    """
    Build a structure containing the marks for a given apparatus for a given gymnast/team. Takes as input the passageMarks JSON structure from the input JSON.
    """
    results_passage = dict()

    for mark in passage['corpsMarks']:
        if mark['corps'] in MARK_TYPES.keys():
            results_passage[get_mark_type_label(mark['corps'])] = format_mark(mark['value'])

    return results_passage

def get_results_entity(entity, event_title):
    """
    Build a structure containing the information about a given gymnast/team. Takes as input the entity in the palmares JSON structure from the input JSON.
    """
    results_entity = dict()

    if 'firstname' in entity and 'lastname' in entity:
        results_entity['name'] = entity['lastname'] + ' ' + entity['firstname']
    else:
        results_entity['name'] = entity['club'] + ' - ' + entity['label']

    results_entity['event'] = event_title
    results_entity['club'] = entity['club']
    results_entity['initial_rank'] = entity['markRank']

    entity_mark = entity['mark']
    results_entity['total'] = format_mark(entity_mark['value'])
    results_entity_apparatuses = dict()

    for mark in entity_mark['appMarks']:
        apparatus_label = mark['labelApp'].lower()
        results_entity_apparatuses[apparatus_label] = get_results_apparatus(mark['passageMarks'][0])
        results_entity_apparatuses[apparatus_label]['total'] = format_mark(mark['value'])

    results_entity['apparatuses'] = results_entity_apparatuses

    return results_entity

def get_results_category(category, event_title):
    """
    Build a structure containing the information about a given category. Takes as input the category JSON structure from the input JSON.
    """
    # takes as input the category
    results_category = []

    previous_entity_rank = 1
    entities_for_rank = []

    for entity in category['entities']:
        if entity['markRank'] == previous_entity_rank:
            entities_for_rank.append(get_results_entity(entity, event_title))
        else:
            results_category.append(entities_for_rank)
            entities_for_rank = [get_results_entity(entity, event_title)]
            previous_entity_rank = entity['markRank']
    results_category.append(entities_for_rank)

    return results_category

def _is_regional_category(category_label):
    return _category_contains_any_label(category_label, ["régional", "fédérale r", "regional"])

def _is_ignored_category(category_label):
    return _category_contains_any_label(category_label, ["nationale par equipe"])

def _category_contains_any_label(category_label, labels):
    for label in labels:
        if label in category_label.lower():
            return True
    return False

def get_results_event(event_id, config):
    """
    Build a structure containing the information about a given event. Takes as input the event ID.
    """
    results_event_json = get_results_event_json(event_id)

    results_event = dict()

    results_event['event_id'] = results_event_json['event']['id']
    results_event['event_label'] = results_event_json['event']['libelle']
    results_event['event_title'] = config.title

    categories = dict()

    for category in results_event_json['categories']:
        if _is_ignored_category(category['label']):
            continue
        if config.ignore_regionals and _is_regional_category(category['label']):
            continue
        categories[category['label']] = {}
        categories[category['label']]['general'] = get_results_category(category, config.events[event_id])

    results_event['categories'] = categories

    return results_event

def get_results_events(config):
    """
    Build a structure containing the information about multiple events. Takes as input the list of event IDs.
    """
    results_events = []

    for event_id, event_title in config.events.items():
        results_events.append(get_results_event(event_id, config))

    return results_events
