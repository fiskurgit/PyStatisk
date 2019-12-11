from PIL import Image
from pathlib import Path
import random


def gray_value(r, g, b):
    return 0.2989 * r + 0.5870 * g + 0.1140 * b


def filter_2x2_bayer(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    matrix = [[1, 3], [4, 2]]

    for x in range(width):
        for y in range(height):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            gray += gray * matrix[x % 2][y % 2] / 5

            if gray < threshold:
                filtered_image[x, y] = 0
            else:
                filtered_image[x, y] = (255, 255, 255)

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)


def filter_3x3_bayer(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    matrix = [[3, 7, 4], [6, 1, 9], [2, 8, 5]]

    for x in range(width):
        for y in range(height):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            gray += gray * matrix[x % 3][y % 3] / 10

            if gray < threshold:
                filtered_image[x, y] = 0
            else:
                filtered_image[x, y] = (255, 255, 255)

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)


def filter_4x4_bayer(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    matrix = [[1, 9, 3, 11], [13, 5, 15, 7], [4, 12, 2, 10], [16, 8, 14, 6]]

    for x in range(width):
        for y in range(height):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            gray += gray * matrix[x % 4][y % 4] / 17

            if gray < threshold:
                filtered_image[x, y] = 0
            else:
                filtered_image[x, y] = (255, 255, 255)

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)


def filter_5x3_bayer(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    matrix = [[9, 3, 0, 6, 12], [10, 4, 1, 7, 13], [11, 5, 2, 8, 14]]

    for x in range(width):
        for y in range(height):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            # Horizontal:
            gray += gray * matrix[x % 3][y % 5] / 16

            # Vertical:
            # gray += gray * matrix[y % 3][x % 5] / 16

            if gray < threshold:
                filtered_image[x, y] = 0
            else:
                filtered_image[x, y] = (255, 255, 255)

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)


def filter_8x8_bayer(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    matrix = [[24, 10, 12, 26, 35, 47, 49, 37],
              [8, 0, 2, 14, 45, 59, 61, 51],
              [22, 6, 4, 16, 43, 57, 63, 53],
              [30, 20, 18, 28, 33, 41, 55, 39],
              [34, 46, 48, 36, 25, 11, 13, 27],
              [44, 58, 60, 50, 9, 1, 3, 15],
              [42, 56, 62, 52, 23, 7, 5, 17],
              [32, 40, 54, 38, 31, 21, 19, 29]]

    for x in range(width):
        for y in range(height):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            gray += gray * matrix[x % 8][y % 8] / 65

            if gray < threshold:
                filtered_image[x, y] = 0
            else:
                filtered_image[x, y] = (255, 255, 255)

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)


def filter_floyd_steinberg(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    errors = [[0 for x in range(width)] for y in range(height)]

    for x in range(width - 1):
        for y in range(height - 1):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + errors[x][y] < threshold:
                error = gray + errors[x][y]
                filtered_image[x, y] = 0
            else:
                error = gray + errors[x][y] - 255
                filtered_image[x, y] = (255, 255, 255)

            errors[x + 1][y] += 7 * error / 16
            errors[x - 1][y + 1] += 3 * error / 16
            errors[x][y + 1] += 5 * error / 16
            errors[x + 1][y + 1] += 1 * error / 16

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)


def filter_jarvis_judice_ninke(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    errors = [[0 for x in range(width)] for y in range(height)]

    for x in range(width - 1):
        for y in range(height - 1):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + errors[x][y] < threshold:
                error = gray + errors[x][y]
                filtered_image[x, y] = 0
            else:
                error = gray + errors[x][y] - 255
                filtered_image[x, y] = (255, 255, 255)

            errors[x + 1][y] += 7 * error / 48
            errors[x + 2][y] += 5 * error / 48

            errors[x - 2][y + 1] += 3 * error / 48
            errors[x - 1][y + 1] += 5 * error / 48
            errors[x][y + 1] += 7 * error / 48
            errors[x + 1][y + 1] += 5 * error / 48
            errors[x + 2][y + 1] += 3 * error / 48

            errors[x - 2][y + 2] += 1 * error / 48
            errors[x - 1][y + 2] += 3 * error / 48
            errors[x][y + 2] += 5 * error / 48
            errors[x + 1][y + 2] += 3 * error / 48
            errors[x + 2][y + 2] += 1 * error / 48

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)


