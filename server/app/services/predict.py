# app/services/intent_classifier.py

from transformers import DistilBertTokenizerFast, DistilBertModel
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.base import BaseEstimator, TransformerMixin
import torch

# Load tokenizer and model
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
bert_model = DistilBertModel.from_pretrained('distilbert-base-uncased')

# Custom Transformer to convert text to embeddings
class BERTEmbedder(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        with torch.no_grad():
            inputs = tokenizer(X, padding=True, truncation=True, return_tensors="pt")
            outputs = bert_model(**inputs)
            embeddings = outputs.last_hidden_state[:, 0, :].numpy()  # CLS token
        return embeddings

# Training data
texts = [
    "yes", "sure", "okay", "yes please", "absolutely", "sounds good",
    "i want to set an appointment", "hello I want to set an appointment",
    "I want to book an appointment", "I need to make an appointment",
    "How do I schedule a visit?", "Help me book a doctor",
    "hello, how are you?", "hello my friend", "Are you feeling good today?",
    "departments", "I want to see a cardiologist", "show me departments",
    "קרדיולוגיה", "cardiology",
    "גסטרואנטרולוגיה", "gastroenterology",
    "נוירולוגיה", "neurology",
    "CT", "ct scan"
]
labels = [
    "confirmation", "confirmation", "confirmation", "confirmation", "confirmation", "confirmation",
    "start_booking", "start_booking", "start_booking", "start_booking",
    "start_booking", "start_booking",
    "chitchat", "chitchat", "chitchat",
    "choose_department", "choose_department", "choose_department",
    "choose_department", "choose_department",
    "choose_department", "choose_department",
    "choose_department", "choose_department",
    "choose_department", "choose_department"
]

# Build pipeline and fit it
pipeline = make_pipeline(BERTEmbedder(), LogisticRegression(max_iter=1000))
pipeline.fit(texts, labels)

# Exportable function
def predict_intent(text):
    return pipeline.predict([text])[0]
