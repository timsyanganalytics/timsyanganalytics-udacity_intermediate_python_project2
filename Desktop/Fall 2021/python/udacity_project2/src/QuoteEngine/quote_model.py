"""The script to define the QuoteModel class
which encapsulates the body and author
"""


class QuoteModel:
    """The definition of the class"""

    def __init__(self, body, author):
        self.body = body
        self.author = author

    def __str__(self):
        """Print the quote from a QuoteModel object.
        In the format of '{body} - {author}'
        """
        return f"{self.body} - {self.author}"
