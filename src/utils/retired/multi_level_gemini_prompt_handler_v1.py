from utils.llm_prompt_handlers.gemini_prompt_handler import gemini_prompt_handler

def multi_level_gemini_prompt_handler_v1(paragraph, foo):
    # First-level prediction prompt template
    level_1_template = """
        Identify the discourse relation in the following paragraph by selecting one of the four options: temporal, contingency, comparison, or expansion.

        {paragraph}

        Definitions:
        - Contingency.
        - Temporal.
        - Comparison.
        - Expansion.

        **Important:** Return only the chosen discourse relation as your response, without any explanation.
        """

    # Get first-level prediction
    level_1_prediction = gemini_prompt_handler(paragraph, level_1_template).lower().strip()
    print(f"Level 1 Prediction: {level_1_prediction}")

    # Define Level-2 prompt templates based on the Level-1 prediction
    if level_1_prediction == "temporal":
        level_2_template = """
        Given that the paragraph exhibits a Level-1 PDTB relation of Temporal, identify the specific Level-2 relation from the options provided:

        - Synchronous.
        - Asynchronous.

        Paragraph: {paragraph}

        **Important:** Based on the paragraph, please return only one word, without any additional explanation: Synchronous or Asynchronous.
        """
    elif level_1_prediction == "contingency":
        level_2_template = """
        Given that the paragraph exhibits a Level-1 PDTB relation of Contingency, identify the specific Level-2 relation from the options provided:

        - Cause.
        - Cause+Belief.
        - Cause+SpeechAct.
        - Condition.
        - Condition+SpeechAct.
        - Negative-Condition.
        - Negative-Condition+SpeechAct.
        - Purpose.

        Paragraph: {paragraph}

        **Important:** Based on the paragraph, please return only one word or phrase without any additional explanation: Cause, Cause+Belief, Cause+SpeechAct, Condition, Condition+SpeechAct, Negative-Condition, Negative-Condition+SpeechAct, or Purpose.
        """
    elif level_1_prediction == "comparison":
        level_2_template = """
        Given that the paragraph exhibits a Level-1 PDTB relation of Comparison, identify the specific Level-2 relation from the options provided:

        - Concession.
        - Concession+SpeechAct.
        - Contrast.
        - Similarity.

        Paragraph: {paragraph}

        **Important:** Based on the paragraph, please return only one word without any additional explanation: Concession, Concession+SpeechAct, Contrast, or Similarity.

        """
    elif level_1_prediction == "expansion":
        level_2_template = """
        Given that the paragraph exhibits a Level-1 PDTB relation of Expansion, identify the specific Level-2 relation from the options provided:

        - Conjunction.
        - Disjunction.
        - Equivalence.
        - Exception.
        - Instantiation.
        - Level-of-Detail.
        - Manner.
        - Substitution.

        Paragraph: {paragraph}

        **Important:** Based on the paragraph, please return only one word or phrase without any additional explanation: Conjunction, Disjunction, Equivalence, Exception, Instantiation, Level-of-Detail, Manner, or Substitution.
                """
    else:
        print("Unrecognized discourse relation in level 1 prediction.")
        return None

    # Get second-level prediction based on the identified relation
    level_2_prediction = gemini_prompt_handler(paragraph, level_2_template).strip()
    print(f"Level 2 Prediction: {level_2_prediction}")

    return level_2_prediction