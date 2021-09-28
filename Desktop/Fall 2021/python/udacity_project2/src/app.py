"""The Flask app for interactive meme generation purposes."""

import random
import os
import requests
from flask import Flask, render_template, abort, request

from QuoteEngine import QuoteModel, Ingestor_
from MemeEngine import MemeEngine


app = Flask(__name__)

meme = MemeEngine("./static")


def setup():
    """Load all resources.
    
    Returns: 
        - (quotes, imgs): a list of QuoteModel objects, a list of image paths
    """
    quote_files = [
        "./_data/DogQuotes/DogQuotesTXT.txt",
        "./_data/DogQuotes/DogQuotesDOCX.docx",
        "./_data/DogQuotes/DogQuotesPDF.pdf",
        "./_data/DogQuotes/DogQuotesCSV.csv",
    ]

    quotes = []
    for quote_file in quote_files:
        quotes.extend(Ingestor_.parse(quote_file))

    images_path = "./_data/photos/dog/"

    imgs = []
    for file_ in os.listdir(images_path):
        if file_.endswith(".jpg"):
            imgs.append(os.path.join(images_path, file_))  # xander_x.jpg

    return quotes, imgs


quotes, imgs = setup()


@app.route("/")
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template("meme.html", path=path)


@app.route("/create", methods=["GET"])
def meme_form():
    """User input for meme information."""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post():
    """Create a user defined meme."""
    image_url = request.form.get("image_url")
    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            raise Exception("Response unsuccessful!")
    except requests.exceptions.RequestException:
        print("Image URL not valid - please re-enter")

    img_out_path = f"./tmp/meme_{random.randint(0, 1000)}.jpg"

    # Check if this image exists, then remove it
    if os.path.exists(img_out_path):
        os.remove(img_out_path)

    with open(img_out_path, "wb") as outfile:
        outfile.write(response.content)

    body = request.form.get("body")
    author = request.form.get("author")
    quote = QuoteModel(body, author)

    try:
        path = meme.make_meme(img_out_path, quote.body, quote.author)
    except Exception as e:
        print(e)

    # Remove the temp saved image
    if os.path.exists(img_out_path):
        os.remove(img_out_path)

    return render_template("meme.html", path=path)


if __name__ == "__main__":
    app.run()
