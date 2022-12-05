import requests
import json

EVENTS = ['13579', '13580']
URL_RESULTATS = "https://resultats.ffgym.fr/api/palmares/evenement/"

MARK_TYPES = {'DB': 'DB', 'DA': 'DA', 'Art.': 'A', 'Exé.': 'E', 'Pén.': 'P'}

def get_results_event_json(event_id):
    url_event = URL_RESULTATS + str(event_id)
    response = requests.get(url = url_event)
    json = response.json()
    return json[0]

def get_vertical_ranking(event_ids):
    event_results = []

    for event_id in EVENTS:
        event_results.append(get_results_event(get_results_event_json(event_id)))

    vertical_ranking = dict()

    for event in event_results:
        vertical_ranking = merge_events(vertical_ranking, event)

    return vertical_ranking

def merge_events(event1, event2):
    merge = dict()

    merge['event_id'] = 0
    merge['event_label'] = f"Classement vertical events [{','.join(EVENTS)}]"

    merge['categories'] = dict()

    categories = set(event1.get('categories', {}).keys()).union(set(event2.get('categories', {}).keys()))

    for category in categories:
        merge['categories'][category] = merge_categories(event1, event1.get('categories', {}).get(category, None), event2, event2.get('categories', {}).get(category, None))

    return merge

def merge_categories(event1, category1, event2, category2):
    if not category1 and not category2:
        return {}
    if not category1:
        return category2
    if not category2:
        return category1

    category = dict()

    i_cat1 = 1
    i_cat2 = 1
    i_cat = 1

    while i_cat1 <= len(category1)+1 and i_cat2 <= len(category2)+1:
        gymnast1 = category1.get(str(i_cat1), None)
        if gymnast1:
            gymnast1['event_id'] = event1['event_id']
            gymnast1['event_label'] = event1['event_label']
        gymnast2 = category2.get(str(i_cat2), None)
        if gymnast2:
            gymnast2['event_id'] = event2['event_id']
            gymnast2['event_label'] = event2['event_label']
        
        comparison = compare_gymnasts(gymnast1, gymnast2)
        if comparison == 0:
            i_cat1+=1
            i_cat2+=1
        elif comparison < 0:
            category[str(i_cat)] = gymnast1
            i_cat1+=1
            i_cat+=1
        else:
            category[str(i_cat)] = gymnast2
            i_cat2+=1
            i_cat+=1

    return category

def compare_gymnasts(gymnast1, gymnast2):
    if not gymnast1 and not gymnast2:
        return 0
    if not gymnast1:
        return 1
    if not gymnast2:
        return -1

    gym1_total = gymnast1['total']
    gym2_total = gymnast2['total']

    if gym1_total > gym2_total:
        return -1
    if gym1_total < gym2_total:
        return 1
    if gym1_total == gym2_total:
        gym1_exe = 0
        gym2_exe = 0

        for apparatus in gymnast1['apparatuses'].keys():
            gym1_exe += gymnast1['apparatuses'][apparatus]['E']

        for apparatus in gymnast2['apparatuses'].keys():
            gym2_exe += gymnast2['apparatuses'][apparatus]['E']

        if gym1_exe >= gym2_exe:
            return -1
        else:
            return 1

def get_results_event(event_json):
    results_event = dict()

    results_event['event_id'] = event_json['event']['id']
    results_event['event_label'] = event_json['event']['libelle']

    categories = dict()

    for category in event_json['categories']:
        categories[category['label']] = get_results_category(category)

    results_event['categories'] = categories

    return results_event

def get_results_category(category):
    # takes as input the category
    results_category = dict()

    for gymnast in category['entities']:
        results_category[str(gymnast['markRank'])] = get_results_gymnast(gymnast)

    return results_category

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

def get_results_passage(passage):
    # takes as input the passageMarks
    results_passage = dict()

    for mark in passage['corpsMarks']:
        if mark['corps'] in MARK_TYPES.keys():
            results_passage[get_mark_type_label(mark['corps'])] = format_mark(mark['value'])

    return results_passage

def get_mark_type_label(mark_type):
    return MARK_TYPES[mark_type]

def format_mark(mark):
    return float(mark)

# test get_results_event_json
#print(get_results_event_json(13579))

# test get_passage
#PASSAGE = '{"id":667267,"passage":1,"value":"18.8000000000","dossart":397,"corpsMarks":[{"id":2395611,"corps":"DB","value":"2.7000000000","dossart":397,"ordre":1},{"id":2395612,"corps":"DA","value":"2.4000000000","dossart":397,"ordre":2},{"id":2395613,"corps":"Art.","value":"7.4000000000","dossart":397,"ordre":3},{"id":2395614,"corps":"Exé.","value":"6.9000000000","dossart":397,"ordre":4},{"id":2395615,"corps":"Pén.","value":"0.6000000000","dossart":397,"ordre":5},{"id":2395616,"corps":"DIFFICULTE 2023","value":"5.1000000000","dossart":397}]}'
#print(get_results_passage(json.loads(PASSAGE)))

