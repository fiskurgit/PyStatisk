import Log
from PIL import Image
from pathlib import Path


# https://github.com/fiskurgit/DitherKt/blob/master/src/online/fisk/filters/Filter.kt
# https://codegolf.stackexchange.com/questions/26554/dither-a-grayscale-image
def process(image_file):
    Log.blue('dithering:   %s' % image_file)

    source_image = Image.open(image_file)
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size
    Log.blue('image size: %s' % str([width, height]))

    threshold = 255

    errors = [[0 for x in range(height)] for y in range(width)]

    for x in range(width - 2):
        for y in range(height - 2):
            gray = source_image.getpixel((x, y))

            if gray + errors[x][y] < threshold:
                error = gray + errors[x][y]
                filtered_image[x, y] = 0
            else:
                error = gray + errors[x][y] - 255
                filtered_image[x, y] = 255

            errors[x + 1][y] += error / 8
            errors[x + 2][y] += error / 8

            errors[x - 1][y + 1] += error / 8
            errors[x][y + 1] += error / 8
            errors[x + 1][y + 1] += error / 8

            errors[x][y + 2] += error / 8

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)
