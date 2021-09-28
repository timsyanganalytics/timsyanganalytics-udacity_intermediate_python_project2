# Meme Generator

## Overview
This project is an interactive app that generates meme with a quote from an author,
on top of a dog picture. It supports command line inputs for you to customize the
quote and the author. 

TODO: Flask

## Environment
Set up this project on a unique conda environment with python 3.9
`conda create --name meme_generator python=3.9`

Activate the conda environment by `conda activate meme_generator`

Install the required python packages via `pip install -r requirements.txt`, including
python package `pdftotext`. Due to my macOS version, I am not able to install `pdftotext`
via `brew` command (then use subprocess)

## Folder structure

This project

```bash
├── src
│   ├── _data
│   │   ├── **/*.css
│   ├── MemeEngine
│   ├── QuoteEngine
│   ├── app.py
│   ├── meme.py
├── requirements.txt
├── demo.gif
├── README.md
└── .gitignore
```

## How to run?

