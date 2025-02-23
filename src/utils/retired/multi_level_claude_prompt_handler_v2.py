from utils.llm_prompt_handlers.claude_prompt_handler import claude_prompt_handler


def multi_level_claude_prompt_handler_v2(paragraph, foo):
    # First-level prediction prompt template
    level_1_template = """
        Identify the discourse relation in the following paragraph by selecting one of the four options: temporal, contingency, comparison, or expansion.

        {paragraph}

        Definitions:
        - Contingency: One argument provides the reason or justification for the other.
        - Temporal: Arguments are related in time.
        - Comparison: Arguments highlight differences or similarities.
        - Expansion: Extends the discourse or advances the narrative.

        **Important:** Return only the chosen discourse relation as your response, without any explanation.
        """

    # Get first-level prediction
    level_1_prediction = claude_prompt_handler(paragraph, level_1_template).lower().strip()
    print(f"Level 1 Prediction: {level_1_prediction}")

    # Define Level-2 prompt templates based on the Level-1 prediction
    if level_1_prediction == "temporal":
        level_2_template = """
        Given that the paragraph exhibits a Level-1 PDTB relation of Temporal, identify the specific Level-2 relation from the options provided:

        - Synchronous: This tag is used when there is some degree of temporal overlap between the events described by the arguments. All forms of overlap are included.
        - Asynchronous: This tag is used when one event is described as preceding the other.

        Paragraph: {paragraph}

        **Important:** Based on the paragraph, please return only one word, without any additional explanation: Synchronous or Asynchronous.
        """
    elif level_1_prediction == "contingency":
        level_2_template = """
        Given that the paragraph exhibits a Level-1 PDTB relation of Contingency, identify the specific Level-2 relation from the options provided:

        - Cause: This tag is used when the situations described in Arg1 and Arg2 are causally influenced but are not in a conditional relation.
        - Cause+Belief: This tag is used when evidence is provided to cause the hearer to believe a claim. The belief is implicit.
        - Cause+SpeechAct: This tag is used when a reason is provided for the speaker uttering a speech act. The speech act is implicit.
        - Condition: This tag is used when one argument presents a situation as unrealized (the antecedent), which (when realized) would lead to the situation described by the other arg (the consequent). There are distinct senses for interpreting the arguments in terms of their semantics or the speech acts they convey. The default is their semantics.
        - Condition+SpeechAct: This tag is used when the consequent is an implicit speech act. So far, all cases of Condition+SA are Arg2-as-cond, so Arg1 is the implicit SA.
        - Negative-Condition: This tag is used when one argument (the antecedent) describes a situation presented as unrealized, which if it doesn’t occur, would lead to the situation described by the other argument (the consequent). There are distinct senses for interpreting the arguments in terms of semantics or speech acts, with the default being semantics.
        - Negative-Condition+SpeechAct: This tag is used when the consequent is an implicit speech act. While none of the tokens in the PDTB-3 have been annotated with this sense, it is included in the hierarchy for completeness.
        - Purpose: This tag is used when one argument presents an action that an AGENT undertakes with the purpose of the GOAL conveyed by the other argument being achieved. Usually (but not always), the agent undertaking the action is the same agent aiming to achieve the goal.

        Paragraph: {paragraph}

        **Important:** Based on the paragraph, please return only one word or phrase without any additional explanation: Cause, Cause+Belief, Cause+SpeechAct, Condition, Condition+SpeechAct, Negative-Condition, Negative-Condition+SpeechAct, or Purpose.
        """
    elif level_1_prediction == "comparison":
        level_2_template = """
        Given that the paragraph exhibits a Level-1 PDTB relation of Comparison, identify the specific Level-2 relation from the options provided:

        - Concession: This tag is used when an expected causal relation is canceled or denied by the situation described in one of the arguments.
        - Concession+SpeechAct: This tag is used when the speech act (SA) associated with one argument is canceled or denied by the other argument or its SA. The only sub-type for which tokens have been identified is Comparison.Concession+SpeechAct.Arg2-as-denier+SA, where it is the SA associated with Arg1 that is canceled or denied by Arg2 or its associated SA.
        - Contrast: This tag is used when at least two differences between Arg1 and Arg2 are highlighted.
        - Similarity: This tag is used when one or more similarities between Arg1 and Arg2 are highlighted with respect to what each argument predicates as a whole or to some entities it mentions.

        Paragraph: {paragraph}

        **Important:** Based on the paragraph, please return only one word without any additional explanation: Concession, Concession+SpeechAct, Contrast, or Similarity.

        """
    elif level_1_prediction == "expansion":
        level_2_template = """
        Given that the paragraph exhibits a Level-1 PDTB relation of Expansion, identify the specific Level-2 relation from the options provided:

        - Conjunction: This tag is used when both arguments bear the same relation to some other situation evoked in the discourse. It indicates that the two arguments make the same contribution with respect to that situation, or contribute to it together. It differs from most other relations in that the arguments don’t directly relate to each other, but to this other situation.
        - Disjunction: This tag is used when the two arguments are presented as alternatives, with either one or both holding. Disjunction is used when both arguments bear the same relation to some other situation evoked in the discourse, making a similar contribution with respect to that situation. While the arguments relate to each other as alternatives (with one or both holding), they also both relate in the same way to this other situation.
        - Equivalence: This tag is used when both arguments are taken to describe the same situation, but from different perspectives.
        - Exception: This tag is used when one argument evokes a set of circumstances in which the described situation holds, and the other argument indicates one or more instances where it doesn’t.
        - Instantiation: This tag is used when one argument describes a situation as holding in a set of circumstances, while the other argument describes one or more of those circumstances.
        - Level-of-Detail: This tag is used when both arguments describe the same situation, but in less or more detail.
        - Manner: This tag is used when the situation described by one argument presents the manner in which the situation described by the other argument has happened or been done. Manner answers “how” questions such as “How were the children playing?”. While Manner may be the primary relation, another sense (e.g., Purpose, Result, or Condition) may also hold.
        - Substitution: This tag is used when arguments are presented as exclusive alternatives, with one being ruled out.

        Paragraph: {paragraph}

        **Important:** Based on the paragraph, please return only one word or phrase without any additional explanation: Conjunction, Disjunction, Equivalence, Exception, Instantiation, Level-of-Detail, Manner, or Substitution.
                """
    else:
        print("Unrecognized discourse relation in level 1 prediction.")
        return None

    # Get second-level prediction based on the identified relation
    level_2_prediction = claude_prompt_handler(paragraph, level_2_template).strip()
    print(f"Level 2 Prediction: {level_2_prediction}")

    return level_2_prediction