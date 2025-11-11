"""
Story to Comic Strip Generator

This module provides functionality to convert written stories into comic strip panels
using Google's Gemini API for intelligent story analysis and comic generation with images.
"""

import os
import re
import base64
import time
from typing import List, Dict, Optional
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from google import genai
from google.genai import types


class ComicPanel:
    """Represents a single comic strip panel."""

    def __init__(self, panel_number: int, scene: str, dialogue: List[str],
                 narration: Optional[str] = None, image_prompt: Optional[str] = None,
                 image_data: Optional[str] = None):
        """
        Initialize a comic panel.

        Args:
            panel_number: The sequence number of the panel
            scene: Description of the scene/visual setting
            dialogue: List of character dialogues
            narration: Optional narration text
            image_prompt: Prompt used to generate the image
            image_data: Base64 encoded image data
        """
        self.panel_number = panel_number
        self.scene = scene
        self.dialogue = dialogue
        self.narration = narration
        self.image_prompt = image_prompt
        self.image_data = image_data

    def __str__(self) -> str:
        """Return a formatted string representation of the panel."""
        output = f"Panel {self.panel_number}: [Scene: {self.scene}]\n"

        if self.narration:
            output += f"Narration: {self.narration}\n"

        for line in self.dialogue:
            output += f"{line}\n"

        if self.image_prompt:
            output += f"Image: Generated from prompt\n"

        return output.strip()

    def to_dict(self) -> Dict:
        """Convert panel to dictionary format."""
        return {
            "panel_number": self.panel_number,
            "scene": self.scene,
            "dialogue": self.dialogue,
            "narration": self.narration,
            "image_prompt": self.image_prompt,
            "image_data": self.image_data
        }


class StoryToComicGenerator:
    """Main class for generating comic strips from stories using Google Gemini API with image generation."""

    def __init__(self, api_key: Optional[str] = None, generate_images: bool = True):
        """
        Initialize the Story to Comic Generator.

        Args:
            api_key: Google Gemini API key. If not provided, will try to read from
                    GEMINI_API_KEY environment variable.
            generate_images: Whether to generate images for panels (default: True)

        Raises:
            ValueError: If no API key is provided or found in environment.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.generate_images = generate_images

        if not self.api_key:
            raise ValueError(
                "No API key provided. Please provide an API key or set the "
                "GEMINI_API_KEY environment variable."
            )

        # Configure the Gemini API using the new client
        self.client = genai.Client(api_key=self.api_key)
        
        # For text generation, we'll use the client's models
        self.text_model_name = 'gemini-2.0-flash-exp'
        
        # Image generation model
        self.image_model_name = 'imagen-4.0-generate-001'
        self.image_generation_available = True

    def generate_comic(self, story: str, max_panels: int = 10) -> List[ComicPanel]:
        """
        Generate comic strip panels from a story with images.

        Args:
            story: The story text to convert into comic panels
            max_panels: Maximum number of panels to generate (default: 10)

        Returns:
            List of ComicPanel objects representing the comic strip with images

        Raises:
            Exception: If the API call fails or response cannot be parsed
        """
        # Create a detailed prompt for the Gemini API
        prompt = self._create_comic_generation_prompt(story, max_panels)

        try:
            # Generate content using Gemini
            response = self.client.models.generate_content(
                model=self.text_model_name,
                contents=prompt
            )

            # Parse the response into comic panels
            panels = self._parse_comic_response(response.text)

            # Generate images for each panel if enabled
            if self.generate_images:
                panels = self._generate_panel_images(panels)

            return panels

        except Exception as e:
            raise Exception(f"Failed to generate comic: {str(e)}")

    def _create_comic_generation_prompt(self, story: str, max_panels: int) -> str:
        """Create a detailed prompt for the Gemini API."""
        prompt = f"""You are an expert comic strip creator. Analyze the following story and convert it into a comic strip format with up to {max_panels} panels.

For each panel, provide:
1. A scene description (visual setting and atmosphere)
2. An image generation prompt (detailed, visual description for creating the artwork)
3. Character dialogues (if any) in the format "Character Name: dialogue"
4. Narration text (if needed for context)

Format your response exactly like this for each panel:

PANEL [number]
SCENE: [Brief scene description]
IMAGE_PROMPT: [Detailed visual description for image generation - include art style (comic book art, vibrant colors, bold outlines), character descriptions, setting details, lighting, mood, and composition. Make it very detailed and specific for generating artwork.]
DIALOGUE:
- [Character Name]: "[Their dialogue]"
- [Character Name]: "[Their dialogue]"
NARRATION: [Optional narration text]

Story to convert:
{story}

Important: For IMAGE_PROMPT, create detailed, vivid descriptions that would work well for AI image generation. Include:
- Art style: "Comic book style art with bold black outlines and vibrant colors"
- Characters: Physical appearance, clothing, expressions, poses
- Setting: Environment details, time of day, atmosphere
- Composition: Camera angle, foreground/background elements
- Mood: Overall feeling and lighting

