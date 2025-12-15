from model import Event, Category

def merge_event_list(events):
    """
    Get the merged ranking between all the provided event results.
    """
    if len(events) == 1:
        return events[0]

    merged_event = events[0]

    for event in events[1:]:
        merged_event = merge_events(merged_event, event)

    return merged_event

def merge_events(event1, event2):
    """
    Merge the rankings of two events.
    """
    merged_event = Event(
        '-'.join([str(event1.id), str(event2.id)]) if event1.id else event2.id,
        f"Classement vertical events [{','.join([str(event1.id), str(event2.id)]) if event1.id else event2.id}]",
        ""
    )

    category_names = set(event1.categories.keys()).union(set(event2.categories.keys()))

    for category_name in category_names:
        category1 = event1.categories.get(category_name, None)
        category2 = event2.categories.get(category_name, None)

        if category1:
            for rank in category1.general_ranking:
                for entity in rank:
                    entity.event_label = event1.label
        if category2:
            for rank in category2.general_ranking:
                for entity in rank:
                    entity.event_label = event2.label

        category = merge_categories(event1, category1, event2, category2)
        merged_event.add_category(merge_categories(event1, category1, event2, category2))

    return merged_event

def merge_categories(event1, category1, event2, category2):
    """
    Merge two corresponding categories of two events.
    """
    # if both categories from the two events are empty (should not happen)
    if not category1 and not category2:
        return None
    # if there are gymnasts in this category only in event 2
    if not category1:
        return category2
    # if there are gymnasts in this category only in event 1
    if not category2:
        return category1

    merged_category = Category(category1.label)

    i_cat1 = 0
    i_cat2 = 0

    # iterate over the two categories in parallel
    while i_cat1 < len(category1.general_ranking) and i_cat2 < len(category2.general_ranking):
        entities1 = category1.general_ranking[i_cat1]
        entities2 = category2.general_ranking[i_cat2]

        comparison = compare_entities_lists(entities1, entities2)
        # if the scores of both lists of ex aequo entities are the same
        if comparison == 0:
            # concatenate the lists of entities and add them to the category list
            entities = entities1 + entities2
            merged_category.general_ranking.append(entities)
            # increase both iterators
            i_cat1+=1
            i_cat2+=1
        elif comparison < 0:
            # if ex aequo entities from event 1 have a best score than ex aequo entities from event 2
            merged_category.general_ranking.append(entities1)
            i_cat1+=1
        elif comparison > 0:
            # if ex aequo entities from event 2 have a best score than ex aequo entities from event 1
            merged_category.general_ranking.append(entities2)
            i_cat2+=1
    # while there are remaining entities in category 1
    # there will not be remaining entities both in category 1 and 2 at the same time
    while i_cat1 < len(category1.general_ranking):
        merged_category.general_ranking.append(category1.general_ranking[i_cat1])
        i_cat1+=1
    # while there are remaining entities in category 2
    while i_cat2 < len(category2.general_ranking):
        merged_category.general_ranking.append(category2.general_ranking[i_cat2])
        i_cat2+=1

    return merged_category

def compare_entities_lists(entities1, entities2):
    """
    Compare the scores of the ex aequo entities from event 1 with the score of the ex aequo entities from event 2.
    """
    entity1 = entities1[0] if entities1 else None
    entity2 = entities2[0] if entities2 else None
    if not entity1 and not entity2:
        raise Exception("Both entities to be compared are None")
    if not entity1:
        return 1
    if not entity2:
        return -1

    gym1_total = entity1.total
    gym2_total = entity2.total

    if gym1_total > gym2_total:
        return -1
    elif gym1_total < gym2_total:
        return 1
    else:
        return 0
