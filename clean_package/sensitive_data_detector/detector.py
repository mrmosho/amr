import spacy
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib
from typing import List, Dict, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DetectionResult:
    def __init__(self, is_sensitive: bool, confidence: float, entities: List[Dict[str, Any]], 
                 sensitive_type: Optional[str] = None, sensitive_value: Optional[str] = None):
        self.is_sensitive = is_sensitive
        self.confidence = confidence
        self.entities = entities
        self.sensitive_type = sensitive_type
        self.sensitive_value = sensitive_value

class SensitiveDataDetector:
    def __init__(self, model_path: str = 'models/sensitive_detector_model.joblib',
                 vectorizer_path: str = 'models/text_vectorizer.joblib'):
        """Initialize the sensitive data detector.
        
        Args:
            model_path: Path to the trained model file
            vectorizer_path: Path to the text vectorizer file
        """
        try:
            self.nlp = spacy.load('en_core_web_sm')
            self.model = joblib.load(model_path)
            self.vectorizer = joblib.load(vectorizer_path)
            logger.info("Model and vectorizer loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model or vectorizer: {str(e)}")
            raise

    def detect(self, text: str) -> DetectionResult:
        """Detect sensitive information in the given text.
        
        Args:
            text: The text to analyze
            
        Returns:
            DetectionResult object containing detection results
        """
        try:
            # Vectorize the text
            text_vec = self.vectorizer.transform([text])
            
            # Get prediction and probability
            prediction = self.model.predict(text_vec)[0]
            confidence = self.model.predict_proba(text_vec)[0][1]
            
            # Get named entities
            doc = self.nlp(text)
            entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
            
            # Determine sensitive type if any
            sensitive_type = None
            sensitive_value = None
            if prediction:
                # Check for specific sensitive types
                if any(ent['label'] in ['PERSON', 'ORG', 'GPE'] for ent in entities):
                    sensitive_type = 'Named Entity'
                    sensitive_value = next((ent['text'] for ent in entities 
                                         if ent['label'] in ['PERSON', 'ORG', 'GPE']), None)
                elif '@' in text and '.' in text.split('@')[1]:
                    sensitive_type = 'Email'
                    sensitive_value = text.split('@')[0] + '@' + text.split('@')[1].split()[0]
                elif any(c.isdigit() for c in text) and len(text.split()) <= 3:
                    sensitive_type = 'Numeric'
                    sensitive_value = text
            
            return DetectionResult(
                is_sensitive=bool(prediction),
                confidence=float(confidence),
                entities=entities,
                sensitive_type=sensitive_type,
                sensitive_value=sensitive_value
            )
            
        except Exception as e:
            logger.error(f"Error during detection: {str(e)}")
            raise

    def batch_detect(self, texts: List[str]) -> List[DetectionResult]:
        """Detect sensitive information in multiple texts.
        
        Args:
            texts: List of texts to analyze
            
        Returns:
            List of DetectionResult objects
        """
        return [self.detect(text) for text in texts]

    def get_sensitive_summary(self, result: DetectionResult) -> str:
        """Get a detailed summary of the detection results.
        
        Args:
            result: DetectionResult object
            
        Returns:
            Formatted summary string
        """
        summary = []
        summary.append(f"Sensitive: {result.is_sensitive}")
        summary.append(f"Confidence: {result.confidence:.2%}")
        
        if result.entities:
            summary.append("\nNamed Entities:")
            for ent in result.entities:
                summary.append(f"- {ent['text']} ({ent['label']})")
        
        if result.sensitive_type:
            summary.append(f"\nSensitive Type: {result.sensitive_type}")
            if result.sensitive_value:
                summary.append(f"Sensitive Value: {result.sensitive_value}")
        
        return "\n".join(summary) 