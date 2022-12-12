import collections

def get_vertical_ranking(events_results):
    if len(events_results) == 1:
        return events_results[0]

    vertical_ranking = dict()

    for event in events_results:
        vertical_ranking = merge_events(vertical_ranking, event)

    return vertical_ranking

def merge_events(event1, event2):
    merge = dict()

    merge['event_id'] = '-'.join([str(event1['event_id']), str(event2['event_id'])]) if event1.get('event_id') else event2['event_id']
    merge['event_label'] = f"Classement vertical events [{','.join([str(event1['event_id']), str(event2['event_id'])]) if event1.get('event_id') else event2['event_id']}]"

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
        gymnasts1 = category1.get(str(i_cat1), None)
        if gymnasts1:
            # TODO map method in array
            for gymnast in gymnasts1:
                gymnast['event_id'] = event1['event_id']
                gymnast['event_label'] = event1['event_label']
        gymnasts2 = category2.get(str(i_cat2), None)
        if gymnasts2:
            for gymnast in gymnasts2:
                gymnast['event_id'] = event2['event_id']
                gymnast['event_label'] = event2['event_label']

        comparison = compare_gymnasts(gymnasts1, gymnasts2)
        if comparison == 0:
            i_cat1+=1
            i_cat2+=1
        elif comparison < 0:
            category[str(i_cat)] = gymnasts1
            i_cat1+=1
            i_cat+=1
        else:
            category[str(i_cat)] = gymnasts2
            i_cat2+=1
            i_cat+=1

    return category

def compare_gymnasts(gymnasts1, gymnasts2):
    # TODO there is an issue with sollies results
    gymnast1 = gymnasts1[0] if gymnasts1 else None
    gymnast2 = gymnasts2[0] if gymnasts2 else None
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
