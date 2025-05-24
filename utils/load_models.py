import pickle as pkl
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def load_models():
    root_dir = Path(__file__).parents[1]
    
    with open(root_dir / 'models/kmeans_model.pkl', 'rb') as f:
        cluster: KMeans = pkl.load(f)
        
    with open(root_dir / 'models/vectorizer.pkl', 'rb') as f:
        vectorizer: TfidfVectorizer = pkl.load(f)
        
    return cluster, vectorizer