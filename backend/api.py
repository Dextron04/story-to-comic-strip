"""
Backend API for Story to Comic Strip Generator

This module provides REST API endpoints for the comic generation service.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import sys

# Add parent directory to path to import story_to_comic module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from story_to_comic import StoryToComicGenerator

app = Flask(__name__,
            static_folder='../frontend/static',
            template_folder='../frontend/templates')
CORS(app)

# Initialize the generator (will be lazy-loaded when needed)
generator = None


def get_generator():
    """Lazy initialization of the comic generator."""
    global generator
    if generator is None:
        try:
            generator = StoryToComicGenerator()
        except ValueError as e:
            raise ValueError(f"Failed to initialize generator: {str(e)}")
    return generator


@app.route('/')
def index():
    """Serve the main frontend page."""
    return render_template('index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Story to Comic Strip Generator'
    })


@app.route('/api/generate', methods=['POST'])
def generate_comic():
    """
    Generate comic strip from story.

    Request JSON:
    {
        "story": "Your story text here...",
        "max_panels": 10  // optional, defaults to 10
    }

    Response JSON:
    {
        "success": true,
        "panels": [
            {
                "panel_number": 1,
                "scene": "Scene description",
                "dialogue": ["Character: dialogue"],
                "narration": "Optional narration"
            },
            ...
        ]
    }
    """
    try:
        # Get request data
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400

        story = data.get('story', '').strip()
        max_panels = data.get('max_panels', 10)

        # Validate input
        if not story:
            return jsonify({
                'success': False,
                'error': 'Story text is required'
            }), 400

        if len(story) < 10:
            return jsonify({
                'success': False,
                'error': 'Story is too short. Please provide a longer story.'
            }), 400

        if not isinstance(max_panels, int) or max_panels < 1 or max_panels > 20:
            return jsonify({
                'success': False,
                'error': 'max_panels must be an integer between 1 and 20'
            }), 400

        # Generate comic
        try:
            gen = get_generator()
            panels = gen.generate_comic(story, max_panels)

            # Convert panels to dictionary format
            panels_data = [panel.to_dict() for panel in panels]

            return jsonify({
                'success': True,
                'panels': panels_data,
                'total_panels': len(panels_data)
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to generate comic: {str(e)}'
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get configuration status."""
    api_key_set = bool(os.getenv('GEMINI_API_KEY'))

    return jsonify({
        'api_key_configured': api_key_set,
        'max_panels_limit': 20,
        'min_story_length': 10
    })


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        print("\n" + "=" * 70)
        print("WARNING: GEMINI_API_KEY environment variable is not set!")
        print("=" * 70)
        print("\nThe application will start, but comic generation will fail.")
        print("\nPlease set your API key:")
        print("1. Create a .env file with: GEMINI_API_KEY=your_api_key_here")
        print("2. Or export it: export GEMINI_API_KEY=your_api_key_here")
        print("\nGet your API key from: https://makersuite.google.com/app/apikey")
        print("=" * 70 + "\n")

    print("\nStarting Story to Comic Strip Generator Web Server...")
    print("Access the application at: http://localhost:5000")
    print("\nPress CTRL+C to stop the server.\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
