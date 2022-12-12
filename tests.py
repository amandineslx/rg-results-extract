import json

from extraction import get_results_passage, get_results_gymnast, get_results_category, get_results_event
from merging import merge_categories

def read_json_from_file(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)

def write_json_to_file(json_content, file_name):
    with open(file_name, 'w') as f:
        f.write(json.dumps(json_content))

# test get_results_event_json
#print(get_results_event_json(13579))

# test get_passage
#PASSAGE = read_json_from_file('passage.json')
#print(get_results_passage(PASSAGE))

# test get_results_gymnast
#GYMNAST = read_json_from_file('gymnast.json')
#print(get_results_gymnast(GYMNAST))

# test get_results_category
#CATEGORY = read_json_from_file('category.json')
#print(get_results_category(CATEGORY))

# test get_results_event
#print(json.dumps(get_results_event(get_results_event_json(13579))))

#print(json.dumps(get_vertical_ranking(EVENTS)))
#get_vertical_ranking(EVENTS)

#print("13579")
#event1 = get_results_event("13579")
#write_json_to_file(event1, 'event1.json')
#print("13580")
#event2 = get_results_event("13580")
#write_json_to_file(event2, 'event2.json')

event1 = {'event_id': '13579', 'event_label': '06'}
event2 = {'event_id': '13580', 'event_label': '13'}
category1 = read_json_from_file('category1.json')
category2 = read_json_from_file('category2.json')

print(json.dumps(merge_categories(event1, category1, event2, category2)))
