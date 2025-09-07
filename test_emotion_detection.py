import unittest
from emotion_detection import emotion_detector

class TestEmotionDetection(unittest.TestCase):
    
    def test_emotion_detector_with_valid_text(self):
        """Test emotion detection with valid text."""
        result = emotion_detector("I am so happy today!")
        
        # Check that all expected keys are present
        expected_keys = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'dominant_emotion']
        for key in expected_keys:
            self.assertIn(key, result)
        
        # Check that joy is likely the dominant emotion for happy text
        self.assertIsNotNone(result['dominant_emotion'])
        self.assertIsInstance(result['joy'], float)
    
    def test_emotion_detector_with_empty_text(self):
        """Test emotion detection with empty text."""
        result = emotion_detector("")
        
        # All emotion scores should be None for empty text
        expected_keys = ['anger', 'disgust', 'fear', 'joy', 'sadness']
        for key in expected_keys:
            self.assertIsNone(result[key])
        
        self.assertIsNone(result['dominant_emotion'])
    
    def test_emotion_detector_with_angry_text(self):
        """Test emotion detection with angry text."""
        result = emotion_detector("I am so angry and furious right now!")
        
        # Check that result has valid structure
        self.assertIsNotNone(result['dominant_emotion'])
        self.assertIsInstance(result['anger'], float)
    
    def test_emotion_detector_with_sad_text(self):
        """Test emotion detection with sad text."""
        result = emotion_detector("I feel so sad and depressed today.")
        
        # Check that result has valid structure
        self.assertIsNotNone(result['dominant_emotion'])
        self.assertIsInstance(result['sadness'], float)
    
    def test_emotion_detector_response_format(self):
        """Test that emotion detector returns the correct format."""
        result = emotion_detector("This is a test message.")
        
        # Check response structure
        self.assertIsInstance(result, dict)
        
        expected_keys = ['anger', 'disgust', 'fear', 'joy', 'sadness', 'dominant_emotion']
        for key in expected_keys:
            self.assertIn(key, result)
        
        # If successful, scores should be floats or None
        if result['dominant_emotion'] is not None:
            for emotion in ['anger', 'disgust', 'fear', 'joy', 'sadness']:
                self.assertIsInstance(result[emotion], float)
                self.assertGreaterEqual(result[emotion], 0.0)
                self.assertLessEqual(result[emotion], 1.0)

if __name__ == '__main__':
    print("Running emotion detection tests...")
    unittest.main()