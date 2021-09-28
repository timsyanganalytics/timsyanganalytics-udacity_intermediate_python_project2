"""Class MemeEngine.
Main functionality:
    - load image using Pillow (PIL)
    - resize the image with max width at 500px,
        and the height is scaled proportionally
    - add a quote body and a quote author to the image
    - save the manipulated image
    - implement the instance method that returns the path to the manipulated image
        make_meme(self, img_path, text, author, width=500) -> str
"""
import os
import random

from PIL import Image, ImageFont, ImageDraw


class MemeEngine:

    acceptable_image_path_type = ["jpg"]

    def __init__(self, output_dir: str):
        """Instantiates a MemeEngine onject.

        Args:
            image_path (str): path of the image to be loaded from
            quotes (List(QuoteModel)): list of loaded quotes to be added to the images
            width (int / float): the maximum width to resize the images into
        """
        self.output_dir = output_dir
        assert isinstance(self.output_dir, str), "Image path must be string"

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _can_ingest_image(self, img_path):
        """Determine if the image can be ingested, by checking if
        the image is of jpg type

        Returns:
            - (boolean) True / False
        """
        image_path_type = img_path.split(".")[-1]
        return image_path_type in self.acceptable_image_path_type

    def _load_image(self, img_path: str):
        """Function to load the image

        first check if the image can be loaded

        Returns:
            - an image object (Image object)
        """
        if self._can_ingest_image(img_path):
            return Image.open(img_path)
        else:
            raise Exception("Image must be of jpg files")

    def _resize_image(self, image, width):
        """Function to resize image by the width specified

        Args:
            image: the image object that is loaded by `load_image` function

        Returns:
            new_image: resized image
        """
        try:
            _width, _height = image.size
            shrinkage = width / _width
            new_width, new_height = int(round(width)), int(round(_height * shrinkage))
            new_image = image.resize((new_width, new_height))
        except Exception as e:
            print(e)
        return new_image

    def _add_quote_body_author_to_image(
        self,
        image,
        body,
        author,
    ):
        """Add quote body and author to the image.

        credit to stackoverflow page:
        https://stackoverflow.com/questions/47694421/pil-issue-oserror-cannot-open-resource

        Args:
            image: the image object that is loaded by `load_image` function
                and resized by `resize_image` function

        Returns:
            images that has quotes and authors
        """
        draw = ImageDraw.Draw(image)
        width, height = image.size
        try:
            font = ImageFont.truetype(
                "./fonts/DejaVuSans.ttf", size=20, encoding="utf-8"
            )
        except Exception as e:
            print(e)

        text = f"{body} - {author}"

        draw.text(
            (width / 16, height * random.randint(2, 8) / 16),
            text,
            fill=(random.randint(0, 255), 0, 0),
            font=font,
        )

        return image

    def _save_image(self, image):
        """Save image to the right output path, and return the output path.

        Args:
            - image: image object (Image object)

        Returns:
            - output_path: output path
        """
        image_output_name = f"meme_{random.randint(0, 1000)}.jpg"
        output_path = os.path.join(self.output_dir, image_output_name)
        image.save(output_path)
        return output_path

    def make_meme(self, img_path, text, author, width=500) -> str:
        """ """

        if text is None and author is None:
            raise Exception("Please specify a text and an author!")

        image = self._load_image(img_path)
        new_image = self._resize_image(image, width)
        new_image = self._add_quote_body_author_to_image(new_image, text, author)
        output_path = self._save_image(new_image)
        return output_path
