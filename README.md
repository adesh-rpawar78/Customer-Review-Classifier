<img width="3454" height="1926" alt="image" src="https://github.com/user-attachments/assets/368298fb-bc54-4e5b-89cd-9411e2fb5dcf" />

# Customer Review Analyzer using NLP

A machine learning web application that analyzes customer reviews using **Natural Language Processing (NLP)** and predicts whether a review is **Good** or **Bad**.

The application also performs sentiment analysis and provides prediction confidence.

## Features

* User registration and login
* Customer review analysis
* Good / Bad review prediction
* Prediction confidence percentage
* Sentiment analysis

  * Positive
  * Neutral
  * Negative
  * Compound sentiment score
* Prediction history
* User-specific dashboard
* MySQL database integration
* Flask web application
* Input validation for invalid reviews

## Technologies Used

* Python
* Flask
* Flask-Login
* Scikit-learn
* NLTK
* VADER Sentiment Analysis
* TF-IDF
* Truncated SVD
* Random Forest Classifier
* MySQL
* HTML
* CSS
* Jinja2

## Machine Learning Pipeline

```text
Customer Review
       ↓
Text Cleaning
       ↓
Stopword Removal
       ↓
POS Tagging
       ↓
Lemmatization
       ↓
TF-IDF Vectorization
       ↓
SVD Dimensionality Reduction
       ↓
Random Forest Classifier
       ↓
Good / Bad Prediction
```

## Project Structure

```text
Customer-review-with-NLP/
│
├── app.py
├── database.py
├── requirements.txt
│
├── random_forest_model.pkl
├── tfidf_vectorizer.pkl
├── svd.pkl
│
├── schema.sql
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── history.html
│   └── dashboard.html
│
└── myenv/
```

## How to Run

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd Customer-review-with-NLP
```

### 2. Create a virtual environment

```bash
python3 -m venv myenv
```

### 3. Activate the virtual environment

```bash
source myenv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure MySQL

Create the required database and tables using:

```bash
mysql -u root -p
```

Then run the SQL from:

```text
schema.sql
```

Make sure the database configuration in `database.py` matches your local MySQL setup.

### 6. Start the Flask application

```bash
python app.py
```

The application will run at:

```text
http://127.0.0.1:5000
```

## Example

### Positive Review

```text
The hotel was amazing, clean and comfortable.
The staff were very friendly.
```

Expected result:

```text
Prediction: Good Review
Sentiment: Positive
```

### Negative Review

```text
Terrible experience. The room was dirty,
the staff were rude and the service was horrible.
```

Expected result:

```text
Prediction: Bad Review
Sentiment: Negative
```

## Database

The application stores:

* User accounts
* Customer reviews
* Prediction results
* Prediction confidence
* Sentiment scores
* Prediction timestamps

## Future Improvements

* Improve model accuracy
* Add model performance metrics
* Add charts and visual analytics
* Deploy the application to a cloud platform
* Add REST API endpoints
* Add real-time review analysis
* Add advanced transformer-based NLP models such as BERT
* Add admin analytics

## Author

**Aadesh Pawar**

B.E. Artificial Intelligence & Data Science
