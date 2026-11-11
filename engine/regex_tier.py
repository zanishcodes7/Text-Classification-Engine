import re
import time 
class RegexClassifier:
    def __init__(self):
         # Define high_confidence, self, deterministic patterns
       self.patterns = {
            "Complaint": [
                r"refund|broken|horrible|scam|terrible|worst|not working|failed|error|fraud|disappointed|bad|hate|hated",
                r"cancel my account|chargeback|poor service|never again|hate this|did not work"
            ],
            "Praise": [
                r"excellent|amazing|love|loved|love this|loved it|great|great job|fantastic|wonderful|best service|superb",
                r"thank you|thanks a lot|highly recommend|loved this website"
            ],
            "Question": [
                r"how do i|how to|where is|can i|what is|when will|is it possible",
                r"\?"
            ]
        }
        # Compile patterns in advance 
       self.compiled_rules = {
            category: [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
            for category, patterns in self.patterns.items()
        }
    def classify(self, text: str):
        start_time = time.perf_counter()
        text_lower = text.lower().strip()
        
        for category, compiled_list in self.compiled_rules.items():
            for pattern in compiled_list:
                if pattern.search(text_lower):
                    latency = round((time.perf_counter() - start_time) * 1000, 3)
                    return {
                        "category": category,
                        "confidence": 1.0,
                        "tier_executed": "Tier 1: Regex Pattern Matcher",
                        "latency_ms": f"{latency} ms"
                    }
        return None