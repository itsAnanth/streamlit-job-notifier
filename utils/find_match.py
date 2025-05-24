import pandas
from pathlib import Path
from .load_models import load_models

def find_match(user_skills: str) -> pandas.DataFrame:
    if user_skills == None or len(user_skills) == 0:
        raise ValueError("user skills must be a valid string seperated by commas (python, js) etc")

    root_dir = Path(__file__).parents[1]

    cluster, vectorizer = load_models()
        
    clustered_jobs_df = pandas.read_csv(root_dir / "data/clustered_jobs.csv", index_col=None)


    X = vectorizer.transform([user_skills])

    best_cluster = cluster.predict(X)
    best_cluster = best_cluster[0]

    return clustered_jobs_df[clustered_jobs_df['Cluster'] == best_cluster]