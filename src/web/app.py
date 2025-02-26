# import sys
# import os
# from pathlib import Path

# project_root = Path(__file__).parent.parent.parent
# sys.path.append(str(project_root))

# from flask import Flask, render_template, request, jsonify
# from src.recommender.hybrid_recommender import HybridRecommender

# app = Flask(__name__)

# # Ensure the CSV file exists
# csv_path = project_root / 'preprocessed_papers.csv'
# # csv_path = project_root / 'old_ieee_articles.csv'
# print(f"Looking for CSV file at: {csv_path}")
# if not csv_path.exists():
#     raise FileNotFoundError(f"The file {csv_path} does not exist. Please run the ieee_scraper.py script first.")

# # Initialize the recommender system
# recommender = HybridRecommender(str(csv_path))

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/recommend', methods=['POST'])
# def recommend():
#     query = request.form['keyword']
#     recommendations = recommender.get_recommendations(query)
#     response = []

#     # Build the response with all required columns
#     for rec in recommendations:
#         paper = recommender.df[recommender.df['title'] == rec]
#         if not paper.empty:
#             response.append({
#                 "title": rec,
#                 "url": str(paper['url'].values[0]),
#                 "abstract": str(paper['abstract'].values[0]),
#                 "authors": str(paper['authors'].values[0]),
#                 "keyword": query
#             })

#     return jsonify(response)


# if __name__ == '__main__':
#     app.run(debug=True)

# import sys
# import os
# from pathlib import Path
# import sqlite3
# from flask import Flask, render_template, request, jsonify

# project_root = Path(__file__).parent.parent.parent
# sys.path.append(str(project_root))
# from src.recommender.hybrid_recommender import HybridRecommender

# # Define paths
# db_path = project_root / 'papers.db'

# # Ensure the database exists
# if not db_path.exists():
#     raise FileNotFoundError(
#         f"The database {db_path} does not exist. Please run csv_to_sqlite.py first.")

# app = Flask(__name__)

# # Initialize recommender system
# recommender = HybridRecommender(str(db_path))  # Pass SQLite DB path


# @app.route('/')
# def home():
#     return render_template('index.html')


# @app.route('/recommend', methods=['POST'])
# def recommend():
#     query = request.form['keyword']
#     recommendations = recommender.get_recommendations(query)
#     recommendations.append({"keyword": query})

#     return jsonify(recommendations)


# if __name__ == '__main__':
#     app.run(debug=True)


import sys
import os
from pathlib import Path
import sqlite3
from flask import Flask, render_template, request, jsonify

project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))
from src.recommender.hybrid_recommender import HybridRecommender

# Define paths
db_path = project_root / 'papers.db'

# Ensure the database exists
if not db_path.exists():
    raise FileNotFoundError(f"The database {db_path} does not exist. Please run csv_to_sqlite.py first.")

app = Flask(__name__)

# Initialize recommender system
recommender = HybridRecommender(str(db_path))  # Pass SQLite DB path

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    query = request.form['keyword']
    page = int(request.form.get('page', 1))  # Get page number, default to 1
    per_page = 7  # Number of results per page
    
    recommendations = recommender.get_recommendations(query)
    
    # Pagination logic
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_recommendations = recommendations[start_idx:end_idx]
    
    return jsonify({
        "recommendations": paginated_recommendations,
        "total_pages": (len(recommendations) + per_page - 1) // per_page,
        "current_page": page
    })

if __name__ == '__main__':
    app.run(debug=True)
