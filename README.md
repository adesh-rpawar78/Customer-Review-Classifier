<img width="3454" height="1926" alt="image" src="https://github.com/user-attachments/assets/368298fb-bc54-4e5b-89cd-9411e2fb5dcf" />

# Customer Review Analyzer using NLP

A full-stack machine learning web application that analyzes customer reviews using **Natural Language Processing (NLP)** and classifies them as **Good** or **Bad** reviews.

The application combines **TF-IDF feature extraction, SVD dimensionality reduction, Random Forest classification, and VADER sentiment analysis** with a Flask backend and MySQL database.

---

## 🚀 Project Overview

Customer reviews contain valuable information about customer satisfaction, but manually analyzing large numbers of reviews is time-consuming.

This project provides an automated solution that:

* Accepts customer reviews through a web interface
* Cleans and preprocesses review text
* Converts text into numerical features using TF-IDF
* Reduces feature dimensionality using SVD
* Classifies reviews using a Random Forest model
* Calculates sentiment using VADER
* Stores predictions and sentiment results in MySQL
* Provides user authentication
* Maintains prediction history
* Displays prediction statistics through a dashboard

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │    Customer/User    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Flask Web App    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Text Preprocessing│
                    │                     │
                    │ • Lowercasing       │
                    │ • Stopword Removal  │
                    │ • POS Tagging       │
                    │ • Lemmatization     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   TF-IDF Vectorizer │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       SVD           │
                    │ Dimensionality      │
                    │ Reduction           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Random Forest Model │
                    └──────────┬──────────┘
                               │
                     ┌─────────┴─────────┐
                     ▼                   ▼
              Good / Bad Review    Confidence Score
                     │
                     ▼
             ┌───────────────┐
             │ VADER Sentiment│
             └───────┬───────┘
                     │
                     ▼
             ┌───────────────┐
             │     MySQL     │
             │   Database    │
             └───────────────┘
```

---

## 🧠 Machine Learning Pipeline

The trained model follows this pipeline:

```text
Raw Customer Review
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
Random Forest Classification
        ↓
Good / Bad Prediction
```

Sentiment analysis is performed separately using VADER:

```text
Customer Review
       ↓
VADER Sentiment Analyzer
       ↓
Positive / Neutral / Negative
       ↓
Compound Sentiment Score
```

---

## ✨ Features

### Authentication

* User registration
* Secure password hashing
* Login/logout
* Session-based authentication
* User-specific prediction history

### Review Classification

* Good review prediction
* Bad review prediction
* Model confidence score
* Input validation

### Sentiment Analysis

The application calculates:

* Positive sentiment
* Neutral sentiment
* Negative sentiment
* Compound sentiment score

### Prediction History

Users can view previous predictions including:

* Review text
* Prediction
* Confidence
* Sentiment scores
* Prediction timestamp

### Dashboard

The dashboard provides aggregated information such as:

* Total predictions
* Good reviews
* Bad reviews
* Average confidence
* Average sentiment scores

---

## 🛠️ Technology Stack

| Category                 | Technology        |
| ------------------------ | ----------------- |
| Programming Language     | Python            |
| Backend                  | Flask             |
| Authentication           | Flask-Login       |
| Machine Learning         | Scikit-learn      |
| NLP                      | NLTK              |
| Sentiment Analysis       | VADER             |
| Feature Extraction       | TF-IDF            |
| Dimensionality Reduction | Truncated SVD     |
| ML Algorithm             | Random Forest     |
| Database                 | MySQL             |
| Frontend                 | HTML, CSS, Jinja2 |
| Model Serialization      | Pickle            |
| Version Control          | Git / GitHub      |

---

## 📁 Project Structure

```text
Customer-review-with-NLP/
│
├── app.py
├── database.py
├── requirements.txt
├── schema.sql
│
├── random_forest_model.pkl
├── tfidf_vectorizer.pkl
├── svd.pkl
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── history.html
│   └── dashboard.html
│
├── notebooks/
│   └── Detecting bad customer reviews with NLP.ipynb
│
└── README.md
```

> The virtual environment (`myenv/`) should not be committed to GitHub.

---

## 🔐 Database Design

The application uses MySQL to store users and prediction results.

### Users

```text
users
├── id
├── username
├── password_hash
└── created_at
```

### Predictions

```text
predictions
├── id
├── user_id
├── review_text
├── prediction
├── confidence
├── sentiment_pos
├── sentiment_neu
├── sentiment_neg
├── sentiment_compound
└── created_at
```

The `user_id` relationship ensures that users can access their own prediction history.

---

## 📊 Example Predictions

### Good Review

**Input**

```text
The hotel was amazing, clean and comfortable.
The staff were very friendly.
```

**Output**

```text
Prediction: Good Review
Confidence: 100%

