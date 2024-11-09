
PT_techniques = {
1: "Appeal_to_Authority",
2: "Appeal_to_Popularity",
3: "Appeal_to_Values",
4: "Appeal_to_Fear-Prejudice",
5: "Flag_Waving",
6: "Causal_Oversimplification",
7: "False_Dilemma-No_Choice",
8: "Consequential_Oversimplification",
9: "Straw_Man",
10: "Red_Herring",
11: "Whataboutism",
12: "Slogans",
13: "Appeal_to_Time",
14: "Conversation_Killer",
15: "Loaded_Language",
16: "Repetition",
17: "Exaggeration-Minimisation",
18: "Obfuscation-Vagueness-Confusion",
19: "Name_Calling-Labeling",
20: "Doubt",
21: "Guilt_by_Association",
22: "Appeal_to_Hypocrisy",
23: "Questioning_the_Reputation"
}

# Dictionary for Level-2 discourse relations with unique IDs and placeholder descriptions

DR_relations_level2 = {
    1: {"name": "synchronous", "description": "Placeholder for synchronous description"},
    2: {"name": "asynchronous", "description": "Placeholder for asynchronous description"},
    3: {"name": "cause", "description": "Placeholder for cause description"},
    4: {"name": "cause+belief", "description": "Placeholder for cause+belief description"},
    5: {"name": "cause+SpeechAct", "description": "Placeholder for cause+SpeechAct description"},
    6: {"name": "condition", "description": "Placeholder for condition description"},
    7: {"name": "condition+SpeechAct", "description": "Placeholder for condition+SpeechAct description"},
    8: {"name": "negative-condition", "description": "Placeholder for negative-condition description"},
    9: {"name": "negative-condition+SpeechAct", "description": "Placeholder for negative-condition+SpeechAct description"},
    10: {"name": "purpose", "description": "Placeholder for purpose description"},
    11: {"name": "concession", "description": "Placeholder for concession description"},
    12: {"name": "concession+SpeechAct", "description": "Placeholder for concession+SpeechAct description"},
    13: {"name": "contrast", "description": "Placeholder for contrast description"},
    14: {"name": "similarity", "description": "Placeholder for similarity description"},
    15: {"name": "conjunction", "description": "Placeholder for conjunction description"},
    16: {"name": "disjunction", "description": "Placeholder for disjunction description"},
    17: {"name": "equivalence", "description": "Placeholder for equivalence description"},
    18: {"name": "exception", "description": "Placeholder for exception description"},
    19: {"name": "instantiation", "description": "Placeholder for instantiation description"},
    20: {"name": "level-of-detail", "description": "Placeholder for level-of-detail description"},
    21: {"name": "manner", "description": "Placeholder for manner description"},
    22: {"name": "substitution", "description": "Placeholder for substitution description"}
}


def get_PT_technique_by_id(PT_id):
    technique = PT_techniques.get(PT_id, None)
    if technique:
        return technique
    else:
        print(f"Persuation technique with ID {PT_id} not found.")
        return None

def get_PT_id_by_name (PT_name):
    for id, technique in PT_techniques.items():
        if technique == PT_name:
            return id
        
    print(f"Discourse relation with name {PT_name} not found.")
    return None

def get_DR_relation_by_id(DR_id):
    relation = DR_relations_level2.get(DR_id, None)
    if relation:
        return relation['name']
    else:
        print(f"Discourse relation with ID {DR_id} not found.")
        return None
    
def get_DR_id_by_name(DR_name):
    for id, relation in DR_relations_level2.items():
        if relation['name'] == DR_name:
            return id
        
    print(f"Discourse relation with name {DR_name} not found.")
    return None