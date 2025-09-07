from flask import Flask, render_template, request, jsonify
from emotion_detection import emotion_detector
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask("Emotion Detector")

@app.route("/emotionDetector", methods=['GET', 'POST'])
def emotion_detector_route():
    """Route for emotion detection analysis."""
    if request.method == 'POST':
        text_to_analyze = request.form.get('text')
    else:
        text_to_analyze = request.args.get('textToAnalyze')
    
    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid text! Please try again!"
    
    try:
        response = emotion_detector(text_to_analyze)
        
        # Check if there was an error in emotion detection
        if 'error' in response or response['dominant_emotion'] is None:
            logger.warning(f"Error in emotion detection: {response.get('error', 'Unknown error')}")
            return "Invalid text! Please try again!"
        
        # Format response string
        emotion_text = (
            f"For the given statement, the system response is "
            f"'anger': {response['anger']}, "
            f"'disgust': {response['disgust']}, "
            f"'fear': {response['fear']}, "
            f"'joy': {response['joy']}, "
            f"'sadness': {response['sadness']}. "
            f"The dominant emotion is {response['dominant_emotion']}."
        )
        
        logger.info(f"Successfully processed emotion detection for text: {text_to_analyze[:50]}...")
        return emotion_text
        
    except Exception as e:
        logger.error(f"Unexpected error in emotion detection route: {e}")
        return "An error occurred while processing your request. Please try again!"

@app.route("/api/emotionDetector", methods=['POST'])
def emotion_detector_api():
    """API endpoint for emotion detection (JSON response)."""
    try:
        data = request.get_json()
        text_to_analyze = data.get('text', '') if data else ''
        
        if not text_to_analyze or not text_to_analyze.strip():
            return jsonify({
                'error': 'Invalid or empty text provided'
            }), 400
        
        response = emotion_detector(text_to_analyze)
        
        if 'error' in response or response['dominant_emotion'] is None:
            return jsonify({
                'error': response.get('error', 'Failed to analyze emotions')
            }), 400
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in API endpoint: {e}")
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500

@app.route("/")
def render_index_page():
    """Render the main page."""
    return render_template('index.html')

@app.route("/health")
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Emotion Detector',
        'version': '2.0.0'
    })

if __name__ == "__main__":
    logger.info("Starting Emotion Detector application...")
    app.run(host="0.0.0.0", port=5000, debug=True)