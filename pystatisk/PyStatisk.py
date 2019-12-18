import re
from pystatisk import Dither, Log
import sys
import os
import markdown
from pathlib import Path

DITHER_PREFIX = "p_"


# Lazily copied from https://stackoverflow.com/a/32009595/7641428
def bytes_label(size, precision=2):
    suffixes = [' bytes', 'kb', 'mb', 'gb', 'tb']
    suffix_index = 0
    while size > 1024 and suffix_index < 4:
        suffix_index += 1
        size = size/1024.0
    return "%.*f%s" % (precision, size, suffixes[suffix_index])


# Assumes data is in format '-some_key some_value -some_other_key another_value'
def get_value(meta_data, key, show_log):
    key_index = meta_data.find(key)
    if key_index == -1:
        if show_log:
            Log.error('Key {0} does not exist in {1}'.format(key, meta_data))
        return None
    else:
        data_index = key_index + len(key) + 1
        post_data = meta_data[data_index:]
        return post_data.split(' ')[0]


def process_images(directory, config_str):
    Log.blue('post config: %s' % config_str)
    files = directory.glob('*')
    image_bytes = 0
    for file_name in files:
        file = Path(file_name)
        if not str(file.name).startswith(DITHER_PREFIX) and \
                file.name.endswith(".jpeg") or \
                file.name.endswith(".jpg") or \
                file.name.endswith(".png"):
            Log.blue('processing:   %s' % file)
            output_filename = Path(file.parent, '%s%s' % (DITHER_PREFIX, file.name))

            filter_name = get_value(config_str, '-algorithm', False)
            threshold_value = get_value(config_str, '-threshold', False)

            if threshold_value is None:
                threshold_value = 255

            if filter_name is not None:
                Dither.filter_from_name(file, threshold_value, output_filename, filter_name)
            else:
                # No filter name supplied in config header data so just resize to max width
                Dither.filter_dummy(file, 0, output_filename)

            stat_info = os.stat(output_filename)
            size = stat_info.st_size
            image_bytes = image_bytes + size

    return image_bytes


# Assumes markdown header in format: # SomeHeader
def extract_title(content):
    meta_data_index = content.find('-->')

    if meta_data_index is not -1:
        title = content[(meta_data_index + 3):].strip()
    else:
        title = content

    key_index = title.find('#')
    title = title[(key_index + 2):]
    return title.split('\n')[0]


def process_markdown(html_template, markdown_file):
    Log.line_break()
    Log.salmon('processing:  %s' % markdown_file)

    output_filename = markdown_file.name.replace(".md", ".html")
    output_file = Path(markdown_file.parent, output_filename)
    Log.blue('output file: %s' % output_file)

    md_stream = open(markdown_file)
    md_content = md_stream.read()
    config_str = md_content.split('\n', 1)[0]
    md_stream.close()

    html = markdown.markdown(md_content)
    output_html = html_template.replace("{{ content }}", html)

    title = extract_title(md_content)
    output_html = output_html.replace('{{ title }}', title)

    # Page background colour override
    if config_str.__contains__("-bg") or config_str.__contains__("-background"):
        background_color = get_value(config_str, "-bg", False)
        if background_color is None:
            background_color = get_value(config_str, "-background", False)

        Log.blue("override page background: %s" % background_color)
        output_html = output_html.replace('<body', str('<body style="background-color:%s"' % background_color))

    # Replace image references
    images = re.findall("([-\w]+\.(?:jpg|gif|png|jpeg))", output_html, re.IGNORECASE)

    if len(images) > 0:
        # Log.salmon('images:      %s' % images)
        for image_ref in images:
            processed_filename = '%s%s' % (DITHER_PREFIX, image_ref)
            output_html = output_html.replace(image_ref, processed_filename)

    # Calculate html size
    page_bytes = len(output_html.encode('utf-8'))
    image_bytes = process_images(markdown_file.parent, config_str)
    output_html = output_html.replace('{{ page_size }}',
                                      str('Page size including images: ' + bytes_label(image_bytes + page_bytes, 0)))

    output_file.write_text(output_html)


def process_posts(template, posts_directory):
    markdown_files = Path(posts_directory).glob('**/*/*.md')
    for md in markdown_files:
        process_markdown(template, md)


def process_path(root):
    template = Path(root, '_template.html')
    if template.exists():
        Log.blue('%s exists...' % template)
        posts_directory = Path(root, 'posts')
        if posts_directory.exists():
            Log.blue('%s exists...' % posts_directory)
            template_stream = open(template)
            html_template = template_stream.read()
            template_stream.close()

            process_posts(html_template, posts_directory)
        else:
            Log.fatal_error('missing posts/ directory')
    else:
        Log.fatal_error('missing _template.html')


if __name__ == '__main__':
    Log.title()
    Log.blue("PyStatisk")

    argumentCount = len(sys.argv)

    if argumentCount == 1:
        Log.fatal_error("no path argument")

    cwd = os.getcwd()
    Log.blue('Working dir: %s' % cwd)

    arguments = list(sys.argv)
    pathInput = arguments[1]
    websiteRoot = Path(pathInput)

    if websiteRoot.exists():
        Log.blue('%s exists...' % websiteRoot)
        process_path(websiteRoot)
    else:
        Log.fatal_error('%s cannot be found' % websiteRoot)

