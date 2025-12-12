import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


books_df = pd.read_csv("data/books.csv")
books_df.columns = books_df.columns.str.strip().str.lower()
books_df = books_df.fillna("")


if "id" not in books_df.columns:
    books_df["id"] = books_df.index.astype(str)

books_df['combined_text'] = (
    books_df['title'].astype(str) + " " +
    books_df['author'].astype(str) + " " +
    books_df['genre'].astype(str) + " " +
    books_df['mood'].astype(str) + " " +
    books_df['description'].astype(str) + " " +
    books_df['review'].astype(str)
)


vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = vectorizer.fit_transform(books_df['combined_text'])

def get_top_books(n=12):
    return books_df.sample(n).to_dict(orient="records")

def get_recommendations(query, top_n=12):
    user_vec = vectorizer.transform([query])
    similarity_scores = cosine_similarity(user_vec, tfidf_matrix).flatten()
    books_df["score"] = similarity_scores + 0.1 * books_df["rating"].astype(float)
    top_books = books_df.sort_values("score", ascending=False).head(top_n)
    return top_books.to_dict(orient="records")
