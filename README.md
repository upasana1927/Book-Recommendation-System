Book Recommendation System

A web-based book recommendation system that suggests books based on mood, genre, or user input using Machine Learning (TF-IDF and cosine similarity).

Features:

    View random books on the homepage.

    Search books by name,mood or genre.

    AI-powered recommendations based on user input.

    Clean and responsive web interface.

Tech Stack

    Backend: Python, Flask

    Frontend: HTML, CSS, JavaScript

    ML: scikit-learn (TF-IDF, cosine similarity)

    Data: CSV dataset of books 

Installation

    Clone the repository:

    git clone https://github.com/upasana1927/Book-Recommendation-System
    cd Book-Recommendation-System

Install dependencies:

    pip install -r requirements.txt

Run the Flask app:

    python app.py

    Open your browser and go to http://127.0.0.1:5000/.

Dataset

    The app expects a CSV file with the following columns:

    title – Book title

    author – Book author

    genre – Book genre

    mood – Mood category

    description – Book description

    coverimage – (Optional) URL to book cover

    freelink – (Optional) Link to read online

Usage

    Navigate to Home to see random books.

    Go to Recommendation to search by name, mood or genre.

    Enter a query in the search box to get AI-powered suggestions.

Future Scope

    Personalized User Profiles: Save user preferences and reading history for better recommendations.

    Collaborative Filtering: Combine user ratings with content-based filtering for more accurate suggestions.

    Advanced NLP Models: Use BERT or GPT embeddings for semantic understanding of book descriptions.

    Recommendation by Reviews: Include user reviews to improve suggestions.

    Mobile App: Convert the system into a mobile-friendly application.

    Integration with APIs: Connect to external book databases like Google Books or Goodreads.

    Visual Recommendations: Include book covers, ratings, and links to online reading platforms.