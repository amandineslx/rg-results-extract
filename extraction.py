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
    Build a structure containing the marks for a given apparatus for a given gymnast. Takes as input the passageMarks JSON structure from the input JSON.
    """
    results_passage = dict()

    for mark in passage['corpsMarks']:
        if mark['corps'] in MARK_TYPES.keys():
            results_passage[get_mark_type_label(mark['corps'])] = format_mark(mark['value'])

    return results_passage

def get_results_gymnast(gymnast):
    """
    Build a structure containing the information about a given gymnast. Takes as input the entity in the palmares JSON structure from the input JSON.
    """
    results_gymnast = dict()

    if 'firstname' in gymnast and 'lastname' in gymnast:
        results_gymnast['name'] = gymnast['lastname'] + ' ' + gymnast['firstname']
    else:
        results_gymnast['name'] = gymnast['club'] + ' - ' + gymnast['label']

    results_gymnast['club'] = gymnast['club']
    results_gymnast['rank'] = gymnast['markRank']

    gymnast_mark = gymnast['mark']
    results_gymnast['total'] = format_mark(gymnast_mark['value'])
    results_gymnast_apparatuses = dict()

    for mark in gymnast_mark['appMarks']:
        apparatus_label = mark['labelApp'].lower()
        results_gymnast_apparatuses[apparatus_label] = get_results_apparatus(mark['passageMarks'][0])
        results_gymnast_apparatuses[apparatus_label]['total'] = format_mark(mark['value'])

    results_gymnast['apparatuses'] = results_gymnast_apparatuses

    return results_gymnast

def get_results_category(category):
    """
    Build a structure containing the information about a given category. Takes as input the category JSON structure from the input JSON.
    """
    # takes as input the category
    results_category = []

    previous_gymnast_rank = 1
    gymnasts_for_rank = []

    for gymnast in category['entities']:
        if gymnast['markRank'] == previous_gymnast_rank:
            gymnasts_for_rank.append(get_results_gymnast(gymnast))
        else:
            results_category.append(gymnasts_for_rank)
            gymnasts_for_rank = [get_results_gymnast(gymnast)]
            previous_gymnast_rank = gymnast['markRank']
    results_category.append(gymnasts_for_rank)

    return results_category

def get_results_event(event_id):
    """
    Build a structure containing the information about a given event. Takes as input the event ID.
    """
    results_event_json = get_results_event_json(event_id)

    results_event = dict()

    results_event['event_id'] = results_event_json['event']['id']
    results_event['event_label'] = results_event_json['event']['libelle']

    categories = dict()

    for category in results_event_json['categories']:
        categories[category['label']] = get_results_category(category)

    results_event['categories'] = categories

    return results_event

def get_results_events(event_ids):
    """
    Build a structure containing the information about multiple events. Takes as input the list of event IDs.
    """
    results_events = []

    for event_id in event_ids:
        results_events.append(get_results_event(event_id))

    return results_events
