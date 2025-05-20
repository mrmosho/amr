# Sensitive Data Detection System

A comprehensive machine learning-based system for detecting sensitive information in text using both rule-based and ML approaches. This system combines natural language processing (NLP) with machine learning to identify various types of sensitive data.

## Features

- **Multi-Approach Detection**:
  - Machine Learning-based classification
  - Named Entity Recognition (NER)
  - Pattern-based detection
  - Rule-based validation

- **Sensitive Data Types Detected**:
  - Personal names
  - Email addresses
  - Phone numbers
  - Credit card numbers
  - Social Security Numbers
  - Physical addresses
  - Organizations
  - Locations
  - Passwords

- **Advanced Features**:
  - Confidence scoring
  - Entity recognition
  - Batch processing
  - Detailed detection summaries
  - Comprehensive logging

## Installation

1. **Install the Package**:
   ```bash
   pip install -e .
   ```

2. **Download Required Models**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Verify Model Files**:
   Ensure these files are present in the `models` directory:
   - `sensitive_detector_model.joblib`
   - `text_vectorizer.joblib`

## Quick Start

```python
from sensitive_data_detector import SensitiveDataDetector

# Initialize the detector
detector = SensitiveDataDetector(
    model_path='models/sensitive_detector_model.joblib',
    vectorizer_path='models/text_vectorizer.joblib'
)

# Single text detection
text = "My email is john.doe@example.com"
result = detector.detect(text)

# Get detailed summary
summary = detector.get_sensitive_summary(result)
print(summary)

# Batch processing
texts = [
    "My email is john.doe@example.com",
    "The weather is nice today",
    "Contact me at 123-456-7890"
]
results = detector.batch_detect(texts)
```

## Project Structure

```
sensitive_data_detector/
├── setup.py                 # Package installation configuration
├── README.md               # This documentation
├── requirements.txt        # Package dependencies
├── sensitive_data_detector/
│   ├── __init__.py        # Package initialization
│   └── detector.py        # Main detection module
├── scripts/
│   ├── train_combined.py  # Training script
│   └── generate_synthetic_data.py  # Data generation script
├── data/                   # Data directory
│   ├── ner_dataset.csv    # NER training data
│   └── synthetic_sensitive_data.csv  # Synthetic training data
└── models/                 # Model directory
    ├── sensitive_detector_model.joblib    # Trained model
    └── text_vectorizer.joblib            # Text vectorizer
```

## Usage Examples

### Basic Detection
```python
detector = SensitiveDataDetector()
result = detector.detect("My SSN is 123-45-6789")
print(f"Is sensitive: {result.is_sensitive}")
print(f"Confidence: {result.confidence}")
print(f"Type: {result.sensitive_type}")
```

### Batch Processing
```python
texts = [
    "Contact: John Doe, Email: john@example.com",
    "The meeting is at 2 PM",
    "Card number: 4111-1111-1111-1111"
]
results = detector.batch_detect(texts)
```

### Getting Detailed Information
```python
result = detector.detect("My email is test@example.com")
summary = detector.get_sensitive_summary(result)
print(summary)
```

## DetectionResult Object

The `detect()` method returns a `DetectionResult` object with:

- `is_sensitive`: Boolean indicating if sensitive data was found
- `confidence`: Confidence score (0-1)
- `entities`: List of named entities found
- `sensitive_type`: Type of sensitive data
- `sensitive_value`: The actual sensitive value found

## Training Your Own Model

1. **Generate Synthetic Data**:
   ```bash
   python scripts/generate_synthetic_data.py
   ```

2. **Train the Model**:
   ```bash
   python scripts/train_combined.py
   ```

## Requirements

- Python >= 3.8
- scikit-learn==1.3.0
- spacy==3.7.2
- pandas==2.0.3
- numpy==1.24.3
- joblib==1.3.2
- Faker==22.6.0

## Development

### Adding New Detection Types
1. Modify the detection patterns in `detector.py`
2. Add new training data
3. Retrain the model

### Customizing the Model
1. Adjust parameters in `train_combined.py`
2. Modify feature extraction in `detector.py`
3. Add new training data types

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## Support

For issues and feature requests, please create an issue in the repository. 