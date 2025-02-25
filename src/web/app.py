import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from flask import Flask, render_template, request, jsonify
from src.recommender.hybrid_recommender import HybridRecommender

app = Flask(__name__)

# Ensure the CSV file exists
csv_path = project_root / 'ieee_articles.csv'
print(f"Looking for CSV file at: {csv_path}")
if not csv_path.exists():
    raise FileNotFoundError(f"The file {csv_path} does not exist. Please run the ieee_scraper.py script first.")

# Initialize the recommender system
recommender = HybridRecommender(str(csv_path))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    query = request.form['keyword']
    recommendations = recommender.get_recommendations(query)
    response = []
    
    # Build the response with all required columns
    for rec in recommendations:
        paper = recommender.df[recommender.df['title'] == rec]
        if not paper.empty:
            response.append({
                "title": rec,
                "url": str(paper['url'].values[0]),
                "abstract": str(paper['abstract'].values[0]),
                "authors": str(paper['authors'].values[0]),
                "keyword": query
            })
    
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
