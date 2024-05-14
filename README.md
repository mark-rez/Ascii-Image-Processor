![example image](https://github.com/Giooorgiooo/Ascii-Image-Processor/blob/main/example.png)

# Ascii Image Processor

This is a simple Python program that converst an image into ascii art.

I thank all people that use this for their project. I love to contribute to the community. However, please credit me by using the GitHub project link.

## Usage

To use this program, you need python 3.6+ and all of the required packages installed.
To install the required packages, run: `pip3 install -r requirements.txt`

### Convert image to ascii art from argument
1. Run `py main.py -image "PATH/TO/IMAGE" -output "OUTPUT FILENAME"`
   
| Argument  | Description |
| ------------- | ------------- |
|  -image | path to input image  |
| -output  | output file name  |
| --colored  | enables colors  |
| --char_per_pixel  | creates an ascii char for every pixel  |
| -font_size  | change font size (default: 16)  |
| -font_path  | path to the font file (default file: consolas.ttf) |
| -characters  | change the used characters (must be sorted from darkest to brightest) |

### Convert image to ascii art in python script
1. Import the text-to-speech function with `from imageprocessor import AsciiImageProcessor`.
2. Create an instance of `AsciiImageProcessor`: `processor = AsciiImageProcessor()` in your code.
3. Get an image by running `image = processor.get_ascii_img("PATH/TO/YOUR/IMAGE")`
4. Save the image `image.save("OUTPUT FILE NAME")`

I provided an [example script](https://github.com/Giooorgiooo/Ascii-Image-Processor/blob/main/examplescript.py) which shows how the ascii-image-converter could be used in a script.
