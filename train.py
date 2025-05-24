import pandas
from models import train_clusters

df = pandas.read_csv('data/jobs.csv')
train_clusters(df)