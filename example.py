"""
Example usage of the Story to Comic Strip Generator

This script demonstrates how to use the StoryToComicGenerator to convert
stories into comic strip format.
"""

from story_to_comic import StoryToComicGenerator, story_to_comic
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def example_1_basic_usage():
    """Example 1: Basic usage with the StoryToComicGenerator class"""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 70 + "\n")

    # Initialize the generator with API key from environment
    try:
        generator = StoryToComicGenerator()

        # Your story
        story = """
        Once upon a time, there was a brave knight named Sir Arthur who embarked on a quest to save the kingdom from a fearsome dragon.
        "I must find the dragon's lair," said Sir Arthur as he prepared his sword and shield.
        The journey was long and treacherous. He traveled through dark forests and crossed raging rivers.
        After many days, Sir Arthur finally reached the mountain where the dragon lived.
        "At last, I've found it!" he exclaimed, looking up at the smoking cave entrance.
        The dragon emerged with a mighty roar. "Who dares enter my domain?" it bellowed.
        "I am Sir Arthur, and I've come to free the kingdom from your terror!" the knight replied bravely.
        After a fierce battle, Sir Arthur discovered the dragon was only angry because a thorn was stuck in its foot.
        "Let me help you," said Sir Arthur, and he carefully removed the thorn.
        "Thank you, kind knight," said the dragon. "I will trouble the kingdom no more."
        And so, Sir Arthur returned home as a hero, having won not through violence, but through compassion.
        """

        # Generate comic strip
        print("Generating comic strip from story...\n")
        result = generator.generate_comic_text(story, max_panels=8)

        print(result)

    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease make sure to set your GEMINI_API_KEY environment variable.")
        print("You can do this by:")
        print("1. Creating a .env file with: GEMINI_API_KEY=your_api_key_here")
        print("2. Or exporting it: export GEMINI_API_KEY=your_api_key_here")


def example_2_quick_function():
    """Example 2: Using the convenience function"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Using Convenience Function")
    print("=" * 70 + "\n")

    story = """
    In a small village lived a curious girl named Luna who loved to explore.
    One day, she discovered a mysterious glowing door in the old library.
    "What could be behind this?" Luna wondered as she slowly pushed it open.
    Behind the door was a magical garden filled with talking flowers and singing birds.
    "Welcome, Luna!" said a wise old oak tree. "We've been waiting for you."
    Luna spent the day learning about the magic of nature and friendship.
    When evening came, she returned home, knowing she had found something special.
    """

    try:
        result = story_to_comic(story, max_panels=5)
        print(result)

    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease set your GEMINI_API_KEY environment variable.")


def example_3_detailed_output():
    """Example 3: Working with panel objects directly"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Working with Panel Objects")
    print("=" * 70 + "\n")

    story = """
    Detective Sarah Chen examined the crime scene carefully.
    "The window was broken from the inside," she noted.
    Her partner, Detective Mike Rodriguez, found a mysterious letter.
    "Sarah, you need to see this," he said urgently.
    The letter contained a cryptic message that would change everything.
    """

    try:
        generator = StoryToComicGenerator()

        # Generate panels
        panels = generator.generate_comic(story, max_panels=4)

        print(f"Generated {len(panels)} panels:\n")

        for panel in panels:
            print(f"\nPanel {panel.panel_number}:")
            print(f"  Scene: {panel.scene}")
            if panel.narration:
                print(f"  Narration: {panel.narration}")
            print(f"  Dialogues: {len(panel.dialogue)}")
            for dialogue in panel.dialogue:
                print(f"    - {dialogue}")

            # You can also get panel as dictionary
            panel_dict = panel.to_dict()
            print(f"  Panel data structure: {panel_dict.keys()}")

    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease set your GEMINI_API_KEY environment variable.")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("STORY TO COMIC STRIP GENERATOR - EXAMPLES")
    print("=" * 70)

    # Check if API key is available
    if not os.getenv("GEMINI_API_KEY"):
        print("\nWARNING: GEMINI_API_KEY environment variable is not set!")
        print("\nPlease set your API key before running these examples:")
        print("1. Create a .env file in the project root with:")
        print("   GEMINI_API_KEY=your_api_key_here")
        print("2. Or export it in your terminal:")
        print("   export GEMINI_API_KEY=your_api_key_here")
        print("\nGet your API key from: https://makersuite.google.com/app/apikey")
        return

    # Run examples
    example_1_basic_usage()
    example_2_quick_function()
    example_3_detailed_output()

    print("\n" + "=" * 70)
    print("Examples completed!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
