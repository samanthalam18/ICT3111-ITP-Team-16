# ITP-Team-16

## Description

This part of the project aims to give user a better interface when performing CT image enhancement.

## Installation

To get started, follow these steps:

1. Clone the repository.
2. Navigate to the project directory.
3. Open a terminal and run the following command.
   `pip install -r requirements.txt`
4. Go to `https://pytorch.org/` to download the appriopriate pytorch version. Tip if you are using pip add the `--force-install` flag.
## VSCode

1. Open a new terminal.
2. Run the following command.
   `python -m flask run`

## Pycharm

1. Run app.py.

## Usage in UI

The project structure is organized as follows:

-    **app.py**: This file contains the main Python logic, routing, and functions of the application.

-    **templates**: This directory contains the HTML templates used by the application.

     -    **index.html**: The home page template.
     -    **base.html**: The base template that includes the header, footer, and links to Bootstrap and CSS files.
     -    **predict.html**: This template is displayed when the enhance button is pressed on the home page, showing the uploaded and enhanced image.
     -    **cyst.html**: The Cyst tab template. It displays all the uploaded and enhanced images from the image folder that contain the word 'cyst' in the image name.
     -    **normal.html**: The Normal tab template. It displays all the uploaded and enhanced images from the image folder that contain the word 'normal' in the image name.
     -    **history.html**: The All tab template. It displays all the uploaded and enhanced images from the image folder.

-    **static**: This directory contains the style.css file, which includes all the CSS used for the templates.

-    **uploads**: This directory contains all the uploaded images.

-    **images**: This directory contains all the enhanced images.
