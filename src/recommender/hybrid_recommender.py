# from .content_based import ContentBasedRecommender
# from .collaborative import CollaborativeRecommender

# class HybridRecommender:
#     def __init__(self, data_file):
#         self.content_based = ContentBasedRecommender(data_file)
#         self.collaborative = CollaborativeRecommender(data_file)
#         # Initialize df from content-based recommender
#         self.df = self.content_based.df

#     def get_recommendations(self, query, top_n=10):
#         content_recs = set(self.content_based.get_recommendations(query, top_n))
#         collab_recs = set(self.collaborative.get_recommendations(query, top_n))
#         hybrid_recs = list(content_recs.union(collab_recs))
#         return hybrid_recs[:top_n]

from .content_based import ContentBasedRecommender
from .collaborative import CollaborativeRecommender
import sqlite3
import pandas as pd


class HybridRecommender:
    def __init__(self, db_path):
        self.db_path = db_path
        self.content_based = ContentBasedRecommender(db_path)
        self.collaborative = CollaborativeRecommender(db_path)

    def get_recommendations(self, query, top_n=30):
        content_recs = set(
            self.content_based.get_recommendations(query, top_n))
        collab_recs = set(self.collaborative.get_recommendations(query, top_n))
        hybrid_recs = list(content_recs.union(
            collab_recs))  # Combine both methods

        # Fetch full details for the recommendations
        conn = sqlite3.connect(self.db_path)
        query_placeholders = ', '.join(['?'] * len(hybrid_recs))
        query_sql = f"SELECT title, url, abstract, authors FROM papers WHERE title IN ({query_placeholders})"

        if hybrid_recs:
            results = pd.read_sql(query_sql, conn, params=hybrid_recs)
        else:
            results = pd.DataFrame(
                # pass the query as keyword
                columns=['title', 'url', 'abstract', 'authors'])

        conn.close()
        return results.to_dict(orient="records")[:top_n]
