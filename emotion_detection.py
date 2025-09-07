from transformers import pipeline
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmotionDetector:
    def __init__(self):
        """Initialize the emotion detection pipeline."""
        try:
            # Using a robust emotion classification model
            self.emotion_pipeline = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                top_k=None
            )
            logger.info("Emotion detection model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading emotion detection model: {e}")
            self.emotion_pipeline = None

    def detect_emotions(self, text):
        """
        Detect emotions in the given text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Dictionary containing emotion scores and dominant emotion
        """
        if not text or not text.strip():
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None,
                'error': 'Invalid or empty text provided'
            }
        
        if self.emotion_pipeline is None:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None,
                'error': 'Emotion detection model not available'
            }
        
        try:
            # Get emotion predictions
            predictions = self.emotion_pipeline(text)
            
            # Initialize emotion scores
            emotions = {
                'anger': 0.0,
                'disgust': 0.0,
                'fear': 0.0,
                'joy': 0.0,
                'sadness': 0.0
            }
            
            # Map model labels to our emotion categories
            label_mapping = {
                'anger': 'anger',
                'disgust': 'disgust',
                'fear': 'fear',
                'joy': 'joy',
                'happiness': 'joy',  # Alternative mapping
                'sadness': 'sadness',
                'surprise': 'joy',   # Map surprise to joy for compatibility
                'love': 'joy'        # Map love to joy for compatibility
            }
            
            # Process predictions
            for prediction in predictions:
                label = prediction['label'].lower()
                score = prediction['score']
                
                if label in label_mapping:
                    mapped_emotion = label_mapping[label]
                    emotions[mapped_emotion] = max(emotions[mapped_emotion], score)
            
            # Find dominant emotion
            dominant_emotion = max(emotions, key=emotions.get)
            
            # Round scores to 6 decimal places for consistency
            for emotion in emotions:
                emotions[emotion] = round(emotions[emotion], 6)
            
            result = {
                'anger': emotions['anger'],
                'disgust': emotions['disgust'],
                'fear': emotions['fear'],
                'joy': emotions['joy'],
                'sadness': emotions['sadness'],
                'dominant_emotion': dominant_emotion
            }
            
            logger.info(f"Successfully analyzed text: {text[:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"Error during emotion detection: {e}")
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None,
                'error': f'Error processing text: {str(e)}'
            }

# Global detector instance
_detector = None

def get_detector():
    """Get or create the global detector instance."""
    global _detector
    if _detector is None:
        _detector = EmotionDetector()
    return _detector

def emotion_detector(text_to_analyse):
    """
    Main function for emotion detection (maintains compatibility with existing code).
    
    Args:
        text_to_analyse (str): Text to analyze
        
    Returns:
        dict: Dictionary containing emotion scores and dominant emotion
    """
    detector = get_detector()
    return detector.detect_emotions(text_to_analyse)