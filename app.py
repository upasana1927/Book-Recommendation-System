from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sqlite3
import pandas as pd
from recommend_utils import get_top_books, get_recommendations, books_df

app = Flask(__name__)
app.secret_key = "your_secret_key"

USER_ID = 1  # Guest user

# ------------------------------
# Initialize session history
# ------------------------------
@app.before_request
def make_session_permanent():
    if 'name_history' not in session:
        session['name_history'] = []
    if 'mood_history' not in session:
        session['mood_history'] = []
    if 'genre_history' not in session:
        session['genre_history'] = []

# ------------------------------
# Home and Recommendation Pages
# ------------------------------
@app.route("/")
def home():
    return render_template("index.html", books=get_top_books())

@app.route("/recommend")
def recommend():
    return render_template("recommend.html")

# ------------------------------
# Search by Name
# ------------------------------
@app.route("/search/name", methods=["GET", "POST"])
def search_name():
    query = ""
    recommended_books = []

    if request.method == "POST":
        query = request.form.get("name", "").strip()
        if query:
            books_df['title'] = books_df['title'].fillna('').astype(str)
            mask = books_df['title'].str.contains(query, case=False, na=False)
            recommended_books = books_df[mask].to_dict(orient="records")

            # Update search history (last 10)
            history = session.get('name_history', [])
            if query not in history:
                history.append(query)
            session['name_history'] = history[-10:]

    return render_template(
        "recommend_name.html",
        query=query,
        books=recommended_books,
        history=session.get('name_history', [])
    )

# ------------------------------
# Search by Genre
# ------------------------------
@app.route("/search/genre", methods=["GET", "POST"])
def search_genre():
    query = ""
    recommended_books = []

    if request.method == "POST":
        query = request.form.get("genre", "").strip()
        if query:
            recommended_books = get_recommendations(query)

            # Update search history
            history = session.get('genre_history', [])
            if query not in history:
                history.append(query)
            session['genre_history'] = history[-10:]

    return render_template(
        "recommend_genre.html",
        query=query,
        books=recommended_books,
        history=session.get('genre_history', [])
    )

# ------------------------------
# Search by Mood
# ------------------------------
@app.route("/search/mood", methods=["GET", "POST"])
def search_mood():
    query = ""
    recommended_books = []

    if request.method == "POST":
        query = request.form.get("mood", "").strip()
        if query:
            recommended_books = get_recommendations(query)

            # Update search history
            history = session.get('mood_history', [])
            if query not in history:
                history.append(query)
            session['mood_history'] = history[-10:]

    return render_template(
        "recommend_mood.html",
        query=query,
        books=recommended_books,
        history=session.get('mood_history', [])
    )

# ------------------------------
# Favorites Page
# ------------------------------
@app.route("/favorites")
def favorites():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT book_id FROM favorites WHERE user_id=?", (USER_ID,))
    ids = cursor.fetchall()
    conn.close()

    fav_books = books_df[books_df["id"].astype(str).isin([i[0] for i in ids])]
    return render_template("favorites.html", books=fav_books.to_dict(orient="records"))

# ------------------------------
# Add to Favorites
# ------------------------------
@app.route("/add_favorite", methods=["POST"])
def add_favorite():
    book_id = request.form.get("book_id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO favorites (user_id, book_id) VALUES (?, ?)", (USER_ID, book_id))
    conn.commit()
    conn.close()
    return jsonify({"msg": "Added to Favorites!"})

# ------------------------------
# Remove from Favorites
# ------------------------------
@app.route("/remove_favorite/<book_id>", methods=["POST"])
def remove_favorite(book_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM favorites WHERE user_id=? AND book_id=?", (USER_ID, book_id))
    conn.commit()
    conn.close()
    return redirect(url_for("favorites"))

# ------------------------------
# Optional: Search history API for JS autocomplete
# ------------------------------
@app.route("/search/history")
def search_history():
    term = request.args.get("term", "").lower()
    type_ = request.args.get("type")
    hist = []

    if type_ == "name":
        hist = session.get('name_history', [])
    elif type_ == "mood":
        hist = session.get('mood_history', [])
    elif type_ == "genre":
        hist = session.get('genre_history', [])

    suggestions = [x for x in hist if term in x.lower()]
    return jsonify(suggestions)

# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
