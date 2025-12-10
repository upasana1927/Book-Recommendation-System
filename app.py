from flask import Flask, render_template, request, session, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Load dataset
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


# ----------------- Search with History ----------------- #
def update_history(key, query):
    if key not in session:
        session[key] = []
    if query and query not in session[key]:
        session[key].insert(0, query)
        session[key] = session[key][:5]  # keep last 5


@app.route('/search/name', methods=['GET', 'POST'])
def search_name():
    query = None
    recommended_books = []
    if request.method == 'POST':
        query = request.form.get('movie_name').strip()
        if query:
            update_history('name_history', query)
            mask = books_df['title'].str.lower().str.contains(query.lower())
            recommended_books = books_df[mask].to_dict(orient='records')
    history = session.get('name_history', [])
    return render_template('recommend_name.html', query=query, books=recommended_books, history=history)


@app.route('/search/genre', methods=['GET', 'POST'])
def search_genre():
    query = None
    recommended_books = []
    if request.method == 'POST':
        query = request.form.get('genre').strip()
        if query:
            update_history('genre_history', query)
            recommended_books = get_recommendations(query)
    history = session.get('genre_history', [])
    return render_template('recommend_genre.html', query=query, books=recommended_books, history=history)


@app.route('/search/mood', methods=['GET', 'POST'])
def search_mood():
    query = None
    recommended_books = []
    if request.method == 'POST':
        query = request.form.get('mood').strip()
        if query:
            update_history('mood_history', query)
            recommended_books = get_recommendations(query)
    history = session.get('mood_history', [])
    return render_template('recommend_mood.html', query=query, books=recommended_books, history=history)


# API for JavaScript auto-suggest
@app.route('/search/history')
def search_history():
    term = request.args.get('term', '').lower()
    search_type = request.args.get('type', 'name')  # name, genre, mood
    key = f"{search_type}_history"
    history = session.get(key, [])
    suggestions = [h for h in history if term in h.lower()]
    return jsonify(suggestions)


if __name__ == "__main__":
    app.run(debug=True)
