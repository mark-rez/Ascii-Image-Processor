# author: Giorgio
# date: 13.05.2024
# topic: ascii art
# repo: https://github.com/Giooorgiooo/Ascii-Image-Processor

from PIL import Image
from imageprocessor import AsciiImageProcessor

# configure converting
processor = AsciiImageProcessor()
processor.set_characters(AsciiImageProcessor.Characters.SHORT)

# Create and save image
image: Image = processor.get_ascii_img("input/original_image.jpg", char_per_pixel=True)
image.save("output/output_image.png")