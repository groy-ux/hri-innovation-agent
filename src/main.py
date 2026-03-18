import pandas as pd
from data_loader import load_ideas
from extractor import extract_dimensions


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


def main():
    df = load_ideas()

    extracted_rows = []

    print("\n=== RUNNING EXTRACTION ===\n")

    for _, row in df.iterrows():
        extracted = extract_dimensions(row["raw_text"])

        combined_row = {
            "idea_id": row["idea_id"],
            "title": row["title"],
            "raw_text": row["raw_text"],
            **extracted,
        }
        extracted_rows.append(combined_row)

        print(f"\nIdea: {row['title']}")
        print(extracted)

    structured_df = pd.DataFrame(extracted_rows)
    structured_df["combined_text"] = structured_df.apply(build_combined_text, axis=1)

    print("\n=== STRUCTURED DATA ===\n")
    print(structured_df[[
        "idea_id",
        "title",
        "problem_opportunity",
        "intended_outcome",
        "stakeholder",
        "context",
        "combined_text"
    ]])

    structured_df.to_csv("data/processed/ideas_structured.csv", index=False)
    print("\nSaved structured data to data/processed/ideas_structured.csv")


if __name__ == "__main__":
    main()