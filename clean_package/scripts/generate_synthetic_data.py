import pandas as pd
from faker import Faker
import random
import logging
from typing import List, Tuple
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SyntheticDataGenerator:
    def __init__(self, num_samples: int = 10000):
        self.fake = Faker()
        self.num_samples = num_samples
        
    def generate_sensitive_text(self) -> Tuple[str, bool]:
        """Generate a text containing sensitive information."""
        templates = [
            # Credit card templates
            "My credit card number is {cc}",
            "Please charge {cc} to my card",
            "Card ending in {cc_last4}",
            "Visa card: {cc}",
            
            # Email templates
            "Contact me at {email}",
            "Send the report to {email}",
            "My email address is {email}",
            
            # Phone number templates
            "Call me at {phone}",
            "My mobile number is {phone}",
            "Contact number: {phone}",
            
            # Address templates
            "I live at {address}",
            "Shipping address: {address}",
            "Billing address: {address}",
            
            # SSN templates
            "My SSN is {ssn}",
            "Social Security Number: {ssn}",
            
            # Password templates
            "Password: {password}",
            "Login credentials: admin/{password}",
            "My password is {password}",
            
            # Combined templates
            "Name: {name}, Email: {email}, Phone: {phone}",
            "Contact: {name}, Address: {address}, Card: {cc}",
            "Profile: {name}, SSN: {ssn}, Email: {email}"
        ]
        
        # Generate random number of sensitive fields (1-3)
        num_fields = random.randint(1, 3)
        template = random.choice(templates)
        
        # Fill template with fake data
        text = template.format(
            cc=self.fake.credit_card_number(),
            cc_last4=self.fake.credit_card_number()[-4:],
            email=self.fake.email(),
            phone=self.fake.phone_number(),
            address=self.fake.address(),
            ssn=self.fake.ssn(),
            password=self.fake.password(),
            name=self.fake.name()
        )
        
        return text, True
    
    def generate_non_sensitive_text(self) -> Tuple[str, bool]:
        """Generate a text without sensitive information."""
        templates = [
            "The weather is nice today",
            "I went to the store",
            "The movie was great",
            "Let's meet for lunch",
            "The project is going well",
            "I love reading books",
            "The food was delicious",
            "The concert was amazing",
            "I enjoy hiking",
            "The game was exciting",
            "The book was interesting",
            "The show was entertaining",
            "I like to travel",
            "The park is beautiful",
            "The music was relaxing"
        ]
        
        # Sometimes combine multiple non-sensitive sentences
        num_sentences = random.randint(1, 3)
        text = " ".join(random.sample(templates, num_sentences))
        
        return text, False
    
    def generate_dataset(self) -> Tuple[List[str], List[bool]]:
        """Generate a balanced dataset of sensitive and non-sensitive texts."""
        texts = []
        labels = []
        
        # Generate equal number of sensitive and non-sensitive samples
        num_sensitive = self.num_samples // 2
        num_non_sensitive = self.num_samples - num_sensitive
        
        logger.info(f"Generating {num_sensitive} sensitive samples...")
        for _ in range(num_sensitive):
            text, label = self.generate_sensitive_text()
            texts.append(text)
            labels.append(label)
        
        logger.info(f"Generating {num_non_sensitive} non-sensitive samples...")
        for _ in range(num_non_sensitive):
            text, label = self.generate_non_sensitive_text()
            texts.append(text)
            labels.append(label)
        
        # Shuffle the dataset
        combined = list(zip(texts, labels))
        random.shuffle(combined)
        texts, labels = zip(*combined)
        
        return list(texts), list(labels)

def main():
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Generate synthetic dataset
    generator = SyntheticDataGenerator(num_samples=10000)
    texts, labels = generator.generate_dataset()
    
    # Create DataFrame
    df = pd.DataFrame({
        'text': texts,
        'is_sensitive': labels
    })
    
    # Save to CSV
    output_file = 'data/synthetic_sensitive_data.csv'
    df.to_csv(output_file, index=False)
    logger.info(f"Generated dataset saved to {output_file}")
    
    # Print some statistics
    num_sensitive = sum(labels)
    num_non_sensitive = len(labels) - num_sensitive
    logger.info(f"Total samples: {len(texts)}")
    logger.info(f"Sensitive samples: {num_sensitive}")
    logger.info(f"Non-sensitive samples: {num_non_sensitive}")
    
    # Print some examples
    print("\nExample sensitive texts:")
    sensitive_examples = df[df['is_sensitive']].head(3)
    for _, row in sensitive_examples.iterrows():
        print(f"- {row['text']}")
    
    print("\nExample non-sensitive texts:")
    non_sensitive_examples = df[~df['is_sensitive']].head(3)
    for _, row in non_sensitive_examples.iterrows():
        print(f"- {row['text']}")

if __name__ == "__main__":
    main() 