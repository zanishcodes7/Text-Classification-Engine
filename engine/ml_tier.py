import os 
import pickle 
import time 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
class StatisticalMLClassifier:
    def __init__(self,model_path = "models/trained_vectorizer.pkl"):
        self.model_path = model_path
        self.vectorizer = None
        self.model = None
        self._initialize_model ()
    def _initialize_model(self):
        if os.path.exists (self.model_path):
            with open (self.model_path, "rb" ) as f:
                data = pickle.load(f)
                self.vectorizer = data["vectorizer"]
                self.model = data["model"]
        else:
            """training data set """
            training_data =[
                ("The item arrived completely shattered and unusable.", "Complaint"),
                ("I demand a full return for this defective purchase.", "Complaint"),
                ("The application freezes every time I navigate to settings.", "Complaint"),
                ("Customer support ignored my tickets for three weeks.", "Complaint"),
                ("Outstanding experience, user interface is clean and snappy.", "Praise"),
                ("Truly delighted with the fast delivery and top quality.", "Praise"),
                ("Extremely helpful support team, fixed my issue immediately.", "Praise"),
                ("Could you please inform me about your international shipping policy?", "Question"),
                ("Is there an option to export reporting metrics into CSV format?", "Question"),
                ("What are the pricing tiers for enterprise team accounts?", "Question")
            ]
            texts, labels = zip(*training_data)
            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
            X_vec = self.vectorizer.fit_transform(texts)
            
            self.model = LogisticRegression()
            self.model.fit(X_vec, labels)
            
            # Save for future use
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            with open(self.model_path, "wb") as f:
                pickle.dump({"vectorizer": self.vectorizer, "model": self.model}, f)
    def classify( self,text:str):
        start_time = time.perf_counter()
        text_vec = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vec)[0]
        probabilities = self.model.predict_proba(text_vec)[0]
        confidence = float(max (probabilities))
        latency = round ((time.perf_counter()- start_time) *1000,3)
        return {
            "category": prediction,
            "confidence": round (confidence,3 ),
            "tier_executed": "Tier 2: Statistical ML (TF-IDF)",
            "latency_ms": f"{latency} ms"
        }