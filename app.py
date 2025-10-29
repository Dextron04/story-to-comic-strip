"""
Story to Comic Strip Generator - Web Application

Main entry point for running the web server.
Run this file to start the web application.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import the Flask app from backend
from backend.api import app

if __name__ == '__main__':
    # Check if API key is set
    if not os.getenv('GEMINI_API_KEY'):
        print("\n" + "=" * 70)
        print("WARNING: GEMINI_API_KEY environment variable is not set!")
        print("=" * 70)
        print("\nThe application will start, but comic generation will fail.")
        print("\nPlease set your API key:")
        print("1. Create a .env file in the project root with:")
        print("   GEMINI_API_KEY=your_api_key_here")
        print("2. Or export it in your terminal:")
        print("   export GEMINI_API_KEY=your_api_key_here")
        print("\nGet your API key from: https://makersuite.google.com/app/apikey")
        print("=" * 70 + "\n")

    print("\n" + "=" * 70)
    print("Story to Comic Strip Generator - Web Application")
    print("=" * 70)
    print("\nStarting server...")
    print("\nAccess the application at:")
    print("  Local:   http://localhost:5000")
    print("  Network: http://0.0.0.0:5000")
    print("\nPress CTRL+C to stop the server.")
    print("=" * 70 + "\n")

    # Run the Flask application
    app.run(
        debug=True,
        host='0.0.0.0',
        port=4000
    )
