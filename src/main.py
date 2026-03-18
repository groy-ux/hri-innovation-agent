import pandas as pd
from data_loader import load_ideas
from extractor import extract_dimensions
from similarity import compute_similarity_matrix, get_most_similar_pairs, find_top_k_similar
from novelty import compute_novelty_from_similarity


def build_combined_text(row: pd.Series) -> str:
    return (
        f"Title: {row['title']}\n"
        f"Core mechanism: {row['core_mechanism']}\n"
        f"Problem/opportunity: {row['problem_opportunity']}\n"
        f"Intended outcome: {row['intended_outcome']}\n"
        f"Stakeholder: {row['stakeholder']}\n"
        f"Context: {row['context']}\n"
        f"Value type: {row['value_type']}"
    )


def build_library():
    df = load_ideas()
    extracted_rows = []

    print("\n=== RUNNING EXTRACTION ON IDEA LIBRARY ===\n")

    for _, row in df.iterrows():
        extracted = extract_dimensions(row["raw_text"])

        combined_row = {
            "idea_id": row["idea_id"],
            "title": row["title"],
            "raw_text": row["raw_text"],
            **extracted,
        }
        extracted_rows.append(combined_row)

    structured_df = pd.DataFrame(extracted_rows)
    structured_df["combined_text"] = structured_df.apply(build_combined_text, axis=1)
    structured_df.to_csv("data/processed/ideas_structured.csv", index=False)

    return structured_df


def evaluate_new_idea(new_idea_text: str, structured_df: pd.DataFrame):
    print("\n=== EVALUATING NEW IDEA ===\n")
    print("New idea:")
    print(new_idea_text)

    new_idea_extracted = extract_dimensions(new_idea_text)
    print("\nExtracted dimensions:")
    print(new_idea_extracted)

    new_idea_row = {
        "title": "New Idea",
        **new_idea_extracted
    }

    new_idea_combined = build_combined_text(pd.Series(new_idea_row))

    top_matches = find_top_k_similar(
        new_idea_combined,
        structured_df["combined_text"].tolist(),
        structured_df["title"].tolist(),
        k=3
    )

    print("\nTop similar existing ideas:")
    for match in top_matches:
        novelty = compute_novelty_from_similarity(match["similarity_score"])
        print(f"Existing idea: {match['title']}")
        print(f"Similarity score: {match['similarity_score']}")
        print(f"Novelty score: {novelty['novelty_score']}")
        print(f"Novelty band: {novelty['novelty_band']}")
        print("-" * 50)


def main():
    structured_df = build_library()

    print("\n=== SIMILARITY MATRIX FOR IDEA LIBRARY ===\n")
    similarity_matrix = compute_similarity_matrix(structured_df["combined_text"])
    print(similarity_matrix)

    print("\n=== MOST SIMILAR IDEA FOR EACH IDEA ===\n")
    similarity_results = get_most_similar_pairs(
        similarity_matrix,
        structured_df["title"].tolist()
    )

    for result in similarity_results:
        novelty = compute_novelty_from_similarity(result["similarity_score"])
        print(f"Idea: {result['idea']}")
        print(f"Most similar idea: {result['most_similar_idea']}")
        print(f"Similarity score: {result['similarity_score']}")
        print(f"Novelty score: {novelty['novelty_score']}")
        print(f"Novelty band: {novelty['novelty_band']}")
        print("-" * 50)

    user_idea = input("\nEnter a new idea to evaluate:\n")
    evaluate_new_idea(user_idea, structured_df)


if __name__ == "__main__":
    main()