def get_vertical_ranking(events_results):
    """
    Get the merged ranking between all the provided event results.
    """
    if len(events_results) == 1:
        return events_results[0]

    vertical_ranking = dict()

    for event in events_results:
        vertical_ranking = merge_events(vertical_ranking, event)

    return vertical_ranking

def merge_events(event1, event2):
    """
    Merge the rankings of two events.
    """
    merge = dict()

    merge['event_id'] = '-'.join([str(event1['event_id']), str(event2['event_id'])]) if event1.get('event_id') else event2['event_id']
    merge['event_label'] = f"Classement vertical events [{','.join([str(event1['event_id']), str(event2['event_id'])]) if event1.get('event_id') else event2['event_id']}]"

    merge['categories'] = dict()

    categories = set(event1.get('categories', {}).keys()).union(set(event2.get('categories', {}).keys()))

    for category in categories:
        category1 = event1.get('categories', {}).get(category, [])
        category2 = event2.get('categories', {}).get(category, [])
        merge['categories'][category] = {}
        merge['categories'][category]['general'] = merge_categories(event1, category1, event2, category2)

    return merge

def merge_categories(event1, category1, event2, category2):
    """
    Merge two corresponding categories of two events.
    """
    # if both categories from the two events are empty (should not happen)
    if not category1 and not category2:
        return []
    # if there are gymnasts in this category only in event 2
    if not category1:
        return category2['general']
    # if there are gymnasts in this category only in event 1
    if not category2:
        return category1['general']

    category = []

    i_cat1 = 0
    i_cat2 = 0

    # iterate over the two categories in parallel
    while i_cat1 < len(category1['general']) and i_cat2 < len(category2['general']):
        gymnasts1 = category1['general'][i_cat1]
        for gymnast in gymnasts1:
            gymnast['event_id'] = event1['event_id']
            gymnast['event_label'] = event1['event_label']
        gymnasts2 = category2['general'][i_cat2]
        for gymnast in gymnasts2:
            gymnast['event_id'] = event2['event_id']
            gymnast['event_label'] = event2['event_label']

        comparison = compare_gymnasts_lists(gymnasts1, gymnasts2)
        # if the scores of both lists of ex aequo gymnasts are the same
        if comparison == 0:
            # concatenate the lists of gymnasts and add them to the category list
            gymnasts = gymnasts1 + gymnasts2
            category.append(gymnasts)
            # increase both iterators
            i_cat1+=1
            i_cat2+=1
        elif comparison < 0:
            # if ex aequo gymnasts from event 1 have a best score than ex aequo gymnasts from event 2
            category.append(gymnasts1)
            i_cat1+=1
        elif comparison > 0:
            # if ex aequo gymnasts from event 2 have a best score than ex aequo gymnasts from event 1
            category.append(gymnasts2)
            i_cat2+=1
    # while there are remaining gymnasts in category 1
    # there will not be remaining gymnasts both in category 1 and 2 at the same time
    while i_cat1 < len(category1['general']):
        category.append(category1['general'][i_cat1])
        i_cat1+=1
    # while there are remaining gymnasts in category 2
    while i_cat2 < len(category2['general']):
        category.append(category2['general'][i_cat2])
        i_cat2+=1

    return category

def compare_gymnasts_lists(gymnasts1, gymnasts2):
    """
    Compare the scores of the ex aequo gymnasts from event 1 with the score of the ex aequo gymnasts from event 2.
    """
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
