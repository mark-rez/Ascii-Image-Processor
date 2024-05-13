# author: Giorgio
# date: 13.05.2024
# topic: ascii art
# repo: https://github.com/Giooorgiooo/Ascii-Image-Processor

import os
import argparse
from imageprocessor import AsciiImageProcessor

# Get the path to the directory of the current Python script
def main():
    default_font_path: str = str(os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")+"/consolas.ttf")
    
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("-image", type=str, help="Path to the image file")
    parser.add_argument("-output", type=str, help="Name of the output file")
    parser.add_argument("--colored", default=False, action="store_true", help="Preserve the color of the original image")
    parser.add_argument("--char_per_pixel", default=False, action="store_true", help="Use one character per pixel")
    parser.add_argument("-font_size", type=int, default=16, help="Size of the font (default: 16)")
    parser.add_argument("-font_path", type=str, default=default_font_path, help="Path to the font file (default: consolas.ttf)")
    parser.add_argument("-characters", type=str, default=AsciiImageProcessor.Characters.SHORT, help="Used characters")
    
    args = parser.parse_args()

    # Create an instance of AsciiImageProcessor
    ascii_processor = AsciiImageProcessor(characters=args.characters, font_path=args.font_path, font_size=args.font_size)

    # Convert image to ASCII art
    ascii_image = ascii_processor.get_ascii_img(args.image, colored=args.colored, char_per_pixel=args.char_per_pixel)

    # Save ASCII art to output file
    ascii_image.save(args.output)

if __name__ == "__main__":
    main()
