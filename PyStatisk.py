import Log
import sys
import markdown
from pathlib import Path


def process_markdown(html_template, markdown_file):
    Log.blue('processing:  %s' % markdown_file)

    md_content = open(markdown_file)
    html = markdown.markdown(md_content.read())

    output_dir = markdown_file.parent
    output_filename = markdown_file.name.replace(".md", ".html")
    output_file = Path(output_dir, output_filename)
    Log.purple('output file: %s' % output_file)

    output_html = html_template.replace("{{ content }}", html)
    Log.salmon(output_html)

    output_file.write_text(output_html)


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

