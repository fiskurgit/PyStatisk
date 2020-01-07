![PyStatisk Ascii Logo](https://raw.githubusercontent.com/fiskurgit/PyStatisk/master/assets/ascii_logo.png)
## PyStatisk

A Python port of the Kotlin [Statisk](https://github.com/fiskurgit/Statisk) project, designed to run on low power devices (RaspberryPi Zero). Converts Markdown files to simple Html with image size reduction for extreme low-bandwidth web pages.

![](https://raw.githubusercontent.com/fiskurgit/PyStatisk/master/assets/website_screenshot.png)

## Install

Install via [PIP](https://pypi.org/project/Statisk/):

`pip install Statisk`

then run with:

`stsk /path/to/blog/`

## Setup

`_template.html` should be placed in root directory of the website, simple example:

```html
<!DOCTYPE html>
<html>
    <head>
        <!-- Optional -->
        <title>{{ title }}</title>  
    </head>
    <body>
        {{ content }}
        <footer>
            <!-- Optional -->
            {{ page_size }}
        </footer>
    </body>
</html>
```

## Blog Structure
Markdown posts need to be in a Year/Month/Day (`YYYY/MM/DD`) structure inside a root `posts/` directory:
<pre style="font-family: monospace;">
|- _template.html  
|- posts/  
    |- 2020/  
        |- 01/ 
            |-20/ 
                |- index.md   
                |- picture.png  
            |-15/ 
                |- index.md
    |- 2019/  
        |- 12/    
            |-24/ 
                |- index.md
                |- pictureA.png 
                |- pictureB.png 
</pre> 

## Style Parameters

Markdown posts can set parameters to override how images are handled and to set the page background:

| Argument | Behaviour | 
| --- | --- |
| `-algorithm` | Sets dither algorithm (see below), eg. `-algorithm stucki` |
| `-threshold` | Set threshold of dither algorithms in range 0 to 255, eg. `-threshold  255` |
| `-image_foreground` | (__todo__) Set the foreground colour for dithered images, eg. `-image_foreground  #0e0e0e` |
| `-image_background` | (__todo__) Set the background colour for dithered images, eg. `-image_background  #efefef` |
| `-background` | Override the page background colour, eg. `-background  #efefef` |

### Dithering

Available dithering algorithms (from [DitherKt](https://github.com/fiskurgit/DitherKt)):

`2by2Bayer`, `3by3Bayer`, `4by4Bayer`, `5by3Bayer`, `8by8Bayer`, `FloydSteinberg`, `FalseFloydSteinberg`, `NewspaperHalftone`, `JarvisJudiceNinke`, `Sierra`, `SierraLite`, `TwoRowSierra`, `Burkes`, `Atkinson`, `Stucki`, `ErrorDif`, `Threshold`, `Random`

there's also a `greyscale` filter (`-algorithm greyscale`), threshold is ignored.