Sentiment
Positive: 62.40%
Neutral: 37.60%
Negative: 0.00%
Compound: 0.923
```

### Bad Review

**Input**

```text
Terrible experience. The room was dirty,
the staff were rude and the service was horrible.
```

**Output**

```text
Prediction: Bad Review
Confidence: 63%

Sentiment
Positive: 0.00%
Neutral: 46.80%
Negative: 53.20%
Compound: -0.910
```

> Prediction values can vary depending on the trained model and preprocessing configuration.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Customer-review-with-NLP
```

### 2. Create a virtual environment

```bash
python3 -m venv myenv
```

### 3. Activate the environment

macOS/Linux:

```bash
source myenv/bin/activate
```

Windows:

```bash
myenv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ MySQL Configuration

Create the database:

```sql
CREATE DATABASE review_classifier;
```

Then execute the SQL schema:

```bash
mysql -u root -p review_classifier < schema.sql
```

Update your database configuration in `database.py` according to your local MySQL credentials.

For production, database credentials should be stored in environment variables instead of being committed to GitHub.

---

## ▶️ Run the Application

Activate the virtual environment:

```bash
source myenv/bin/activate
```

Start Flask:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🔑 Application Flow

```text
Register
   ↓
Login
   ↓
Enter Customer Review
   ↓
Validate Input
   ↓
Preprocess Text
   ↓
Generate TF-IDF Features
   ↓
Apply SVD
   ↓
Random Forest Prediction
   ↓
Calculate Confidence
   ↓
VADER Sentiment Analysis
   ↓
Store Result in MySQL
   ↓
Display Result
   ↓
History / Dashboard
```

---

## 🧪 Input Validation

The application prevents invalid input such as:

```text
123456789
```

and displays:

```text
Please enter a meaningful customer review containing text.
```

This prevents the prediction pipeline from processing meaningless input.

---

## 📈 Model Evaluation

The machine learning notebook contains the model development and evaluation workflow.

Recommended metrics to report here after final model evaluation:

```text
Accuracy: XX.XX%
Precision: XX.XX%
Recall: XX.XX%
F1-Score: XX.XX%
ROC-AUC: XX.XX%
```

**Do not add numbers until they are calculated from your final trained model.**

---

## 🔬 Machine Learning Components

### TF-IDF

TF-IDF converts review text into numerical features based on the importance of words within the dataset.

### SVD

Truncated SVD reduces the dimensionality of the TF-IDF feature matrix while preserving important information.

### Random Forest

Random Forest is used as the classification algorithm to predict whether the review belongs to the Good or Bad class.

### VADER

VADER provides sentiment scores that complement the classification model by identifying positive, neutral, and negative sentiment.

---

## 🔒 Security Considerations

The application includes:

* Password hashing using Werkzeug
* Login-protected routes
* User-specific database queries
* Parameterized SQL queries
* Session-based authentication

For production deployment, additional security measures should be added, including:

* Environment-based secrets
* CSRF protection
* Secure session cookies
* HTTPS
* Database connection security
* Production WSGI server

---

## 🚀 Future Improvements

Potential improvements include:

* Improve classification performance through hyperparameter tuning
* Add cross-validation
* Add model evaluation charts
* Add confusion matrix
* Add ROC and Precision-Recall curves
* Add BERT/Transformer-based classification
* Add REST API endpoints
* Add Docker support
* Add CI/CD pipeline
* Deploy using AWS or another cloud platform
* Add monitoring and logging
* Add batch review processing
* Add CSV upload for multiple reviews
* Add admin analytics

---

## 🎯 Learning Outcomes

This project demonstrates practical experience with:

* Python backend development
* Flask
* REST/web application architecture
* Natural Language Processing
* Text preprocessing
* Machine learning classification
* Feature engineering
* Sentiment analysis
* MySQL database integration
* Authentication
* Model serialization
* Git/GitHub
* End-to-end ML application development

---

Skills demonstrated in this project:

`Python` · `SQL` · `Machine Learning` · `NLP` · `Flask` · `MySQL` · `Scikit-learn` · `NLTK` · `Git`

---
