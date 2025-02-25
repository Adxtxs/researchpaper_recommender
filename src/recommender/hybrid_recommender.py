from .content_based import ContentBasedRecommender
from .collaborative import CollaborativeRecommender

class HybridRecommender:
    def __init__(self, data_file):
        self.content_based = ContentBasedRecommender(data_file)
        self.collaborative = CollaborativeRecommender(data_file)
        # Initialize df from content-based recommender
        self.df = self.content_based.df

    def get_recommendations(self, query, top_n=10):
        content_recs = set(self.content_based.get_recommendations(query, top_n))
        collab_recs = set(self.collaborative.get_recommendations(query, top_n))
        hybrid_recs = list(content_recs.union(collab_recs))
        return hybrid_recs[:top_n]
