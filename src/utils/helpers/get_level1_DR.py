def get_level1_DR(level2_relation):

    # Define a dictionary that maps level-2 relations to their level-1 equivalents
    level2_to_level1 = {
        # Temporal
        "synchronous": "temporal",
        "asynchronous": "temporal",

        # Contingency
        "cause": "contingency",
        "cause+belief": "contingency",
        "cause+speechact": "contingency",
        "condition": "contingency",
        "condition+speechact": "contingency",
        "negative-condition": "contingency",
        "negative-condition+speechact": "contingency",
        "purpose": "contingency",

        # Comparison
        "concession": "comparison",
        "concession+speechact": "comparison",
        "contrast": "comparison",
        "similarity": "comparison",

        # Expansion
        "conjunction": "expansion",
        "disjunction": "expansion",
        "equivalence": "expansion",
        "exception": "expansion",
        "instantiation": "expansion",
        "level-of-detail": "expansion",
        "manner": "expansion",
        "substitution": "expansion"
    }

    # Return the level-1 relation, or None if the level-2 relation is not found
    return level2_to_level1.get(level2_relation.lower(), None)