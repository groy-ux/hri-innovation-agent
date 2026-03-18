import pandas as pd

def load_ideas():
    df = pd.read_csv("data/raw/ideas.csv")
    return df