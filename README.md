![PyStatisk Ascii Logo](assets/ascii_logo.png)
## PyStatisk

A Python port of the Kotlin [Statisk](https://github.com/fiskurgit/Statisk) project, designed to run on low power devices (RaspberryPi Zero). Converts Markdown files to simple Html with image size reduction for extreme low-bandwidth web pages.

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