# test get_results_gymnast
#GYMNAST = '{"markRank":1,"id":2429459,"type":"IND","lastname":"DARRIGADE","firstname":"Fanny","licence":"93006.106.00586","idClub":2500,"club":"SPORTING CLUB MOUANS SARTOUX GYMNASTIQUE RYTHMIQUE","city":"MOUANS SARTOUX","dossart":397,"nationality":"FRA","mark":{"id":206939,"value":"36.8660000000","rank":1,"dossart":397,"entityType":"IND","appMarks":[{"id":726348,"labelApp":"Massues","codeApp":"015","value":"18.8000000000","dossart":397,"rank":1,"passageMarks":[{"id":667267,"passage":1,"value":"18.8000000000","dossart":397,"corpsMarks":[{"id":2395611,"corps":"DB","value":"2.7000000000","dossart":397,"ordre":1},{"id":2395612,"corps":"DA","value":"2.4000000000","dossart":397,"ordre":2},{"id":2395613,"corps":"Art.","value":"7.4000000000","dossart":397,"ordre":3},{"id":2395614,"corps":"Exé.","value":"6.9000000000","dossart":397,"ordre":4},{"id":2395615,"corps":"Pén.","value":"0.6000000000","dossart":397,"ordre":5},{"id":2395616,"corps":"DIFFICULTE 2023","value":"5.1000000000","dossart":397}]}]},{"id":726349,"labelApp":"Ruban","codeApp":"017","value":"18.0660000000","dossart":397,"rank":1,"passageMarks":[{"id":667268,"passage":1,"value":"18.0660000000","dossart":397,"corpsMarks":[{"id":2395617,"corps":"DB","value":"2.8000000000","dossart":397,"ordre":1},{"id":2395618,"corps":"DA","value":"2.3000000000","dossart":397,"ordre":2},{"id":2395619,"corps":"Art.","value":"6.5000000000","dossart":397,"ordre":3},{"id":2395620,"corps":"Exé.","value":"6.4660000000","dossart":397,"ordre":4},{"id":2395621,"corps":"Pén.","value":"0E-10","dossart":397,"ordre":5},{"id":2395622,"corps":"DIFFICULTE 2023","value":"5.1000000000","dossart":397}]}]}]}}'
#print(get_results_gymnast(json.loads(GYMNAST)))