Please create engaging, visually descriptive comic panels that capture the key moments and emotions of the story."""

        return prompt

    def _parse_comic_response(self, response_text: str) -> List[ComicPanel]:
        """
        Parse the Gemini API response into ComicPanel objects.

        Args:
            response_text: The raw text response from Gemini API

        Returns:
            List of ComicPanel objects
        """
        panels = []

        # Split response into individual panels
        panel_sections = re.split(r'PANEL\s+(\d+)', response_text)

        # Skip the first element (text before first panel)
        for i in range(1, len(panel_sections), 2):
            if i + 1 >= len(panel_sections):
                break

            panel_num = int(panel_sections[i])
            panel_content = panel_sections[i + 1]

            # Extract scene
            scene_match = re.search(r'SCENE:\s*(.+?)(?:\n|$)', panel_content, re.IGNORECASE)
            scene = scene_match.group(1).strip() if scene_match else "Unknown scene"

            # Extract image prompt
            image_prompt_match = re.search(
                r'IMAGE_PROMPT:\s*(.+?)(?=DIALOGUE:|NARRATION:|PANEL|\Z)',
                panel_content,
                re.IGNORECASE | re.DOTALL
            )
            image_prompt = image_prompt_match.group(1).strip() if image_prompt_match else scene

            # Extract dialogues
            dialogue_section = re.search(
                r'DIALOGUE:\s*(.+?)(?=NARRATION:|PANEL|\Z)',
                panel_content,
                re.IGNORECASE | re.DOTALL
            )

            dialogues = []
            if dialogue_section:
                dialogue_lines = dialogue_section.group(1).strip().split('\n')
                for line in dialogue_lines:
                    line = line.strip()
                    if line and (line.startswith('-') or line.startswith('*')):
                        # Remove leading dash/asterisk and clean up
                        dialogue = line[1:].strip()
                        if dialogue:
                            dialogues.append(dialogue)

            # Extract narration
            narration_match = re.search(r'NARRATION:\s*(.+?)(?:\n|PANEL|\Z)', panel_content, re.IGNORECASE)
            narration = narration_match.group(1).strip() if narration_match else None

            # Create panel object
            panel = ComicPanel(
                panel_number=panel_num,
                scene=scene,
                dialogue=dialogues,
                narration=narration,
                image_prompt=image_prompt
            )

            panels.append(panel)

        return panels

    def _generate_panel_images(self, panels: List[ComicPanel]) -> List[ComicPanel]:
        """
        Generate images for all comic panels.

        Args:
            panels: List of ComicPanel objects

        Returns:
            List of ComicPanel objects with image_data populated
        """
        if not self.generate_images:
            return panels
            
        print(f"Generating images for {len(panels)} panels...")
        
        billing_warning_shown = False

        for i, panel in enumerate(panels):
            try:
                print(f"  Generating image for panel {panel.panel_number}...")

                # Use Imagen API to generate images
                image_data = self._generate_image_with_imagen(panel.image_prompt)
                panel.image_data = image_data

            except Exception as e:
                error_msg = str(e)
                
                # Check if it's a billing error and only show the warning once
                if ("billed users" in error_msg.lower() or "billing" in error_msg.lower()) and not billing_warning_shown:
                    print(f"\n  {'=' * 66}")
                    print(f"  NOTE: Imagen API requires a billing account to generate images.")
                    print(f"  Creating high-quality placeholder images for all panels instead.")
                    print(f"  {'=' * 66}\n")
                    billing_warning_shown = True
                elif not billing_warning_shown:
                    print(f"  Warning: Failed to generate image for panel {panel.panel_number}: {e}")
                
                # Create placeholder if generation fails
                panel.image_data = self._create_placeholder_image(panel)

        return panels

    def _generate_image_with_imagen(self, prompt: str) -> str:
        """
        Generate image using Imagen model via the new Google GenAI SDK.

        Args:
            prompt: The image generation prompt

        Returns:
            Base64 encoded image data
        """
        try:
            # Enhance the prompt for comic book style
            enhanced_prompt = f"Comic book art style with bold outlines and vibrant colors. {prompt}"
            
            # Generate image using the new API
            response = self.client.models.generate_images(
                model=self.image_model_name,
                prompt=enhanced_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="1:1",  # Square format for comic panels
                )
            )
            
            if response.generated_images and len(response.generated_images) > 0:
                # Get the first generated image
                generated_image = response.generated_images[0]

                # The SDK may return different types for the image payload depending
                # on the SDK version or model. Handle common cases robustly:
                # - bytes/bytearray
                # - a PIL Image-like object with .save()
                # - an object with raw bytes on attributes like 'content' or 'image_bytes'
                img_bytes = None

                # Case A: raw bytes
                if isinstance(generated_image.image, (bytes, bytearray)):
                    img_bytes = bytes(generated_image.image)

                # Case B: object with a save() method (PIL Image or similar)
                else:
                    img_obj = generated_image.image
                    # Try saving with explicit format first, then without
                    try:
                        img_io = BytesIO()
                        # Some implementations accept format kw, others don't
                        img_obj.save(img_io, format='PNG')
                        img_bytes = img_io.getvalue()
                    except TypeError:
                        try:
                            img_io = BytesIO()
                            img_obj.save(img_io)
                            img_bytes = img_io.getvalue()
                        except Exception:
                            # Try common attribute names that may contain raw bytes
                            for attr in ('content', 'image_bytes', 'data', 'bytes'):
                                val = getattr(img_obj, attr, None)
                                if isinstance(val, (bytes, bytearray)):
                                    img_bytes = bytes(val)
                                    break

                if not img_bytes:
                    raise Exception('Unable to extract image bytes from SDK response')

                image_base64 = base64.b64encode(img_bytes).decode('utf-8')

                print(f"    ✓ Image generated successfully")
                return image_base64
            else:
                raise Exception("No images generated in response")

        except Exception as e:
            error_msg = str(e)
            if "billed users" in error_msg.lower() or "billing" in error_msg.lower():
                print(f"    ℹ Imagen API requires billing to be enabled")
                print(f"    ℹ Using high-quality placeholder instead")
            else:
                print(f"    Imagen generation failed: {e}")
            raise

    def _create_placeholder_image(self, panel: ComicPanel, width: int = 512, height: int = 384) -> str:
        """
        Create a placeholder image with the scene description.

        Args:
            panel: The ComicPanel object
            width: Image width
            height: Image height

        Returns:
            Base64 encoded image data
        """
        # Create a colorful gradient background
        img = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(img)

        # Draw gradient background
        for y in range(height):
            # Create a gradient from purple to blue
            r = int(102 + (118 - 102) * (y / height))
            g = int(126 + (187 - 126) * (y / height))
            b = int(241 + (162 - 241) * (y / height))
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        # Add panel number badge
        badge_size = 60
        draw.ellipse([20, 20, 20 + badge_size, 20 + badge_size],
                    fill='#6366f1', outline='white', width=4)

        # Draw panel number
        try:
            # Try to use a nice font
            font_large = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 32)
            font_medium = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 16)
        except:
            # Fall back to default font
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()

        number_text = str(panel.panel_number)
        # Center the number in the badge
        bbox = draw.textbbox((0, 0), number_text, font=font_large)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        number_x = 20 + (badge_size - text_width) // 2
        number_y = 20 + (badge_size - text_height) // 2
        draw.text((number_x, number_y), number_text, fill='white', font=font_large)

        # Draw scene description with word wrap
        scene_text = panel.scene if len(panel.scene) <= 200 else panel.scene[:197] + "..."

        # Word wrap the text
        words = scene_text.split()
        lines = []
        current_line = []
        max_width = width - 40

        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font_medium)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Limit to first 8 lines
        lines = lines[:8]

        # Draw text box for scene
        box_y = height - 160
        draw.rectangle([10, box_y, width - 10, height - 10],
                      fill='white', outline='#6366f1', width=3)

        # Draw scene text
        text_y = box_y + 10
        for line in lines:
            draw.text((20, text_y), line, fill='#1f2937', font=font_medium)
            text_y += 18

        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        return img_base64

    def generate_comic_text(self, story: str, max_panels: int = 10) -> str:
        """
        Generate comic strip and return as formatted text.

        Args:
            story: The story text to convert into comic panels
            max_panels: Maximum number of panels to generate

        Returns:
            Formatted string representation of the comic strip
        """
        panels = self.generate_comic(story, max_panels)

        output = "=" * 60 + "\n"
        output += "COMIC STRIP\n"
        output += "=" * 60 + "\n\n"

        for panel in panels:
            output += str(panel) + "\n\n"

        output += "=" * 60

        return output

    def generate_comic_dict(self, story: str, max_panels: int = 10) -> List[Dict]:
        """
        Generate comic strip and return as list of dictionaries.

        Args:
            story: The story text to convert into comic panels
            max_panels: Maximum number of panels to generate

        Returns:
            List of dictionaries representing comic panels
        """
        panels = self.generate_comic(story, max_panels)
        return [panel.to_dict() for panel in panels]


# Convenience function for quick usage
def story_to_comic(story: str, api_key: Optional[str] = None, max_panels: int = 10) -> str:
    """
    Quick function to convert a story to comic strip format.

    Args:
        story: The story text to convert
        api_key: Google Gemini API key (optional if set in environment)
        max_panels: Maximum number of panels to generate

    Returns:
        Formatted string representation of the comic strip
    """
    generator = StoryToComicGenerator(api_key=api_key)
    return generator.generate_comic_text(story, max_panels)
