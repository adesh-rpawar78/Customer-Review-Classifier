import os
import pickle
import string

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

from database import get_connection, init_db


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-change-me")

login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin):

    def __init__(self, id, username):
        self.id = id
        self.username = username


@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, username FROM users WHERE id = %s",
        (user_id,),
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return User(row["id"], row["username"])

    return None


model = pickle.load(
    open("random_forest_model.pkl", "rb")
)

vectorizer = pickle.load(
    open("tfidf_vectorizer.pkl", "rb")
)

svd = pickle.load(
    open("svd.pkl", "rb")
)


def get_wordnet_pos(tag):
    if tag.startswith("J"):
        return wordnet.ADJ

    if tag.startswith("V"):
        return wordnet.VERB

    if tag.startswith("N"):
        return wordnet.NOUN

    if tag.startswith("R"):
        return wordnet.ADV

    return wordnet.NOUN


def clean_text(text):
    text = text.lower()

    words = [
        word.strip(string.punctuation)
        for word in text.split()
    ]

    words = [
        word
        for word in words
        if not any(character.isdigit() for character in word)
    ]

    stop = stopwords.words("english")

    words = [
        word
        for word in words
        if word and word not in stop
    ]

    tags = pos_tag(words)

    lemmatizer = WordNetLemmatizer()

    return " ".join(
        lemmatizer.lemmatize(
            word,
            get_wordnet_pos(tag),
        )
        for word, tag in tags
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for("register"))

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE username = %s",
            (username,),
        )

        if cursor.fetchone():
            flash("That username is already taken.")

            cursor.close()
            conn.close()

            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)

        cursor.execute(
            """
            INSERT INTO users
            (username, password_hash)
            VALUES (%s, %s)
            """,
            (username, password_hash),
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash("Account created. Please log in.")

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE username = %s",
            (username,),
        )

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row and check_password_hash(
            row["password_hash"],
            password,
        ):
            login_user(
                User(
                    row["id"],
                    row["username"],
                )
            )

            return redirect(url_for("home"))

        flash("Invalid username or password.")

        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    prediction = None
    confidence = None
    sentiment = None
    review = None

    if request.method == "POST":
        review = request.form["review"].strip()

        if not review:
            flash("Please enter a review.")
            return redirect(url_for("home"))

        # Check whether the review contains meaningful alphabetic text
        if not any(character.isalpha() for character in review):
            flash(
                "Please enter a meaningful customer review containing text."
            )
            return redirect(url_for("home"))

        cleaned = clean_text(review)

        # Make sure text remains after preprocessing
        if not cleaned.strip():
            flash("Please enter a meaningful customer review.")
            return redirect(url_for("home"))

        X = vectorizer.transform([cleaned])

        X_svd = svd.transform(X)

        prediction = int(
            model.predict(X_svd)[0]
        )

        probabilities = model.predict_proba(X_svd)[0]

        confidence = float(
            max(probabilities)
        )

        sid = SentimentIntensityAnalyzer()

        sentiment = sid.polarity_scores(review)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO predictions
            (
                user_id,
                review_text,
                prediction,
                confidence,
                sentiment_pos,
                sentiment_neu,
                sentiment_neg,
                sentiment_compound
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                current_user.id,
                review,
                prediction,
                confidence,
                sentiment["pos"],
                sentiment["neu"],
                sentiment["neg"],
                sentiment["compound"],
            ),
        )

        conn.commit()

        cursor.close()
        conn.close()

    return render_template(
        "index.html",
        review=review,
        prediction=prediction,
        confidence=confidence,
        sentiment=sentiment,
    )


@app.route("/history")
@login_required
def history():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM predictions
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT 50
        """,
        (current_user.id,),
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "history.html",
        predictions=rows,
    )


@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            COUNT(*) AS total_predictions,
            SUM(prediction = 0) AS good_reviews,
            SUM(prediction = 1) AS bad_reviews,
            AVG(confidence) AS average_confidence,
            AVG(sentiment_pos) AS average_positive,
            AVG(sentiment_neu) AS average_neutral,
            AVG(sentiment_neg) AS average_negative,
            AVG(sentiment_compound) AS average_compound
        FROM predictions
        WHERE user_id = %s
        """,
        (current_user.id,),
    )

    stats = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        stats=stats,
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
