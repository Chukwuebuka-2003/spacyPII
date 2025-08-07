# spacyPII

## PII Detection and Masking

### Approach

This project implements a Personal Identifiable Information (PII) detection and masking system. It utilizes a hybrid approach combining:

-   **spaCy's Named Entity Recognition (NER)**: Specifically, the `en_core_web_sm` model is used to identify "PERSON" entities, which are treated as names.
-   **Regular Expressions**: Custom regex patterns are defined to detect "EMAIL" and "API_KEY" PII.

The `detect_pii` function identifies all PII entities in the input text, returning a list of dictionaries with their values, labels, start and end indices, and a confidence score. The `mask_text` function then takes the original text and the detected entities to produce a masked version of the text, replacing PII with unique tokens (e.g., `__TOKEN_1__`). A `pii_map` is also generated, linking these tokens back to the original PII values and their labels.

### How to run the code

1.  **Install spaCy model**:
    ```bash
    python -m spacy download en_core_web_sm
    ```
2.  **Run the `test.py` script**:
    ```bash
    python test.py
    ```
    This script will process a sample text, detect PII, mask it, and save the result to `sample_output.json`. It will also print the result to the console.

### PII Labels Handled

The following PII labels are currently handled:

-   **NAME**: Detected using spaCy's NER for "PERSON" entities.
-   **EMAIL**: Detected using a regular expression for common email formats.
-   **API_KEY**: Detected using a regular expression specifically for patterns like `sk_test_...`.

### Tool Used: spaCy

I chose to use spaCy for its robust Named Entity Recognition capabilities. While Hugging Face offers a wide range of pre-trained models, spaCy's `en_core_web_sm` model provides efficient and accurate "PERSON" entity recognition out-of-the-box, which is crucial for identifying names. For other PII types like email and API keys, regular expressions were deemed more suitable due to their precision and simplicity for these specific patterns, complementing spaCy's NER.
