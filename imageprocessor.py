# author: Giorgio
# date: 13.05.2024
# topic: ascii art
# repo: https://github.com/Giooorgiooo/Ascii-Image-Processor

from PIL import Image, ImageFont, ImageDraw, UnidentifiedImageError
from pathlib import Path
from colorsys import hsv_to_rgb, rgb_to_hsv
import os

class AsciiImageProcessor:
    class Characters:
        # Long list of characters ordered by intensity
        LONG: str = "`.-':_,^=;><+!rc*/z?sLTv)J7(|Fi{C}fI31tlu[neoZ5Yxjya]2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"
        # Short list of characters for simpler representation
        SHORT: str = " .:-=+*#%@"
        # Default list of characters for ASCII conversion
        DEFAULT: str = ".'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    
    def __init__(self, font_path: str = str(os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")+"/consolas.ttf") , font_size: int = 16, characters: str = Characters.DEFAULT, colored: bool = False) -> None:
        """
        Initialize AsciiImageProcessor.

        Args:
            font_path (str): Path to the font file.
            font_size (int): Size of the font.
            characters (str): String of characters to represent different shades of pixels.
            colored (bool): Flag to indicate whether to preserve the color of the original image.
        """
        self.characters: str = characters

        self.font_size = font_size
        self.font_path = font_path
        # Load font
        self.font: ImageFont.FreeTypeFont = ImageFont.truetype(self.font_path, size=self.font_size)
        
    def set_characters(self, characters: str) -> None:
        """
        Set custom characters for ASCII conversion.

        Args:
            characters (str): String of characters to represent different shades of pixels.
        """
        self.characters = characters
    
    def set_font(self, path: str) -> None:
        """
        Set custom font for ASCII conversion.

        Args:
            path (str): Path to the font file.
        """
        self.font_path = path
        self.font: ImageFont.FreeTypeFont = ImageFont.truetype(self.font_path, size=self.font_size)

    def set_font_size(self, font_size: int) -> None:
        """
        Set font size for ASCII conversion.

        Args:
            font_size (int): Size of the font.
        """
        self.font: ImageFont.FreeTypeFont = ImageFont.truetype(self.font_path, size=font_size)

    def _get_char_size(self) -> tuple[int, int, int]:
        """
        Get the width and height of a character.

        Returns:
            tuple[int, int, int]: Width and height of a character.
        """
        # Get the bounding box of a space character
        box: tuple[int, int, int, int] = self.font.getbbox(" ")
        return box[2], box[3]

    def _get_grouped_pixel(self, image: Image, root_x: int, root_y: int) -> tuple[int, int, int]:
        """
        Get the average RGB value of a group of pixels.

        Args:
            image (Image): Image object.
            root_x (int): X-coordinate of the top-left corner of the group of pixels.
            root_y (int): Y-coordinate of the top-left corner of the group of pixels.

        Returns:
            tuple[int, int, int]: Average RGB value of the group of pixels.
        """
        image_width, image_height = image.size
        average_pixel: list[int] = [0, 0, 0]

        rows, cols = self._get_char_size()

        # Iterate over the group of pixels
        for offset_y in range(cols):
            for offset_x in range(rows):
                if (root_x + offset_x < image_width) and (root_y + offset_y < image_height):
                    # Get pixel value
                    pixel = image.getpixel((root_x + offset_x, root_y + offset_y))
                    
                    # Accumulate RGB values
                    for i in range(3):
                        average_pixel[i] += pixel[i] / (rows * cols)

        return round(average_pixel[0]), round(average_pixel[1]), round(average_pixel[2])

    def get_ascii_img(self, path: str, colored: bool = False, char_per_pixel: bool = False) -> Image:
        """
        Convert an image to ASCII art.

        Args:
            path (str): Path to the image file.
            colored (bool): Flag to indicate whether to preserve the color of the original image.
            char_per_pixel (bool): Flag to indicate whether to use one character per pixel.

        Returns:
            Image: ASCII art image.
        """
        if not Path(path).exists():
            raise ValueError(f"The path '{path}' does not exist.")

        try:
            # Open an image
            original_image: Image = Image.open(path)
        except UnidentifiedImageError:
            raise UnidentifiedImageError(f"Cannot identify file '{path}' as an image.")

        # Get the dimensions of the image
        original_image_width, original_image_height = original_image.size

        character_size: tuple[int, int] = self._get_char_size()

        rows: list[list[tuple[str, tuple[int, int, int]]]] = []

        step_x = 1 if char_per_pixel else character_size[0]
        step_y = 1 if char_per_pixel else character_size[1]
        # Iterate over each pixel
        for y in range(0, original_image_height, step_y):
            row: list[tuple[str, tuple[int, int, int]]] = []
            for x in range(0, original_image_width, step_x):
                pixel = original_image.getpixel((x, y)) if char_per_pixel else self._get_grouped_pixel(original_image, x, y) 
                # Calculate darkness based on average intensity of RGB values
                darkness: float = (pixel[0] + pixel[1] + pixel[2]) / 765
                # Choose appropriate character based on darkness
                character: str = self.characters[int(darkness * len(self.characters)) - 1]
                
                if colored:
                    # set brightness of color to 100% since the char handles the density/brightness of a pixel
                    h, s, v = rgb_to_hsv(pixel[0] / 255, pixel[1] / 255, pixel[2] / 255)
                    r, g, b = hsv_to_rgb(h, s, 1)
                    # Append character and pixel color to the row
                    row.append((character, (int(r * 255), int(g * 255), int(b * 255))))
                else:
                    row.append((character, (255, 255, 255)))

            rows.append(row)

        # Create a new image for ASCII art
        ascii_image: Image = Image.new("RGBA", 
                                       (original_image_width * (character_size[0] if char_per_pixel else 1), 
                                        original_image_height * (character_size[1] if char_per_pixel else 1)), "black")
        
        # Draw text on the ASCII image
        draw: ImageDraw = ImageDraw.Draw(ascii_image)
        for y, row in enumerate(rows):
            for x, character in enumerate(row):
                draw_point: tuple[int, int] = (x * character_size[0], y * character_size[1])
                draw.text(draw_point, character[0], font=self.font, fill=(character[1][0], character[1][1], character[1][2]), align="center")

        return ascii_image