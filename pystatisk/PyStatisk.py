import re

from pystatisk import Dither, Log
import sys
import markdown
from pathlib import Path

DITHER_PREFIX = "p_"


def process_images(directory):
    files = directory.glob('*')
    for file_name in files:
        file = Path(file_name)
        if not str(file.name).startswith(DITHER_PREFIX) and \
                file.name.endswith(".jpeg") or \
                file.name.endswith(".jpg") or \
                file.name.endswith(".png"):
            Log.blue('dithering:   %s' % file)
            Dither.filter_stucki(file, 185, DITHER_PREFIX)


def process_markdown(html_template, markdown_file):
    Log.line_break()
    Log.salmon('processing:  %s' % markdown_file)

    output_filename = markdown_file.name.replace(".md", ".html")
    output_file = Path(markdown_file.parent, output_filename)
    Log.purple('output file: %s' % output_file)

    md_content = open(markdown_file)
    html = markdown.markdown(md_content.read())
    output_html = html_template.replace("{{ content }}", html)

    # Replace image references
    images = re.findall("([-\w]+\.(?:jpg|gif|png|jpeg))", output_html, re.IGNORECASE)

    if len(images) > 0:
        # Log.salmon('images:      %s' % images)
        for image_ref in images:
            processed_filename = '%s%s' % (DITHER_PREFIX, image_ref)
            output_html = output_html.replace(image_ref, processed_filename)

    output_file.write_text(output_html)

    process_images(markdown_file.parent)


def process_posts(template, posts):
    markdown_files = Path(posts).glob('**/*/*.md')
    for md in markdown_files:
        process_markdown(template, md)


def process_path(root):
    template = Path(root, '_template.html')
    if template.exists():
        Log.blue('%s exists...' % template)
        posts_directory = Path(root, 'posts')
        if posts_directory.exists():
            Log.blue('%s exists...' % posts_directory)
            html_template = open(template).read()
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

    arguments = list(sys.argv)
    pathInput = arguments[1]
    websiteRoot = Path(pathInput)

    if websiteRoot.exists():
        Log.blue('%s exists...' % pathInput)
        process_path(websiteRoot)
    else:
        Log.fatal_error('path cannot be found')
