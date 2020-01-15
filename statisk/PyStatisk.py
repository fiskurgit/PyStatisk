import re
from statisk import ImageFilter, Log
import sys
import os
import markdown
from pathlib import Path

DITHER_PREFIX = "p_"

post_links = list()
post_titles = list()


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
            threshold_arg = get_value(config_str, '-threshold', False)
            threshold_value = 255
            if threshold_arg is not None:
                threshold_value = int(threshold_arg)

            if filter_name is not None:
                # We have a filter - but do we have any foreground or background overrides?
                image_foreground = get_value(config_str, '-image_foreground', False)
                if image_foreground is not None:
                    ImageFilter.foreground = tuple(int(image_foreground.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
                else:
                    ImageFilter.foreground = ImageFilter.BLACK

                image_background = get_value(config_str, '-image_background', False)
                if image_background is not None:
                    ImageFilter.background = tuple(int(image_background.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
                else:
                    ImageFilter.background = ImageFilter.WHITE

                ImageFilter.filter_from_name(file, threshold_value, output_filename, filter_name)
            else:
                # No filter name supplied in config header data so just resize to max width
                ImageFilter.filter_dummy(file, 0, output_filename)

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
    Log.green('processing:  %s' % markdown_file)

    output_filename = markdown_file.name.replace(".md", ".html")
    output_file = Path(markdown_file.parent, output_filename)

    if "posts/" in str(output_file):
        post_link = str(output_file)
        post_segment_index = post_link.index("posts/")
        post_link = post_link[post_segment_index:]
        post_links.append(post_link)

    Log.blue('output file: %s' % output_file)

    md_stream = open(markdown_file)
    md_content = md_stream.read()
    config_str = md_content.split('\n', 1)[0]
    md_stream.close()

    html = markdown.markdown(md_content)
    output_html = html_template.replace("{{ content }}", html)

    title = extract_title(md_content)

    # Only add title if we're within posts/
    if "posts/" in str(output_file):
        post_titles.append(title)

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
        Log.grey('%s exists...' % template)
        posts_directory = Path(root, 'posts')
        if posts_directory.exists():
            Log.grey('%s exists...' % posts_directory)
            template_stream = open(template)
            html_template = template_stream.read()
            template_stream.close()

            process_posts(html_template, posts_directory)

            # All posts should now be built but the index needs creating
            Log.line_break()
            Log.grey('Building index...')
            index_md = Path(root, 'index.md')
            if index_md.exists():
                process_markdown(html_template, index_md)
        else:
            Log.fatal_error('missing posts/ directory')
    else:
        Log.fatal_error('missing _template.html')


def entry():
    Log.title()

    post_links.clear()
    post_titles.clear()

    argument_count = len(sys.argv)

    if argument_count == 1:
        Log.fatal_error("no path argument")

    arguments = list(sys.argv)
    path_input = arguments[1]
    website_root = Path(path_input)

    if website_root.exists():
        Log.grey('%s exists...' % website_root)
        process_path(website_root)

        posts = ""

        Log.line_break()

        # Add links to posts to index.html
        for index in range(len(post_titles)):
            post_link = post_links[index]
            post_title = post_titles[index]
            posts = posts + '<a href="' + post_link + '">' + post_title + '</a><br>\n'
            Log.grey("post_link: " + post_link + " post_title: " + post_title)

        index_path = Path(website_root, 'index.html')
        if index_path.exists():
            index_stream = open(index_path)
            index_template = index_stream.read()
            index_stream.close()
            index_template = index_template.replace("{{ posts }}", posts)
            index_path.write_text(index_template)

        Log.line_break()
        Log.green("Finished")

    else:
        Log.fatal_error('%s cannot be found' % website_root)


if __name__ == "__main__":
    entry()
