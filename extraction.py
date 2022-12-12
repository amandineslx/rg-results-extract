import requests

URL_RESULTATS = "https://resultats.ffgym.fr/api/palmares/evenement/"
MARK_TYPES = {'DB': 'DB', 'DA': 'DA', 'Art.': 'A', 'Exé.': 'E', 'Pén.': 'P'}

# EXTRACTION FROM THE FFGYM WEBSITE
def get_results_event_json(event_id):
    url_event = URL_RESULTATS + str(event_id)
    response = requests.get(url = url_event)
    json = response.json()
    return json[0]

# EXTRACTION FROM THE JSON RETRIEVED FROM THE WEBSITE
def get_mark_type_label(mark_type):
    return MARK_TYPES[mark_type]

def format_mark(mark):
    return float(mark)

def get_results_passage(passage):
    # takes as input the passageMarks
    results_passage = dict()

    for mark in passage['corpsMarks']:
        if mark['corps'] in MARK_TYPES.keys():
            results_passage[get_mark_type_label(mark['corps'])] = format_mark(mark['value'])

    return results_passage

def get_results_gymnast(gymnast):
    # takes as input the entity in the palmares
    results_gymnast = dict()

    results_gymnast['last_name'] = gymnast['lastname']
    results_gymnast['first_name'] = gymnast['firstname']
    results_gymnast['club'] = gymnast['club']
    results_gymnast['rank'] = gymnast['markRank']

    gymnast_mark = gymnast['mark']
    results_gymnast['total'] = format_mark(gymnast_mark['value'])
    results_gymnast_apparatuses = dict()

    for mark in gymnast_mark['appMarks']:
        apparatus_label = mark['labelApp'].lower()
        results_gymnast_apparatuses[apparatus_label] = get_results_passage(mark['passageMarks'][0])
        results_gymnast_apparatuses[apparatus_label]['total'] = format_mark(mark['value'])

    results_gymnast['apparatuses'] = results_gymnast_apparatuses

    return results_gymnast

def get_results_category(category):
    # takes as input the category
    results_category = dict()

    for gymnast in category['entities']:
        if str(gymnast['markRank']) not in results_category:
            results_category[str(gymnast['markRank'])] = []
        results_category[str(gymnast['markRank'])].append(get_results_gymnast(gymnast))

    return results_category

def get_results_event(event_id):
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
    results_events = []

    for event_id in event_ids:
        results_events.append(get_results_event(event_id))

    return results_events
