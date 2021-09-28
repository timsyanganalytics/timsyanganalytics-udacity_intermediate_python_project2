import os
import random
import argparse

from QuoteEngine import QuoteModel, Ingestor_
from MemeEngine import MemeEngine


OUTPUT_PATH = "./tmp"

def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = [
            './_data/DogQuotes/DogQuotesTXT.txt',
            './_data/DogQuotes/DogQuotesDOCX.docx',
            './_data/DogQuotes/DogQuotesPDF.pdf',
            './_data/DogQuotes/DogQuotesCSV.csv'
        ]
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor_.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    # Check if output path already exists
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    meme = MemeEngine(OUTPUT_PATH)
    path = meme.make_meme(img, quote.body, quote.author)
    return path


def make_args():
    """Create an ArgumentParser for this script.
    
    :return: A tuple of the path, body and author parsers.
    """

    parser = argparse.ArgumentParser(
        description="Load an image and texts to generate meme."
    )
    parser.add_argument(
        "--path",
        type=str,
        help="The path of the image to generate a meme",
    )
    parser.add_argument(
        "--body",
        type=str,
        help="The main text to be put on the image",
    )
    parser.add_argument(
        "--author",
        type=str,
        help="The author of the main text to be put on the image",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = make_args()
    print(generate_meme(args.path, args.body, args.author))
