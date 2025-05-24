import pickle as pkl
import pandas
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def find_match(user_skills: str) -> pandas.DataFrame:
    if user_skills == None or len(user_skills) == 0:
        raise ValueError("user skills must be a valid string seperated by commas (python, js) etc")

    root_dir = Path(__file__).parents[1]

    with open(root_dir / 'models/kmeans_model.pkl', 'rb') as f:
        cluster: KMeans = pkl.load(f)
        
    with open(root_dir / 'models/vectorizer.pkl', 'rb') as f:
        vectorizer: TfidfVectorizer = pkl.load(f)
        
    clustered_jobs_df = pandas.read_csv(root_dir / "data/clustered_jobs.csv", index_col=None)

    skills = "python, js"

    X = vectorizer.transform([skills])

    best_cluster = cluster.predict(X)[0]

    return clustered_jobs_df[clustered_jobs_df['Cluster'] == best_cluster]