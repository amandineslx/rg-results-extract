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
        category1 = event1.get('categories', {}).get(category, [])
        category2 = event2.get('categories', {}).get(category, [])
        merge['categories'][category] = merge_categories(event1, category1, event2, category2)

    return merge

def merge_categories(event1, category1, event2, category2):
    if not category1 and not category2:
        return []
    if not category1:
        return category2
    if not category2:
        return category1

    category = []

    i_cat1 = 0
    i_cat2 = 0

    while i_cat1 < len(category1) and i_cat2 < len(category2):
        gymnasts1 = category1[i_cat1]
        for gymnast in gymnasts1:
            gymnast['event_id'] = event1['event_id']
            gymnast['event_label'] = event1['event_label']
        gymnasts2 = category2[i_cat2]
        for gymnast in gymnasts2:
            gymnast['event_id'] = event2['event_id']
            gymnast['event_label'] = event2['event_label']

        comparison = compare_gymnasts_lists(gymnasts1, gymnasts2)
        if comparison == 0:
            gymnasts = gymnasts1 + gymnasts2
            category.append(gymnasts)
            i_cat1+=1
            i_cat2+=1
        elif comparison < 0:
            category.append(gymnasts1)
            i_cat1+=1
        elif comparison > 0:
            category.append(gymnasts2)
            i_cat2+=1
    while i_cat1 < len(category1):
        category.append(category1[i_cat1])
        i_cat1+=1
    while i_cat2 < len(category2):
        category.append(category2[i_cat2])
        i_cat2+=1

    return category

def compare_gymnasts_lists(gymnasts1, gymnasts2):
    # TODO there is an issue with sollies results
    gymnast1 = gymnasts1[0] if gymnasts1 else None
    gymnast2 = gymnasts2[0] if gymnasts2 else None
    if not gymnast1 and not gymnast2:
        raise Exception("Both gymnasts to be compared are None")
    if not gymnast1:
        return 1
    if not gymnast2:
        return -1

    gym1_total = gymnast1['total']
    gym2_total = gymnast2['total']

    if gym1_total > gym2_total:
        return -1
    elif gym1_total < gym2_total:
        return 1
    else:
        return 0
