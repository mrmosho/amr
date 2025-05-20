from setuptools import setup, find_packages

setup(
    name="sensitive_data_detector",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        'scikit-learn==1.3.0',
        'spacy==3.7.2',
        'pandas==2.0.3',
        'numpy==1.24.3',
        'joblib==1.3.2',
        'Faker==22.6.0'
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A machine learning-based system for detecting sensitive information in text",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sensitive_data_detector",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
) 