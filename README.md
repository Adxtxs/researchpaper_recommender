# IEEE Research Paper Recommendation System

## Overview
This project implements a **research paper recommendation system** that suggests relevant IEEE Xplore articles using different recommendation techniques.

## Features
- **Web Scraping**: Extracts research papers from IEEE Xplore.
- **Data Preprocessing**: Cleans and processes text data.
- **Content-Based Filtering**:
  - Uses **TF-IDF & Cosine Similarity**.
  - Implements **K-Nearest Neighbors (KNN)** with Bag of Words and Euclidean Distance.
  - Integration of **Word2Vec model with Cosine Similarity** for semantic similarity.
- **Collaborative Filtering**: Planned for future implementation to recommend papers based on user preferences.
- **Hybrid Recommendation System**:
  - Combines Content-Based Filtering and Collaborative Filtering for better recommendations.
- **PageRank Algorithm Using Neo4j**: Planned for graph-based recommendations. (not implemented)

## Approach

To overcome the limitations of individual recommendation techniques, this system uses a hybrid approach with the following models:

### 1. **Content-Based Filtering**
- **TF-IDF & Cosine Similarity**: Finds papers with similar textual content.
- **K-Nearest Neighbors (KNN)**: Uses Bag of Words representation and Euclidean Distance.

### 2. **Collaborative Filtering**
- Planned: Recommends papers based on user-item interaction data.

### 3. **Hybrid Recommendation System**
- Combines results from Content-Based Filtering and Collaborative Filtering to provide more comprehensive recommendations.

### 4. **PageRank Algorithm Using Neo4j**
- Planned: Graph-based recommendation system leveraging Neo4j to rank papers based on their importance within a citation network.

## How It Works

1. **Scraping Research Papers**
   - Extracts research papers from IEEE Xplore based on user queries.

2. **Preprocessing Data**
   - Cleans text data, tokenizes abstracts, and converts them into TF-IDF vectors, Bag-of-Words representations, or Word2Vec embeddings (planned).

3. **Generating Recommendations**
   - Uses Content-Based Filtering to find similar papers.
   - Applies Collaborative Filtering (planned) to refine recommendations.
   - The Hybrid System combines both approaches for improved accuracy.

4. **Getting Top Recommendations**
   - Computes similarity scores using TF-IDF & Cosine Similarity, KNN, and (planned) Word2Vec.
   - Sorts papers by similarity and selects the top N most relevant recommendations. (top 10)

## Setting up the Virtual Environment

1. Open Command Prompt and navigate to your project directory:
    ```sh
    cd D:/Projects/researchpaper_recommender
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:
    ```sh
    .\venv\Scripts\activate
    ```

4. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Future Improvements

- Implementing Collaborative Filtering using user-item interaction data.
- Enhancing the Hybrid System by dynamically weighting Content-Based and Collaborative Filtering results.
- Integrating Neo4j for graph-based citation network analysis with the PageRank algorithm.
- Incorporating Word2Vec or other semantic similarity models for improved text processing.
- or anything else.....
