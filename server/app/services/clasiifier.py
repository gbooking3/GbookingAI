import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
import os

training_data = [
    #positive confirmations
    ("yes", "confirmation"),
    ("sure", "confirmation"),
    ("okay", "confirmation"),
    ("yes please", "confirmation"),
    ("absolutely", "confirmation"),
    ("sounds good", "confirmation"),

    ("i want to set an appointment", "start_booking"),
    ("i want to schedule an appointment", "start_booking"), 
    ("hello I want to set an appointment", "start_booking"),
    ("I want to book an appointment", "start_booking"),
    ("How do I schedule a visit?", "start_booking"),
    ("I need to make an appointment", "start_booking"),
    ("Help me book a doctor", "start_booking"),
    ("How can I schedule an appointment?", "start_booking"),

    ("hello, how are you?", "chitchat"),
    ("hello my friend", "chitchat"),
    ("hello i want to set an appointment", "chitchat"),
    ("Are you feeling good today?", "chitchat"),

        # Start booking intent

    ("departments", "choose_department"),
    ("I want to see a cardiologist", "choose_department"),
    ("show me departments", "choose_department"),


]


# 2. Preprocessing
def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

X = [clean_text(t[0]) for t in training_data]
y = [t[1] for t in training_data]

# 3. TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# 4. Train Classifier
clf = LogisticRegression()
clf.fit(X_vec, y)

save_path = os.path.dirname(__file__)  # this gets the current file's directory
os.makedirs(save_path, exist_ok=True)
file_path = os.path.join(save_path, "intent_model.pkl")

with open(file_path, "wb") as f:
    pickle.dump((vectorizer, clf), f)


