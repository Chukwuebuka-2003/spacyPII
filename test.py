import re
import spacy
import json
import logging
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
    logging.info("spaCy model 'en_core_web_sm' loaded successfully.")
except OSError:
    logging.error("spaCy model 'en_core_web_sm' not found. Please run 'python -m spacy download en_core_web_sm'")
    exit()

# Define regex patterns
EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
API_KEY_REGEX = r"\bsk_test_[A-Za-z0-9]+\b"

def detect_pii(text: str) -> List[Dict]:
    """Detects PII in a given text."""
    doc = nlp(text)
    matches = []
    logging.info(f"Detecting PII in text: '{text}'")

    # spaCy NER for names
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            matches.append({
                "value": ent.text,
                "label": "NAME",
                "start": ent.start_char,
                "end": ent.end_char,
                "confidence": 0.95
            })
            logging.info(f"Found NAME: {ent.text}")

    # Regex for EMAIL
    for match in re.finditer(EMAIL_REGEX, text):
        matches.append({
            "value": match.group(),
            "label": "EMAIL",
            "start": match.start(),
            "end": match.end(),
            "confidence": 0.99
        })
        logging.info(f"Found EMAIL: {match.group()}")

    # Regex for API_KEY
    for match in re.finditer(API_KEY_REGEX, text):
        matches.append({
            "value": match.group(),
            "label": "API_KEY",
            "start": match.start(),
            "end": match.end(),
            "confidence": 0.97
        })
        logging.info(f"Found API_KEY: {match.group()}")

    return sorted(matches, key=lambda x: x['start'])

def generate_token_map(entities: List[Dict]) -> Dict:
    """Generates a map of tokens to PII entities."""
    pii_map = {}
    token_count = 1
    for ent in entities:
        token = f"__TOKEN_{token_count}__"
        pii_map[token] = {
            "value": ent['value'],
            "label": ent['label'],
            "confidence": ent['confidence']
        }
        token_count += 1
    logging.info(f"Generated PII map: {pii_map}")
    return pii_map

def mask_text(text: str, entities: List[Dict]) -> str:
    """Masks PII in a text with tokens."""
    masked_text = ""
    last_index = 0
    token_count = 1

    for ent in entities:
        start, end = ent['start'], ent['end']
        label = ent['label']
        token = f"__TOKEN_{token_count}__"
        token_label = f"[{label}:{token}]"

        masked_text += text[last_index:start]
        masked_text += token_label
        last_index = end
        token_count += 1

    masked_text += text[last_index:]
    logging.info(f"Masked text: '{masked_text}'")
    return masked_text

def process_input(text: str) -> Dict:
    """Processes input text to detect and mask PII."""
    logging.info("Starting PII detection and masking process.")
    entities = detect_pii(text)
    pii_map = generate_token_map(entities)
    masked_text = mask_text(text, entities)
    result = {
        "masked_text": masked_text,
        "pii_map": pii_map
    }
    logging.info("PII detection and masking process completed.")
    return result

if __name__ == "__main__":
    sample_text = "My name is Chukwuebuka and my email is ebulamicheal@gmail.com. Use API key sk_test_51XYZ to connect."
    result = process_input(sample_text)

    with open("sample_output.json", "w") as f:
        json.dump(result, f, indent=2)
        logging.info("Saved processing result to sample_output.json")

    print(json.dumps(result, indent=2))
