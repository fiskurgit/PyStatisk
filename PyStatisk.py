import Log
import sys
import os
from pathlib import Path


def process_markdown(template, markdown_file):
    Log.blue('processing %s' % markdown_file)


def process_posts(template, posts):
    found_markdown = False
    for file in os.listdir(posts):
        filename = os.fsdecode(file)
        if filename.endswith(".md"):
            found_markdown = True
            process_markdown(template, file)
            continue
        else:
            continue

    if not found_markdown:
        Log.fatal_error("no markdown files found in %s" % posts)


def process_path(root):
    template = Path(root, '_template.html')
    if template.exists():
        Log.blue('%s exists...' % template)
        posts_directory = Path(root, 'posts')
        if posts_directory.exists():
            Log.blue('%s exists...' % posts_directory)
            process_posts(template, posts_directory)
        else:
            Log.fatal_error('missing posts/ directory')
    else:
        Log.fatal_error('missing _template.html')


if __name__ == '__main__':
    Log.line_break()
    Log.title()
    Log.line_break()
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

