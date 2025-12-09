from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

books_df = pd.read_csv("data/books.csv")
books_df.columns = books_df.columns.str.strip().str.lower()
books_df = books_df.fillna('')

books_df['combined_text'] = (
    books_df['title'].astype(str) + " " +
    books_df['genre'].astype(str) + " " +
    books_df['mood'].astype(str) + " " +
    books_df['description'].astype(str)
)

vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(books_df['combined_text'])

similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_top_books(n=12):
    return books_df.sample(n).to_dict(orient='records')

def get_recommendations(user_input):
    user_vec = vectorizer.transform([user_input])
    similarity_scores = cosine_similarity(user_vec, tfidf_matrix).flatten()
    top_indices = similarity_scores.argsort()[-12:][::-1]
    return books_df.iloc[top_indices].to_dict(orient='records')

@app.route('/')
def home():
    return render_template('index.html', books=get_top_books())

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/search/mood', methods=['GET', 'POST'])
def search_mood():
    query = None
    recommended_books = []
    if request.method == 'POST':
        query = request.form.get('mood')
        if query:
            recommended_books = get_recommendations(query)
    return render_template('recommend_mood.html', query=query, books=recommended_books, similar=[])

@app.route('/search/genre', methods=['GET', 'POST'])
def search_genre():
    query = None
    recommended_books = []
    if request.method == 'POST':
        query = request.form.get('genre')
        if query:
            recommended_books = get_recommendations(query)
    return render_template('recommend_genre.html', query=query, books=recommended_books, similar=[])

if __name__ == "__main__":
    app.run(debug=True)
