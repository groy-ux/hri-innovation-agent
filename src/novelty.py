def compute_novelty_from_similarity(similarity_score: float) -> dict:
    novelty_score = round(1 - similarity_score, 3)

    if novelty_score < 0.3:
        novelty_band = "low novelty"
    elif novelty_score < 0.6:
        novelty_band = "medium novelty"
    else:
        novelty_band = "high novelty"

    return {
        "novelty_score": novelty_score,
        "novelty_band": novelty_band
    }