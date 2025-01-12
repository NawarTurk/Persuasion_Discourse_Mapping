
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
    1: {"name": "synchronous", "description": "Temporal.Synchronous This tag is used when there is some degree of temporal overlap between the events described by the arguments. All forms of overlap are included."},
    2: {"name": "asynchronous", "description": "Temporal.Asynchronous This tag is used when one event is described as preceding the other."},
    3: {"name": "cause", "description": "Contingency.Cause This tag is used when the situations described in Arg1 and Arg2 are causally influenced but are not in a conditional relation."},
    4: {"name": "cause+belief", "description": "Contingency.Cause+Belief This tag is used when evidence is provided to cause the hearer to believe a claim. The belief is implicit."},
    5: {"name": "cause+SpeechAct", "description": "Contingency.Cause+SpeechAct This tag is used when a reason is provided for the speaker uttering a speech act. The speech act is implicit."},
    6: {"name": "condition", "description": "Contingency.Condition This tag is used when one argument presents a situation as unrealized (the antecedent), which (when realized) would lead to the situation described by the other arg (the consequent). There are distinct senses for interpreting the arguments in terms of their semantics or the speech acts they convey. The default is their semantics."},
    7: {"name": "condition+SpeechAct", "description": "Contingency.Condition+SpeechAct This tag is used when the consequent is an implicit speech act. So far, all cases of Condition+SA are Arg2-as-cond, so Arg1 is the implicit SA."},
    8: {"name": "negative-condition", "description": "Contingency.Negative-condition This tag is used when one argument (the antecedent) describes a situation presented as unrealized, which if it doesn’t occur, would lead to the situation described by the other argument (the consequent). There are distinct senses for interpreting the arguments in terms of semantics or speech acts, with the default being semantics."},
    9: {"name": "negative-condition+SpeechAct", "description": "Contingency.Negative-condition+SpeechAct This tag is used when the consequent is an implicit speech act. While none of the tokens in the PDTB-3 have been annotated with this sense, it is included in the hierarchy for completeness."},
    10: {"name": "purpose", "description": "Contingency.Purpose This tag is used when one argument presents an action that an AGENT un- dertakes with the purpose of the GOAL conveyed by the other argument being achieved. Usually (but not always), the agent undertaking the action is the same agent aiming to achieve the goal."},
    11: {"name": "concession", "description": "Comparison.Concession This tag is used when an expected causal relation is cancelled or denied by the situation described in one of the arguments."},
    12: {"name": "concession+SpeechAct", "description": "Comparison.Concession+SpeechAct This tag is used when the speech act (SA) associated with one argument is cancelled or denied by the other argument or its SA. The only sub-type for which tokens have been identified is Comparison.Concession+SpeechAct.Arg2-as-denier+SA, where it is the SA associated with Arg1 that is cancelled or denied by Arg2 or its associated SA. "},
    13: {"name": "contrast", "description": "Comparison.Contrast As noted, Contrast is used when at least two differences between Arg1 and Arg2 are highlighted."},
    14: {"name": "similarity", "description": "Comparison.Similarity This tag is used when one or more similarities between Arg1 and Arg2 are highlighted with respect to what each argument predicates as a whole or to some entities it mentions."},
    15: {"name": "conjunction", "description": "Expansion.Conjunction The tag Conjunction is used when both arguments bear the same relation to some other situation evoked in the discourse. It indicates that the two arguments make the same contribution with respect to that situation, or contribute to it together. It differs from most other relations in that the arguments don’t directly relate to each other, but to this other situation."},
    16: {"name": "disjunction", "description": "Expansion.Disjunction The tag Expansion.Disjunction is used when the two arguments are pre- sented as alternatives, with either one or both holding. As with Conjunction, Disjunction is used when both its arguments bear the same relation to some other situation evoked in the discourse, making a similar contribution with respect to that situation. While the arguments also relate to each other as alternatives (with one or both holding), they also both relate in the same way to this other situation."},
    17: {"name": "equivalence", "description": "Expansion.Equivalence This tag is used when both arguments are taken to describe the same situa- tion, but from different perspectives."},
    18: {"name": "exception", "description": "Expansion.Exception This tag is used when one argument evokes a set of circumstances in which the described situation holds, and the other argument indicates one or more instances where it doesn’t."},
    19: {"name": "instantiation", "description": "Expansion.Instantiation This tag is used when one argument describes a situation as holding in a set of circumstances, while the other argument describes one or more of those circumstances."},
    20: {"name": "level-of-detail", "description": "Expansion.Level-of-Detail This tag is used when both arguments describe the same situation, but in less or more detail."},
    21: {"name": "manner", "description": "Expansion.Manner This tag is used when the situation described by one argument presents the manner in which the situation described by other argument has happened or been done. Manner answers “how” questions such as “How were the children playing?”. While Manner may be the only relation that holds between two arguments, it is often the case that another sense (Purpose, Result or Condition) is taken to hold as well."},
    22: {"name": "substitution", "description": "Expansion.Substitution This tag is used when arguments are presented as exclusive alternatives, with one being ruled out."}
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
        if technique.lower() == PT_name.lower():
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
    
def get_level2_DR_id_by_name(DR_name):
    for id, relation in DR_relations_level2.items():
        if relation['name'].lower() == DR_name.lower():
            return id
        
    print(f"Discourse relation with name {DR_name} not found.")
    return None