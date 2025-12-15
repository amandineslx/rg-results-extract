def is_regional_category(category_label):
    return _contains_any_label(category_label, ["régional", "fédérale r", "regional", "reg"])

def is_ignored_category(category_label):
    return _contains_any_label(category_label, ["nationale par equipe"])

def _contains_any_label(initial_label, labels):
    for label in labels:
        if label in initial_label.lower():
            return True
    return False

def format_mark(mark):
    """
    Format the mark to remove additional decimals.
    """
    return float(mark)
