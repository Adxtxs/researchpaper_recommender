import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentBasedRecommender:
    def __init__(self, data_file):
        self.df = pd.read_csv(data_file)
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['abstract'].fillna(''))
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def get_recommendations(self, query, top_n=10):
        if query in self.df['title'].values:
            idx = self.df[self.df['title'] == query].index[0]
        else:
            query_vec = self.tfidf.transform([query])
            sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
            idx = sim_scores.argsort()[-top_n:][::-1]
            return self.df['title'].iloc[idx].tolist()

        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]
        paper_indices = [i[0] for i in sim_scores]
        return self.df['title'].iloc[paper_indices].tolist()
