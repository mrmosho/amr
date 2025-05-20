import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import spacy
import logging
from typing import Tuple, List
import joblib
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CombinedDataTrainer:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english'
        )
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
    
    def load_ner_dataset(self) -> Tuple[List[str], List[bool]]:
        """Load and process the NER dataset."""
        logger.info("Loading NER dataset...")
        df = pd.read_csv('data/ner_dataset.csv', encoding='latin1')
        
        # Group by sentence and collect words
        sentences = []
        current_sentence = []
        current_sentence_num = None
        
        for _, row in df.iterrows():
            if pd.isna(row['Word']):
                continue
                
            if pd.notna(row['Sentence #']):
                if current_sentence:
                    sentences.append(' '.join(current_sentence))
                current_sentence = []
                current_sentence_num = row['Sentence #']
            
            current_sentence.append(str(row['Word']))
        
        if current_sentence:
            sentences.append(' '.join(current_sentence))
        
        # Mark sentences as sensitive if they contain PERSON, ORG, or GPE entities
        sensitive_sentences = []
        for sentence in sentences:
            doc = self.nlp(sentence)
            is_sensitive = any(ent.label_ in ['PERSON', 'ORG', 'GPE'] for ent in doc.ents)
            sensitive_sentences.append(is_sensitive)
        
        return sentences, sensitive_sentences
    
    def load_synthetic_dataset(self) -> Tuple[List[str], List[bool]]:
        """Load the synthetic dataset."""
        logger.info("Loading synthetic dataset...")
        df = pd.read_csv('data/synthetic_sensitive_data.csv')
        return df['text'].tolist(), df['is_sensitive'].tolist()
    
    def combine_datasets(self) -> Tuple[List[str], List[bool]]:
        """Combine both datasets."""
        # Load both datasets
        ner_texts, ner_labels = self.load_ner_dataset()
        synth_texts, synth_labels = self.load_synthetic_dataset()
        
        # Combine datasets
        all_texts = ner_texts + synth_texts
        all_labels = ner_labels + synth_labels
        
        # Shuffle the combined dataset
        indices = np.random.permutation(len(all_texts))
        return [all_texts[i] for i in indices], [all_labels[i] for i in indices]
    
    def train(self):
        """Train the model on the combined dataset."""
        # Load and combine datasets
        texts, labels = self.combine_datasets()
        
        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42
        )
        
        # Vectorize the text data
        logger.info("Vectorizing text data...")
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        # Train the classifier
        logger.info("Training classifier...")
        self.classifier.fit(X_train_vec, y_train)
        
        # Evaluate the model
        y_pred = self.classifier.predict(X_test_vec)
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        
        # Save the model and vectorizer
        logger.info("Saving model and vectorizer...")
        joblib.dump(self.classifier, 'models/sensitive_detector_model.joblib')
        joblib.dump(self.vectorizer, 'models/text_vectorizer.joblib')
        
        return self.classifier, self.vectorizer

def main():
    trainer = CombinedDataTrainer()
    trainer.train()

if __name__ == "__main__":
    main() 