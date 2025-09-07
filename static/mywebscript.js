function runSentimentAnalysis(event) {
    event.preventDefault();
    
    const textToAnalyze = document.getElementById('textToAnalyze').value.trim();
    const analyzeBtn = document.getElementById('analyzeBtn');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    
    // Hide previous results
    resultDiv.classList.remove('show');
    errorDiv.style.display = 'none';
    
    if (!textToAnalyze) {
        showError('Please enter some text to analyze.');
        return;
    }
    
    // Show loading state
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = '🔄 Analyzing...';
    
    // Make request to emotion detector
    const url = `/emotionDetector?textToAnalyze=${encodeURIComponent(textToAnalyze)}`;
    
    fetch(url)
        .then(response => response.text())
        .then(data => {
            if (data.includes('Invalid text!') || data.includes('error')) {
                showError('Unable to analyze the provided text. Please try different text.');
            } else {
                parseAndDisplayResults(data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('An error occurred while analyzing the text. Please try again.');
        })
        .finally(() => {
            // Reset button state
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = '🔍 Analyze Emotions';
        });
}

function parseAndDisplayResults(responseText) {
    try {
        // Parse the response text to extract emotion scores
        const emotions = {};
        let dominantEmotion = '';
        
        // Extract emotion scores using regex
        const emotionRegex = /'(\w+)': ([\d.]+)/g;
        let match;
        while ((match = emotionRegex.exec(responseText)) !== null) {
            emotions[match[1]] = parseFloat(match[2]);
        }
        
        // Extract dominant emotion
        const dominantMatch = responseText.match(/The dominant emotion is (\w+)/);
        if (dominantMatch) {
            dominantEmotion = dominantMatch[1];
        }
        
        if (Object.keys(emotions).length > 0) {
            displayResults(emotions, dominantEmotion);
        } else {
            showError('Unable to parse emotion analysis results.');
        }
    } catch (error) {
        console.error('Parsing error:', error);
        showError('Error processing the analysis results.');
    }
}

function displayResults(emotions, dominantEmotion) {
    const emotionsDiv = document.getElementById('emotions');
    const dominantDiv = document.getElementById('dominant');
    const resultDiv = document.getElementById('result');
    
    // Clear previous results
    emotionsDiv.innerHTML = '';
    
    // Emotion emojis
    const emotionEmojis = {
        'anger': '😠',
        'disgust': '🤢',
        'fear': '😨',
        'joy': '😊',
        'sadness': '😢'
    };
    
    // Display each emotion
    for (const [emotion, score] of Object.entries(emotions)) {
        const emotionItem = document.createElement('div');
        emotionItem.className = 'emotion-item';
        if (emotion === dominantEmotion) {
            emotionItem.classList.add('dominant');
        }
        
        emotionItem.innerHTML = `
            <div class="emotion-name">
                ${emotionEmojis[emotion] || '🎭'} ${emotion.charAt(0).toUpperCase() + emotion.slice(1)}
            </div>
            <div class="emotion-score">${(score * 100).toFixed(1)}%</div>
        `;
        
        emotionsDiv.appendChild(emotionItem);
    }
    
    // Display dominant emotion
    dominantDiv.innerHTML = `
        <strong>🏆 Dominant Emotion: ${emotionEmojis[dominantEmotion] || '🎭'} ${dominantEmotion.charAt(0).toUpperCase() + dominantEmotion.slice(1)}</strong>
    `;
    
    // Show results
    resultDiv.classList.add('show');
}

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
}

// Add some example texts for quick testing
document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.getElementById('textToAnalyze');
    
    // Add placeholder examples
    const examples = [
        "I am so happy today! The weather is beautiful and everything is going perfectly.",
        "This makes me really angry and frustrated. I can't believe this happened!",
        "I'm feeling quite sad and lonely today. Nothing seems to be going right.",
        "That movie was absolutely disgusting. I couldn't watch it anymore.",
        "I'm so scared about the upcoming exam. What if I fail?"
    ];
    
    let exampleIndex = 0;
    textarea.addEventListener('focus', function() {
        if (!this.value) {
            this.placeholder = examples[exampleIndex];
            exampleIndex = (exampleIndex + 1) % examples.length;
        }
    });
});