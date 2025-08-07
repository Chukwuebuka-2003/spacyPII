import unittest
import json
from test import detect_pii, generate_token_map, mask_text, process_input

class TestPiiDetection(unittest.TestCase):

    def setUp(self):
        self.sample_text = "My name is Chukwuebuka and my email is ebulamicheal@gmail.com. Use API key sk_test_51XYZ to connect."
        self.entities = [
            {'value': 'Chukwuebuka', 'label': 'NAME', 'start': 11, 'end': 22, 'confidence': 0.95},
            {'value': 'ebulamicheal@gmail.com', 'label': 'EMAIL', 'start': 39, 'end': 61, 'confidence': 0.99},
            {'value': 'sk_test_51XYZ', 'label': 'API_KEY', 'start': 75, 'end': 88, 'confidence': 0.97}
        ]

    def test_detect_pii(self):
        detected_entities = detect_pii(self.sample_text)
        # Sort by start position to ensure consistent order for comparison
        detected_entities.sort(key=lambda x: x['start'])
        self.assertEqual(detected_entities, self.entities)

    def test_generate_token_map(self):
        pii_map = generate_token_map(self.entities)
        expected_map = {
            "__TOKEN_1__": {"value": "Chukwuebuka", "label": "NAME", "confidence": 0.95},
            "__TOKEN_2__": {"value": "ebulamicheal@gmail.com", "label": "EMAIL", "confidence": 0.99},
            "__TOKEN_3__": {"value": "sk_test_51XYZ", "label": "API_KEY", "confidence": 0.97}
        }
        self.assertEqual(pii_map, expected_map)

    def test_mask_text(self):
        masked_text = mask_text(self.sample_text, self.entities)
        expected_masked_text = "My name is [NAME:__TOKEN_1__] and my email is [EMAIL:__TOKEN_2__]. Use API key [API_KEY:__TOKEN_3__] to connect."
        self.assertEqual(masked_text, expected_masked_text)

    def test_process_input(self):
        result = process_input(self.sample_text)
        expected_result = {
            "masked_text": "My name is [NAME:__TOKEN_1__] and my email is [EMAIL:__TOKEN_2__]. Use API key [API_KEY:__TOKEN_3__] to connect.",
            "pii_map": {
                "__TOKEN_1__": {"value": "Chukwuebuka", "label": "NAME", "confidence": 0.95},
                "__TOKEN_2__": {"value": "ebulamicheal@gmail.com", "label": "EMAIL", "confidence": 0.99},
                "__TOKEN_3__": {"value": "sk_test_51XYZ", "label": "API_KEY", "confidence": 0.97}
            }
        }

        self.assertEqual(json.loads(json.dumps(result)), json.loads(json.dumps(expected_result)))

if __name__ == '__main__':
    unittest.main()
