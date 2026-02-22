from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from news_verifier import NewsVerifier
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the news verifier
verifier = NewsVerifier()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/verify', methods=['POST'])
def verify_news():
    """API endpoint to verify news"""
    try:
        data = request.get_json()
        user_input = data.get('news_text', '').strip()
        
        if not user_input:
            return jsonify({
                'error': 'Please enter some news text to verify'
            }), 400
        
        if len(user_input) < 10:
            return jsonify({
                'error': 'Please enter at least 10 characters for better verification'
            }), 400
        
        logger.info(f"Verifying news: {user_input[:100]}...")
        
        # Verify the news
        result = verifier.verify_news(user_input)
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in verify_news: {str(e)}")
        return jsonify({'error': 'An internal error occurred. Please try again.'}), 500

@app.route('/api/feeds', methods=['GET'])
def get_feeds():
    """Get list of available RSS feeds"""
    return jsonify({
        'feeds': list(verifier.rss_feeds.keys()),
        'total_sources': len(verifier.rss_feeds)
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Fake News Verification System is running'
    })

if __name__ == '__main__':
    logger.info("Starting Fake News Verification System...")
    app.run(debug=True, port=5000, host='0.0.0.0')