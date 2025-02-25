import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

nltk.download('punkt')
nltk.download('stopwords')

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower()
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(tokens)

def preprocess_data(input_file, output_file):
    df = pd.read_csv(input_file)
    df['cleaned_abstract'] = df['abstract'].apply(clean_text)
    df['cleaned_title'] = df['title'].apply(clean_text)
    df.to_csv(output_file, index=False)
    print(f"Preprocessed data saved to {output_file}")

if __name__ == "__main__":
    preprocess_data('ieee_articles.csv', 'preprocessed_papers.csv')
