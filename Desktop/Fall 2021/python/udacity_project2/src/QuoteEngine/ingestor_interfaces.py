"""This ingestor interfaces engine is.
"""
import os
import docx
import pandas as pd
import pdftotext

from typing import List
from abc import ABC, abstractmethod

from .quote_model import QuoteModel


class IngestorInterface(ABC):
    """Class definition.

    attributes:
        path: file path (should be string type)
        raises type error if input type is not string

        target_file_type: by default empty list, used to define 'can_ingest' method

    methods:
        can_ingest:
            check if the path is legitimate to be ingested
            returns: True / False

        parse (abstractmethod):
            abstractmethod to parse files from types: csv / txt / docx / pdf
            by default set it to 'pass'
    """

    target_file_type = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        file_type = path.split(".")[-1]
        return file_type in cls.target_file_type

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        pass


class CSVIngestorInterface(IngestorInterface):
    """The .csv ingestor interface."""

    target_file_type = ["csv"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:

        if not cls.can_ingest(path):
            file_type = path.split(".")[-1]
            raise Exception(f"Documents of file type {file_type} cannot be ingested")

        df = pd.read_csv(path, header=0)

        assert "body" in df.columns, "Column 'body' not found!"
        assert "author" in df.columns, "Column 'author' not found!"

        return [
            QuoteModel(body, author) for body, author in zip(df["body"], df["author"])
        ]


class TXTIngestorInterface(IngestorInterface):
    """The .txt ingestor interface."""

    target_file_type = ["txt"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:

        if not cls.can_ingest(path):
            file_type = path.split(".")[-1]
            raise Exception(f"Documents of file type {file_type} cannot be ingested")

        bodies = []
        authors = []
        with open(path, "r") as f:
            lines = f.readlines()

        for line in lines:
            bodies.append(line.split(" - ")[0])
            authors.append(line.split(" - ")[1])

        return [QuoteModel(body, author) for body, author in zip(bodies, authors)]


class DOCXIngestorInterface(IngestorInterface):
    """The .docx ingestor interface."""

    target_file_type = ["docx"]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:

        if not cls.can_ingest(path):
            file_type = path.split(".")[-1]
            raise Exception(f"Documents of file type {file_type} cannot be ingested")

        outputs = []
        document = docx.Document(path)

        for paragraph in document.paragraphs:
            body, author = paragraph.text.split(" - ")
            outputs.append(QuoteModel(body, author))

        return outputs


class PDFIngestorInterface(IngestorInterface):
    """The .pdf ingestor interface."""

    target_file_type = ["pdf"]
    TEMP_PATH = "./_data/tmp_pdf_to_txt"

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:

        if not cls.can_ingest(path):
            file_type = path.split(".")[-1]
            raise Exception(f"Documents of file type {file_type} cannot be ingested")

        with open(path, "rb") as f:
            pdf = pdftotext.PDF(f)

        quotes = pdf[0].split("\n")
        quotes = [quote for quote in quotes if " - " in quote]

        outputs = []
        for quote in quotes:
            try:
                body, author = quote.split(" - ")
                outputs.append(QuoteModel(body, author))
                return outputs
            except Exception as e:
                print(e)
