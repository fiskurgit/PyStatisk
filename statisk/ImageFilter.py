from PIL import Image
from statisk import Log
import random

MAX_WIDTH = 960
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
background = WHITE
foreground = BLACK


def gray_value(r, g, b):
    return 0.2989 * r + 0.5870 * g + 0.1140 * b


# Just resizes the image, no filter
def filter_dummy(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)

    image_copy = source_image.copy()
    image_copy.save(output_filename)
    return output_filename


def filter_greyscale(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("L")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

    image_copy.save(output_filename)
    return output_filename


def filter_2x2_bayer(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

    matrix = [[1, 3], [4, 2]]

    for x in range(width):
        for y in range(height):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            gray += gray * matrix[x % 2][y % 2] / 5

            if gray < threshold:
                filtered_image[x, y] = foreground
            else:
                filtered_image[x, y] = background

    image_copy.save(output_filename)
    return output_filename


def filter_3x3_bayer(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

    matrix = [[3, 7, 4], [6, 1, 9], [2, 8, 5]]

    for x in range(width):
        for y in range(height):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            gray += gray * matrix[x % 3][y % 3] / 10

            if gray < threshold:
                filtered_image[x, y] = foreground
            else:
                filtered_image[x, y] = background

    image_copy.save(output_filename)
    return output_filename


def filter_4x4_bayer(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

    matrix = [[1, 9, 3, 11], [13, 5, 15, 7], [4, 12, 2, 10], [16, 8, 14, 6]]

    for x in range(width):
        for y in range(height):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            gray += gray * matrix[x % 4][y % 4] / 17

            if gray < threshold:
                filtered_image[x, y] = foreground
            else:
                filtered_image[x, y] = background

    image_copy.save(output_filename)
    return output_filename


def filter_5x3_bayer(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

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
                filtered_image[x, y] = foreground
            else:
                filtered_image[x, y] = background

    image_copy.save(output_filename)
    return output_filename


def filter_8x8_bayer(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

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
                filtered_image[x, y] = foreground
            else:
                filtered_image[x, y] = background

    image_copy.save(output_filename)
    return output_filename


def filter_floyd_steinberg(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

    errors = [[0 for x in range(width)] for y in range(height)]

    for x in range(width - 1):
        for y in range(height - 1):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + errors[x][y] < threshold:
                error = gray + errors[x][y]
                filtered_image[x, y] = foreground
            else:
                error = gray + errors[x][y] - 255
                filtered_image[x, y] = background

            errors[x + 1][y] += 7 * error / 16
            errors[x - 1][y + 1] += 3 * error / 16
            errors[x][y + 1] += 5 * error / 16
            errors[x + 1][y + 1] += 1 * error / 16

    image_copy.save(output_filename)
    return output_filename


def filter_jarvis_judice_ninke(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

    errors = [[0 for x in range(width)] for y in range(height)]

    for x in range(width - 1):
        for y in range(height - 1):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + errors[x][y] < threshold:
                error = gray + errors[x][y]
                filtered_image[x, y] = foreground
            else:
                error = gray + errors[x][y] - 255
                filtered_image[x, y] = background

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

    image_copy.save(output_filename)
    return output_filename


def filter_sierra(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

    errors = [[0 for y in range(height)] for x in range(width)]

    for x in range(width - 2):
        for y in range(height - 2):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + errors[x][y] < threshold:
                error = gray + errors[x][y]
                filtered_image[x, y] = foreground
            else:
                error = gray + errors[x][y] - 255
                filtered_image[x, y] = background

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

    image_copy.save(output_filename)
    return output_filename


def filter_two_row_sierra(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

    errors = [[0 for y in range(height)] for x in range(width)]

    for x in range(width - 2):
        for y in range(height - 1):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + errors[x][y] < threshold:
                error = gray + errors[x][y]
                filtered_image[x, y] = foreground
            else:
                error = gray + errors[x][y] - 255
                filtered_image[x, y] = background

            errors[x + 1][y] += 4 * error / 16
            errors[x + 2][y] += 3 * error / 16

            errors[x - 2][y + 1] += 1 * error / 16
            errors[x - 1][y + 1] += 2 * error / 16
            errors[x][y + 1] += 3 * error / 16
            errors[x + 1][y + 1] += 2 * error / 16
            errors[x + 2][y + 1] += 1 * error / 16

    image_copy.save(output_filename)
    return output_filename


def filter_stucki(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

    errors = [[0 for y in range(height)] for x in range(width)]

    for x in range(width - 2):
        for y in range(height - 2):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + errors[x][y] < threshold:
                error = gray + errors[x][y]
                filtered_image[x, y] = foreground
            else:
                error = gray + errors[x][y] - 255
                filtered_image[x, y] = background

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

    image_copy.save(output_filename)
    return output_filename


def filter_atkinson(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

    errors = [[0 for y in range(height)] for x in range(width)]

    for x in range(width - 2):
        for y in range(height - 2):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + errors[x][y] < threshold:
                error = gray + errors[x][y]
                filtered_image[x, y] = foreground
            else:
                error = gray + errors[x][y] - 255
                filtered_image[x, y] = background

            errors[x + 1][y] += error / 8
            errors[x + 2][y] += error / 8

            errors[x - 1][y + 1] += error / 8
            errors[x][y + 1] += error / 8
            errors[x + 1][y + 1] += error / 8

            errors[x][y + 2] += error / 8

    image_copy.save(output_filename)
    return output_filename


def filter_left_to_right_error_diffusion(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

    for y in range(height):
        error = 0
        for x in range(width):

            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray + error < threshold:
                delta = gray
                filtered_image[x, y] = foreground
            else:
                delta = gray - 255
                filtered_image[x, y] = background

            if abs(delta) < 10:
                delta = 0

            error += delta

    image_copy.save(output_filename)
    return output_filename


def filter_random(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

    for y in range(height):
        for x in range(width):
            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            threshold = (random.random() * 1000) % 256

            if gray < threshold:
                filtered_image[x, y] = foreground
            else:
                filtered_image[x, y] = background

    image_copy.save(output_filename)
    return output_filename


def filter_threshold(image_file, threshold, output_filename):
    source_image = Image.open(image_file).convert("RGB")
    width, height = source_image.size

    if width > MAX_WIDTH:
        width_ratio = (MAX_WIDTH / float(width))
        resize_height = int((float(height) * float(width_ratio)))
        source_image = source_image.resize((MAX_WIDTH, resize_height), Image.LANCZOS)
        width = MAX_WIDTH
        height = resize_height

    image_copy = source_image.copy()
    filtered_image = image_copy.load()

    for y in range(height):
        for x in range(width):
            r, g, b = source_image.getpixel((x, y))
            gray = gray_value(r, g, b)

            if gray < threshold:
                filtered_image[x, y] = foreground
            else:
                filtered_image[x, y] = background

    image_copy.save(output_filename)
    return output_filename


def filter_from_name(image_file, threshold, output_filename, filter_name):
    if filter_name == "greyscale":
        filter_greyscale(image_file, threshold, output_filename)
    elif filter_name == "2by2bayer":
        filter_2x2_bayer(image_file, threshold, output_filename)
    elif filter_name == "3by3bayer":
        filter_3x3_bayer(image_file, threshold, output_filename)
    elif filter_name == "4by4bayer":
        filter_4x4_bayer(image_file, threshold, output_filename)
    elif filter_name == "5by3bayer":
        filter_5x3_bayer(image_file, threshold, output_filename)
    elif filter_name == "8by8bayer":
        filter_8x8_bayer(image_file, threshold, output_filename)
    elif filter_name == "floydsteinberg":
        filter_floyd_steinberg(image_file, threshold, output_filename)
    elif filter_name == "jarvisjudiceninke":
        filter_jarvis_judice_ninke(image_file, threshold, output_filename)
    elif filter_name == "atkinson":
        filter_atkinson(image_file, threshold, output_filename)
    elif filter_name == "threshold":
        filter_threshold(image_file, threshold, output_filename)
    elif filter_name == "random":
        filter_random(image_file, threshold, output_filename)
    elif filter_name == "stucki":
        filter_stucki(image_file, threshold, output_filename)
    else:
        Log.fatal_error("Unrecognised filter: %s" % filter_name)

