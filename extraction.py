import requests,json

from model import Event, Category, Entity, Apparatus
from common import is_regional_category, is_ignored_category, format_mark

URL_RESULTATS = "https://resultats.ffgym.fr/api/palmares/evenement/"
MARK_TYPES = {'DB': 'DB', 'DA': 'DA', 'Art.': 'A', 'Exé.': 'E', 'Pén.': 'P'}

# EXTRACTION FROM THE FFGYM WEBSITE
def get_results_event_json(event_id):
    """
    Retrieve the JSON file from the FFGym website containing the results for a given event.
    """
    url_event = URL_RESULTATS + str(event_id)
    response = requests.get(url = url_event)
    payload = response.json()
    if not payload:
        raise ValueError("No data associated to event %s, it is probably not published yet" % str(event_id))
    elif 'error' in payload:
        raise ValueError("An error was raised with event %s: %s" % (str(event_id), payload['error']))
    return payload[0]

# EXTRACTION FROM THE JSON RETRIEVED FROM THE WEBSITE
def get_results_apparatus(apparatus):
    """
    Build a structure containing the marks for a given apparatus for a given gymnast/team. Takes as input the passageMarks JSON structure from the input JSON.
    """
    results_apparatus = Apparatus()

    for mark in apparatus['corpsMarks']:
        results_apparatus.set_corps_mark(mark['corps'], mark['value'])

    return results_apparatus

def get_results_entity(entity, event_title):
    """
    Build a structure containing the information about a given gymnast/team. Takes as input the entity in the palmares JSON structure from the input JSON.
    """
    entity_mark = entity['mark']

    results_entity = Entity(_build_entity_name(entity), event_title, entity['club'], entity['markRank'], format_mark(entity_mark['value']))

    for mark in entity_mark['appMarks']:
        apparatus_label = mark['labelApp'].lower()
        apparatus = get_results_apparatus(mark['passageMarks'][0])
        apparatus.total = format_mark(mark['value'])
        results_entity.add_apparatus(apparatus_label, apparatus)

    return results_entity

def _build_entity_name(entity):
    if 'firstname' in entity and 'lastname' in entity:
        return entity['lastname'] + ' ' + entity['firstname']
    else:
        return entity['club'] + ' - ' + entity['label']

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

def get_results_event(event_id, event_title, config):
    """
    Build a structure containing the information about a given event. Takes as input the event ID.
    """
    results_event_json = get_results_event_json(event_id)

    results_event = Event(results_event_json['event']['id'], event_title, config.title)

    for category in results_event_json['categories']:
        if is_ignored_category(category['label']):
            continue
        if config.ignore_regionals and is_regional_category(category['label']):
            continue
        results_category = Category(category['label'])
        results_category.general_ranking = get_results_category(category, config.events[event_id])
        results_event.add_category(results_category)

    return results_event

def get_results_events(config):
    """
    Build a structure containing the information about multiple events. Takes as input the list of event IDs.
    """
    results_events = []

    for event_id, event_title in config.events.items():
        try:
            results_events.append(get_results_event(event_id, event_title, config))
        except ValueError as ve:
            print(ve)

    return results_events
