# Story to Comic Strip Generator

Transform your stories into engaging comic strips using the power of AI! This project leverages Google's Gemini API to automatically generate comic strip panels from written stories, bringing your narratives to life through visual storytelling.

## 🎯 Purpose

The **Story to Comic Strip Generator** is designed to:
- Convert written stories into visual comic strip format
- Generate comic panels with character dialogues and scene descriptions
- Provide an automated way to create visual narratives from text
- Utilize Google's Gemini API for intelligent story analysis and comic generation

## ✨ Features

- **Web Interface**: Beautiful, responsive web application for easy story-to-comic conversion
- **AI-Powered Story Analysis**: Uses Google Gemini API to understand story structure, characters, and scenes
- **Automatic Panel Generation**: Creates comic strip panels based on story content
- **Character Recognition**: Identifies and maintains character consistency across panels
- **Scene Visualization**: Generates appropriate visual descriptions for each story segment
- **Dialogue Extraction**: Automatically identifies and formats character dialogues for comic bubbles
- **Python API**: Use as a Python library for programmatic access

## 🚀 How It Works

1. **Input**: Provide a written story or narrative text
2. **Processing**: The system uses Google Gemini API to analyze the story structure
3. **Generation**: Creates comic strip panels with:
   - Scene descriptions
   - Character dialogues
   - Visual layout suggestions
4. **Output**: Delivers a structured comic strip format ready for visualization

## 🛠️ Requirements

- Google Gemini API access and API key
- Python 3.7+ (recommended)
- Internet connection for API calls

## 📋 Installation

1. Clone the repository:
```bash
git clone https://github.com/Dextron04/story-to-comic-strip.git
cd story-to-comic-strip
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Google Gemini API key:
```bash
# Create a .env file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_api_key_here
```

Or export it directly:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

Get your API key from: [Google AI Studio](https://makersuite.google.com/app/apikey)

## 💡 Usage

### Option 1: Web Application (Recommended)

The easiest way to use the Story to Comic Strip Generator is through the web interface:

1. Start the web server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Features of the web interface:
   - **Intuitive UI**: Clean, modern interface with a comic book theme
   - **Live Preview**: See your comic panels generate in real-time
   - **Example Stories**: Try pre-loaded example stories
   - **Adjustable Panels**: Control the number of comic panels (3-15)
   - **Download**: Export your comic strip as a text file
   - **Responsive Design**: Works on desktop, tablet, and mobile devices

### Option 2: Python API

```python
from story_to_comic import StoryToComicGenerator

# Initialize the generator
generator = StoryToComicGenerator(api_key="your_gemini_api_key")

# Generate comic strip from story
story = """
Once upon a time, there was a brave knight who embarked on a quest to save the kingdom.
"I must find the dragon's lair," said Sir Arthur.
The journey was long and treacherous, but his determination never wavered.
"""

comic_panels = generator.generate_comic(story)
print(comic_panels)
```

## 📖 Example Output

Input story gets transformed into structured comic panels:

```
Panel 1: [Scene: A castle courtyard at dawn]
Knight: "I must find the dragon's lair!"

Panel 2: [Scene: A winding forest path]
Narration: The journey was long and treacherous...

Panel 3: [Scene: Mountain cave entrance]
Knight: "At last, I've found it!"
```

## 📁 Project Structure

```
story-to-comic-strip/
├── app.py                      # Main entry point for web application
├── story_to_comic.py           # Core comic generation library
├── example.py                  # Python API usage examples
├── requirements.txt            # Project dependencies
├── .env.example               # Environment variables template
├── backend/
│   ├── __init__.py
│   └── api.py                 # Flask REST API
├── frontend/
│   ├── templates/
│   │   └── index.html         # Main web interface
│   └── static/
│       ├── css/
│       │   └── style.css      # Styles and themes
│       └── js/
│           └── app.js         # Frontend logic
└── README.md
```

## 🎨 Use Cases

- **Creative Writing**: Transform written stories into visual formats
- **Educational Content**: Create engaging comic strips for learning materials
- **Storytelling**: Convert narratives into comic book format
- **Content Creation**: Generate visual content from text-based stories
- **Prototyping**: Quick comic strip mockups for larger projects

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Comic Strip Creation Tools](https://example.com)
- [AI Story Generation](https://example.com)

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub or contact the maintainers.

---

**Made with ❤️ using Google Gemini API**