def filter_sierra(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    errors = [[0 for y in range(height)] for x in range(width)]

    for x in range(width - 2):
        for y in range(height - 2):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + errors[x][y] < threshold:
                error = gray + errors[x][y]
                filtered_image[x, y] = 0
            else:
                error = gray + errors[x][y] - 255
                filtered_image[x, y] = (255, 255, 255)

            errors[x + 1][y] += 5 * error / 32
            errors[x + 2][y] += 3 * error / 32

            errors[x - 2][y + 1] += 2 * error / 32
            errors[x - 1][y + 1] += 4 * error / 32
            errors[x][y + 1] += 5 * error / 32
            errors[x + 1][y + 1] += 4 * error / 32
            errors[x + 2][y + 1] += 2 * error / 32

            errors[x - 1][y + 2] += 2 * error / 32
            errors[x][y + 2] += 3 * error / 32
            errors[x + 1][y + 2] += 2 * error / 32

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)


def filter_two_row_sierra(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    errors = [[0 for y in range(height)] for x in range(width)]

    for x in range(width - 2):
        for y in range(height - 1):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + errors[x][y] < threshold:
                error = gray + errors[x][y]
                filtered_image[x, y] = 0
            else:
                error = gray + errors[x][y] - 255
                filtered_image[x, y] = (255, 255, 255)

            errors[x + 1][y] += 4 * error / 16
            errors[x + 2][y] += 3 * error / 16

            errors[x - 2][y + 1] += 1 * error / 16
            errors[x - 1][y + 1] += 2 * error / 16
            errors[x][y + 1] += 3 * error / 16
            errors[x + 1][y + 1] += 2 * error / 16
            errors[x + 2][y + 1] += 1 * error / 16

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)


def filter_stucki(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    errors = [[0 for y in range(height)] for x in range(width)]

    for x in range(width - 2):
        for y in range(height - 2):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + errors[x][y] < threshold:
                error = gray + errors[x][y]
                filtered_image[x, y] = 0
            else:
                error = gray + errors[x][y] - 255
                filtered_image[x, y] = (255, 255, 255)

            errors[x + 1][y] += 8 * error / 42
            errors[x + 2][y] += 4 * error / 42

            errors[x - 2][y + 1] += 2 * error / 42
            errors[x - 1][y + 1] += 4 * error / 42
            errors[x][y + 1] += 8 * error / 42
            errors[x + 1][y + 1] += 4 * error / 42
            errors[x + 2][y + 1] += 2 * error / 42

            errors[x - 2][y + 2] += 1 * error / 42
            errors[x - 1][y + 2] += 2 * error / 42
            errors[x][y + 2] += 4 * error / 42
            errors[x + 1][y + 2] += 2 * error / 42
            errors[x + 2][y + 2] += 1 * error / 42

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)


def filter_atkinson(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    errors = [[0 for y in range(height)] for x in range(width)]

    for x in range(width - 2):
        for y in range(height - 2):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + errors[x][y] < threshold:
                error = gray + errors[x][y]
                filtered_image[x, y] = 0
            else:
                error = gray + errors[x][y] - 255
                filtered_image[x, y] = (255, 255, 255)

            errors[x + 1][y] += error / 8
            errors[x + 2][y] += error / 8

            errors[x - 1][y + 1] += error / 8
            errors[x][y + 1] += error / 8
            errors[x + 1][y + 1] += error / 8

            errors[x][y + 2] += error / 8

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)


def filter_left_to_right_error_diffusion(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    for y in range(height):
        error = 0
        for x in range(width):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + error < threshold:
                delta = gray
                filtered_image[x, y] = 0
            else:
                delta = gray - 255
                filtered_image[x, y] = (255, 255, 255)

            if abs(delta) < 10:
                delta = 0

            error += delta

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)


def filter_random(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    for y in range(height):
        for x in range(width):
            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            threshold = (random.random() * 1000) % 256

            if gray < threshold:
                filtered_image[x, y] = 0
            else:
                filtered_image[x, y] = (255, 255, 255)

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)


def filter_threshold(image_file, threshold):
    source_image = Image.open(image_file).convert("RGB")
    image_copy = source_image.copy()
    filtered_image = image_copy.load()
    width, height = source_image.size

    for y in range(height):
        for x in range(width):
            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray < threshold:
                filtered_image[x, y] = 0
            else:
                filtered_image[x, y] = (255, 255, 255)

    output_filename = Path(image_file.parent, 'processed_%s' % image_file.name)
    image_copy.save(output_filename)
