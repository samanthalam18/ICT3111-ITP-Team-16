# ITP-Team-16

## Description

This repository is a part of a broader project dedicated to enhancing user interfaces for performing CT image enhancements.

## Table of Contents
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Credits](#credits)
- [License](#license)
- [Contact Information](#contact-information)

## Installation

Follow these steps to set up the project:

1. Clone this repository.
2. Navigate to the project directory.
3. Open a terminal and run the following command:
   `pip install -r requirements.txt`
4. Visit [Pytorch](https://pytorch.org/) to download the appropriate Pytorch version. If you're using pip, add the `--force-install` flag.
5. Download the models from the following [Google Drive link](https://drive.google.com/drive/folders/1m1NdVVHTWeTbTxiBsz91B7gKgqI3oiFj)
6. **Replace** the existing `denoising` folder in `ICT3111-ITP-Team-16\KAIR\swinir_denoising_gray_15` with the downloaded `denoising` folder from the Google Drive.
7. **Replace** the existing `checkpoints` folder in `ICT3111-ITP-Team-16\pytorch-CycleGAN-and-pix2pix` with the downloaded `checkpoints` folder from the Google Drive.


## Getting Started

### Getting Started with VSCode

1. Open a new terminal within VSCode.
2. Navigate to the project's directory:
```bash
cd ICT3111-ITP-Team-16/Ui
```
3. Start the application by running the following command:
```bash
python -m flask run 
```
or you can run
```
python app.py
```

### Using Pycharm

1. Run the `app.py` script.

## Usage

This application provides an interactive interface for CT image enhancement. You can upload an image, perform enhancement, and view the results.

## Project Structure

The project is organized as follows:

- `app.py`: Contains the main Python logic, routing, and functions of the application.
- `templates`: Contains the HTML templates used by the application.
- `static`: Contains the `style.css` file, which includes all the CSS used for the templates.
- `uploads`: Contains all the uploaded images.
- `images`: Contains all the enhanced images.

**Note**: In `app.py`, line 34 to 41 are for testing purposes only and should be replaced with the correct enhancement function. Line 129 should also be replaced according to the requirements of the enhancement function.

## Credits

We gratefully acknowledge the contributions of the following projects:

- [KAIR](https://github.com/cszn/KAIR)
- [pytorch-CycleGAN-and-pix2pix](https://github.com/junyanz/pytorch-CycleGAN-and-pix2pix)

These repositories provided foundational models and software upon which a substantial part of our project was built and trained.

## License

This project is open source and available under the [MIT License](LICENSE). 

**Note**: Please ensure that you comply with the licensing requirements of all incorporated software.

## Contact Information

For any queries or suggestions, please feel free to contact us:

- [Wen Jun](https://github.com/tryhardlaijun)
- [Ye Kai](https://github.com/yekai11)
- [Bing Kang](https://github.com/changbingkang)
- [Jia Xin](https://github.com/mandyjiaxin98)
- [Samantha](https://github.com/samanthalam18)
