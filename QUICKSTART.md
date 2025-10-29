# Quick Start Guide

Get your Story to Comic Strip Generator up and running in minutes!

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- A Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## 5-Minute Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Configure API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 3: Run the Web Application

```bash
python app.py
```

### Step 4: Open Your Browser

Navigate to: **http://localhost:5000**

## Your First Comic Strip

1. **Try an Example**: Click one of the example story buttons (Knight's Quest, Space Explorer, or Mystery Detective)

2. **Or Write Your Own**: Type or paste your story in the text area

3. **Adjust Settings**: Use the slider to set the number of panels (3-15)

4. **Generate**: Click the "Generate Comic Strip" button

5. **View & Download**: Your comic strip will appear below, and you can download it as a text file

## Using the Python API

Want to use it programmatically? Here's a quick example:

```python
from story_to_comic import StoryToComicGenerator

# Initialize
generator = StoryToComicGenerator()

# Your story
story = """
Once upon a time, in a land far away, there lived a brave adventurer.
"I must find the legendary treasure," she said with determination.
And so, her epic journey began...
"""

# Generate comic
panels = generator.generate_comic(story, max_panels=5)

# Display results
for panel in panels:
    print(panel)
```

Run the examples:

```bash
python example.py
```

## Troubleshooting

### "No API key provided" error

Make sure:
- Your `.env` file exists in the project root
- The file contains: `GEMINI_API_KEY=your_key_here`
- There are no spaces around the `=` sign
- The API key is valid

### "Failed to generate comic" error

Check:
- Your internet connection is working
- The Gemini API key is valid and active
- You haven't exceeded API rate limits

### Port 5000 already in use

Change the port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Changed from 5000
```

## Next Steps

- Explore the Python API examples in `example.py`
- Customize the web interface styling in `frontend/static/css/style.css`
- Check out the full README for more features and options

## Need Help?

- Open an issue on GitHub
- Check the [Google Gemini API Documentation](https://ai.google.dev/docs)
- Read the full [README.md](README.md) for detailed information

Happy comic creating!
