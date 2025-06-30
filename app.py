from flask import Flask, request, render_template
import pickle
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import pos_tag
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
import string

app = Flask(__name__)

# Load saved models
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))
svd = pickle.load(open("svd.pkl", "rb"))

# Function to get wordnet POS tag
def get_wordnet_pos(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

# Text cleaning function
def clean_text(text):
    text = text.lower()
    text = [word.strip(string.punctuation) for word in text.split()]
    text = [word for word in text if not any(c.isdigit() for c in word)]
    stop = stopwords.words('english')
    text = [word for word in text if word and word not in stop]
    pos_tags = pos_tag(text)
    lemmatizer = WordNetLemmatizer()
    text = [lemmatizer.lemmatize(word, get_wordnet_pos(pos)) for word, pos in pos_tags]
    return " ".join(text)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        review = request.form["review"]

        # Clean text
        cleaned = clean_text(review)

        # TF-IDF + SVD transform
        X = vectorizer.transform([cleaned])
        X_svd = svd.transform(X)
        prediction = model.predict(X_svd)[0]

        # Sentiment analysis
        sid = SentimentIntensityAnalyzer()
        sentiment = sid.polarity_scores(review)

        # Override prediction if sentiment is clearly negative
        if sentiment["compound"] < -0.5:
            prediction = 1  # Bad review

        return render_template("index.html", review=review, prediction=prediction, sentiment=sentiment)

    return render_template("index.html", prediction=None)

if __name__ == "__main__":
    app.run(debug=True)
