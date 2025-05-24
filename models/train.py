from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pickle as pkl
from pathlib import Path
import pandas as pd

def find_optimal_clusters(X, max_k=10):
    """Compute silhouette scores for K=2 to max_k and plot."""
    scores = []
    K = range(2, max_k + 1)
    for k in K:
        model = KMeans(n_clusters=k, random_state=42)
        labels = model.fit_predict(X)
        score = silhouette_score(X, labels)
        print(f"Silhouette score for k={k}: {score:.4f}")
        scores.append(score)

    best_k = K[scores.index(max(scores))]
    print(f"Best number of clusters by silhouette score: {best_k}")
    return best_k

def generate_cluster_names(df, top_n=5):
    """Generate meaningful cluster names by extracting top TF-IDF keywords for each cluster."""
    cluster_names = {}
    for cluster in df['Cluster'].unique():
        cluster_skills = df[df['Cluster'] == cluster]['Skills']
        vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        X = vectorizer.fit_transform(cluster_skills)
        # Average TF-IDF scores per term across all docs in cluster
        mean_tfidf = X.mean(axis=0).A1
        terms = vectorizer.get_feature_names_out()
        # Top terms for cluster
        top_terms = [terms[i] for i in mean_tfidf.argsort()[::-1][:top_n]]
        cluster_names[cluster] = ", ".join(top_terms)
    return cluster_names


def train_clusters(df):
    root_dir = Path(__file__).parents[1]
    print("Starting Clustering pipeline...")


    # Step 2: Remove jobs with empty skills
    df = df[df['Skills'].str.strip() != ""].reset_index(drop=True)
    if df.empty:
        print("No jobs with skills found. Exiting.")
        return

    # Step 3: Vectorize skills using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['Skills'])

    # Save vectorizer for later use
    with open(f"{root_dir}/models/vectorizer.pkl", "wb") as f:
        pkl.dump(vectorizer, f)
    print("TF-IDF vectorizer saved as 'vectorizer.pkl'.")

    # Step 4: Find best number of clusters using silhouette score
    best_k = find_optimal_clusters(X, max_k=10)

    # Step 5: Train final KMeans model with best_k clusters
    model = KMeans(n_clusters=best_k, random_state=42)
    clusters = model.fit_predict(X)
    df['Cluster'] = clusters

    # Save model
    with open(f"{root_dir}/models/kmeans_model.pkl", "wb") as f:
        pkl.dump(model, f)
    print(f"KMeans model trained with k={best_k} and saved as 'kmeans_model.pkl'.")

    # Step 6: Evaluate and print final silhouette score
    final_score = silhouette_score(X, clusters)
    print(f"Final silhouette score for k={best_k}: {final_score:.4f}")

    # Step 7: Generate cluster names (top keywords)
    cluster_name_map = generate_cluster_names(df)
    df['Cluster_Name'] = df['Cluster'].map(cluster_name_map)

    print("Cluster names assigned:")
    for c, name in cluster_name_map.items():
        print(f"Cluster {c}: {name}")

    # Step 8: Save clustered jobs to CSV
    df.to_csv(f"{root_dir}/data/clustered_jobs.csv", index=False)
    print("Clustered job data saved to 'clustered_jobs.csv'.")
    
    

if __name__ == "__main__":
    root_dir = Path(__file__).parents[1]
    jobs = pd.read_csv(root_dir / "data/jobs.csv", index_col=None)
    
    train_clusters(jobs)
    