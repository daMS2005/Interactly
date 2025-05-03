# Extraction Folder
This folder contains Jupyter Notebooks and Python scripts for cleaning, transforming, and extracting data from raw input datasets. The processed data is prepared for tasks such as sentiment analysis, intent classification, and named entity recognition (NER).

## Contents

### Notebooks

1. **Product_NER_Dataset_Cleaning.ipynb**
   - Cleans and processes the Product NER dataset.
   - Filters annotations to retain only relevant metadata categories (`meta`, `meta_brand`, `meta_model`).
   - Prepares the dataset for training by aligning BIO labels with tokenized text.
   - Saves the processed data as CSV and PyTorch tensors.

2. **Extract_Sentiment.ipynb**
   - Extracts and processes sentiment data from customer reviews.
   - Samples balanced subsets of reviews based on sentiment scores.
   - Saves the cleaned data for sentiment analysis.

3. **Extract_Intent.ipynb**
   - Cleans and processes the Customer Service dataset for intent classification.
   - Filters specific categories (`PAYMENT`, `FEEDBACK`, `CONTACT`, `REFUND`).
   - Renames columns and saves the cleaned dataset for training.

4. **Customer_Service_dataset_Cleaning.ipynb**
   - Cleans the Customer Service Training Dataset.
   - Removes duplicates, handles missing values, and tokenizes text for BERT-based models.
   - Encodes intents and categories as numerical labels.
   - Saves the final processed dataset for training.

### Scripts

1. **FeatureExtract.py**
   - Analyzes features of the processed datasets.
   - Provides insights into token distributions, label distributions, and dataset statistics.

### Additional Files

- **dataset_links.txt**
  - Contains links to external datasets used for training and evaluation.

## Usage

1. Open the Jupyter Notebooks to explore and execute the data cleaning and extraction workflows.
2. Use the `FeatureExtract.py` script to analyze the processed datasets.
3. Refer to the `dataset_links.txt` file for additional dataset sources.

## Output

- Cleaned datasets are saved in the `Cleaned_Data` directory.
- Processed data is ready for use in downstream tasks such as model training and evaluation.