# test get_results_category
#CATEGORY = '{"id":216225,"label":"Nationale B 16-17 ans GR","code":"R0930220.47651.IDAX1","labelDiscipline":"GYM RYTHMIQUE","codeDiscipline":"GR","corpsMarksLabels":["DB","DA","Art.","Exé.","Pén.","DIFFICULTE 2023"],"event":{"id":13579,"libelle":"GR / INTERDEPART 04-05-06-98-84 / CHPT INDIVIDUEL","lieu":"SOLLIES-PONT","dateDebut":"2022-11-12T00:00:00.000+00:00","dateFin":"2022-11-13T00:00:00.000+00:00"},"entityType":"IND","apparatus":[{"id":17,"label":"Ruban","code":"017","nbPassage":1},{"id":15,"label":"Massues","code":"015","nbPassage":1}],"entities":[{"markRank":1,"id":2429459,"type":"IND","lastname":"DARRIGADE","firstname":"Fanny","licence":"93006.106.00586","idClub":2500,"club":"SPORTING CLUB MOUANS SARTOUX GYMNASTIQUE RYTHMIQUE","city":"MOUANS SARTOUX","dossart":397,"nationality":"FRA","mark":{"id":206939,"value":"36.8660000000","rank":1,"dossart":397,"entityType":"IND","appMarks":[{"id":726348,"labelApp":"Massues","codeApp":"015","value":"18.8000000000","dossart":397,"rank":1,"passageMarks":[{"id":667267,"passage":1,"value":"18.8000000000","dossart":397,"corpsMarks":[{"id":2395611,"corps":"DB","value":"2.7000000000","dossart":397,"ordre":1},{"id":2395612,"corps":"DA","value":"2.4000000000","dossart":397,"ordre":2},{"id":2395613,"corps":"Art.","value":"7.4000000000","dossart":397,"ordre":3},{"id":2395614,"corps":"Exé.","value":"6.9000000000","dossart":397,"ordre":4},{"id":2395615,"corps":"Pén.","value":"0.6000000000","dossart":397,"ordre":5},{"id":2395616,"corps":"DIFFICULTE 2023","value":"5.1000000000","dossart":397}]}]},{"id":726349,"labelApp":"Ruban","codeApp":"017","value":"18.0660000000","dossart":397,"rank":1,"passageMarks":[{"id":667268,"passage":1,"value":"18.0660000000","dossart":397,"corpsMarks":[{"id":2395617,"corps":"DB","value":"2.8000000000","dossart":397,"ordre":1},{"id":2395618,"corps":"DA","value":"2.3000000000","dossart":397,"ordre":2},{"id":2395619,"corps":"Art.","value":"6.5000000000","dossart":397,"ordre":3},{"id":2395620,"corps":"Exé.","value":"6.4660000000","dossart":397,"ordre":4},{"id":2395621,"corps":"Pén.","value":"0E-10","dossart":397,"ordre":5},{"id":2395622,"corps":"DIFFICULTE 2023","value":"5.1000000000","dossart":397}]}]}]}},{"markRank":2,"id":2671397,"type":"IND","lastname":"LORENZELLI","firstname":"Lorine","licence":"93006.056.20220","idClub":1947,"club":"ASSOCIATION INTERCOMMUNALE SPORTIVE ET ARTISTIQUE GR Côte d\'Azur","city":"CARROS","dossart":414,"nationality":"FRA","mark":{"id":206938,"value":"33.9310000000","rank":2,"dossart":414,"entityType":"IND","appMarks":[{"id":726346,"labelApp":"Massues","codeApp":"015","value":"16.2320000000","dossart":414,"rank":3,"passageMarks":[{"id":667265,"passage":1,"value":"16.2320000000","dossart":414,"corpsMarks":[{"id":2395599,"corps":"DB","value":"3.2000000000","dossart":414,"ordre":1},{"id":2395600,"corps":"DA","value":"1.2000000000","dossart":414,"ordre":2},{"id":2395601,"corps":"Art.","value":"5.9660000000","dossart":414,"ordre":3},{"id":2395602,"corps":"Exé.","value":"5.8660000000","dossart":414,"ordre":4},{"id":2395603,"corps":"Pén.","value":"0E-10","dossart":414,"ordre":5},{"id":2395604,"corps":"DIFFICULTE 2023","value":"4.4000000000","dossart":414}]}]},{"id":726347,"labelApp":"Ruban","codeApp":"017","value":"17.6990000000","dossart":414,"rank":2,"passageMarks":[{"id":667266,"passage":1,"value":"17.6990000000","dossart":414,"corpsMarks":[{"id":2395605,"corps":"DB","value":"3.1000000000","dossart":414,"ordre":1},{"id":2395606,"corps":"DA","value":"2.7000000000","dossart":414,"ordre":2},{"id":2395607,"corps":"Art.","value":"5.2660000000","dossart":414,"ordre":3},{"id":2395608,"corps":"Exé.","value":"6.6330000000","dossart":414,"ordre":4},{"id":2395609,"corps":"Pén.","value":"0E-10","dossart":414,"ordre":5},{"id":2395610,"corps":"DIFFICULTE 2023","value":"5.8000000000","dossart":414}]}]}]}},{"markRank":3,"id":2630844,"type":"IND","lastname":"DEVILLE","firstname":"Juliette","licence":"93006.056.19999","idClub":1947,"club":"ASSOCIATION INTERCOMMUNALE SPORTIVE ET ARTISTIQUE GR Côte d\'Azur","city":"CARROS","dossart":386,"nationality":"FRA","mark":{"id":206940,"value":"32.3990000000","rank":3,"dossart":386,"entityType":"IND","appMarks":[{"id":726350,"labelApp":"Massues","codeApp":"015","value":"18.1000000000","dossart":386,"rank":2,"passageMarks":[{"id":667269,"passage":1,"value":"18.1000000000","dossart":386,"corpsMarks":[{"id":2395623,"corps":"DB","value":"3.2000000000","dossart":386,"ordre":1},{"id":2395624,"corps":"DA","value":"1.9000000000","dossart":386,"ordre":2},{"id":2395625,"corps":"Art.","value":"7.5000000000","dossart":386,"ordre":3},{"id":2395626,"corps":"Exé.","value":"5.5000000000","dossart":386,"ordre":4},{"id":2395627,"corps":"Pén.","value":"0E-10","dossart":386,"ordre":5},{"id":2395628,"corps":"DIFFICULTE 2023","value":"5.1000000000","dossart":386}]}]},{"id":726351,"labelApp":"Ruban","codeApp":"017","value":"14.2990000000","dossart":386,"rank":3,"passageMarks":[{"id":667270,"passage":1,"value":"14.2990000000","dossart":386,"corpsMarks":[{"id":2395629,"corps":"DB","value":"2.6000000000","dossart":386,"ordre":1},{"id":2395630,"corps":"DA","value":"1.6000000000","dossart":386,"ordre":2},{"id":2395631,"corps":"Art.","value":"4.4660000000","dossart":386,"ordre":3},{"id":2395632,"corps":"Exé.","value":"5.6330000000","dossart":386,"ordre":4},{"id":2395633,"corps":"Pén.","value":"0E-10","dossart":386,"ordre":5},{"id":2395634,"corps":"DIFFICULTE 2023","value":"4.2000000000","dossart":386}]}]}]}}]}'
#print(json.dumps(get_results_category(json.loads(CATEGORY))))

# test get_results_event
#print(json.dumps(get_results_event(get_results_event_json(13579))))

print(json.dumps(get_vertical_ranking(EVENTS)))
#get_vertical_ranking(EVENTS)
