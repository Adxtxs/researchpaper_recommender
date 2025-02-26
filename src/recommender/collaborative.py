# import pandas as pd
# from sklearn.neighbors import NearestNeighbors
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# class CollaborativeRecommender:
#     def __init__(self, data_file):
#         self.df = pd.read_csv(data_file)
#         self.tfidf = TfidfVectorizer(stop_words='english')
#         self.tfidf_matrix = self.tfidf.fit_transform(self.df['abstract'].fillna(''))
#         self.nn = NearestNeighbors(metric='cosine', algorithm='brute')
#         self.nn.fit(self.tfidf_matrix)

#     def get_recommendations(self, query, top_n=10):
#         if query in self.df['title'].values:
#             idx = self.df[self.df['title'] == query].index[0]
#         else:
#             query_vec = self.tfidf.transform([query])
#             sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
#             idx = sim_scores.argsort()[-1]

#         distances, indices = self.nn.kneighbors(self.tfidf_matrix[idx], n_neighbors=top_n+1)
#         return self.df['title'].iloc[indices.flatten()[1:]].tolist()

import sqlite3
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeRecommender:
    def __init__(self, db_path):
        self.db_path = db_path

        # Load abstracts from SQLite
        conn = sqlite3.connect(self.db_path)
        self.df = pd.read_sql("SELECT title, abstract FROM papers", conn)
        conn.close()

        # TF-IDF Processing
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['abstract'].fillna(''))

        # Nearest Neighbors model
        self.nn = NearestNeighbors(metric='cosine', algorithm='brute')
        self.nn.fit(self.tfidf_matrix)

    def get_recommendations(self, query, top_n=10):
        query_vec = self.tfidf.transform([query])
        sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        idx = sim_scores.argsort()[-top_n:][::-1]

        return self.df['title'].iloc[idx].tolist()
