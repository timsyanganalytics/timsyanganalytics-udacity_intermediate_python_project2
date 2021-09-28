"""The __init__ module for MemeEngine subpackage."""

from .ingestor_interfaces import (
    IngestorInterface,
    CSVIngestorInterface,
    TXTIngestorInterface,
    DOCXIngestorInterface,
    PDFIngestorInterface,
)
from .quote_model import QuoteModel
from .ingestor import Ingestor_
