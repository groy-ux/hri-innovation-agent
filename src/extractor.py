def extract_dimensions(text: str) -> dict:
    text_lower = text.lower()

    # problem + outcome
    if "stress" in text_lower:
        problem = "passenger stress"
        outcome = "improve comfort"
    elif "emotion" in text_lower or "emotions" in text_lower:
        problem = "passenger emotional discomfort"
        outcome = "improve comfort"
    elif "drowsiness" in text_lower or "fatigue" in text_lower:
        problem = "driver fatigue"
        outcome = "improve safety"
    elif "discomfort" in text_lower:
        problem = "seat discomfort"
        outcome = "improve comfort"
    else:
        problem = "general mobility issue"
        outcome = "improve experience"

    # stakeholder + context
    if "child seat" in text_lower or "seat" in text_lower:
        stakeholder = "passenger"
        context = "vehicle seat"
    elif "driver" in text_lower:
        stakeholder = "driver"
        context = "driving"
    else:
        stakeholder = "passenger"
        context = "vehicle cabin"

    # value type
    if "safety" in text_lower or "drowsiness" in text_lower or "fatigue" in text_lower:
        value_type = "safety"
    else:
        value_type = "comfort"

    return {
        "core_mechanism": text[:40],
        "problem_opportunity": problem,
        "intended_outcome": outcome,
        "stakeholder": stakeholder,
        "context": context,
        "value_type": value_type
    }