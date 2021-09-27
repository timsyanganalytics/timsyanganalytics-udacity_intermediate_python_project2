from typing import List

from .quote_model import QuoteModel
from .ingestor_interfaces import (
    IngestorInterface,
    CSVIngestorInterface,
    TXTIngestorInterface,
    DOCXIngestorInterface,
    PDFIngestorInterface,
)


class Ingestor_(IngestorInterface):
    """The ingestor class to consolidate all 4 ingestor interfaces"""

    ingestor_types = [
        CSVIngestorInterface,
        TXTIngestorInterface,
        DOCXIngestorInterface,
        PDFIngestorInterface,
    ]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        try:
            path_type = path.split(".")[-1]
            if path_type.lower() == "csv":
                return CSVIngestorInterface.parse(path)
            elif path_type.lower() == "txt":
                return TXTIngestorInterface.parse(path)
            elif path_type.lower() == "docx":
                return DOCXIngestorInterface.parse(path)
            elif path_type.lower() == "pdf":
                return PDFIngestorInterface.parse(path)
            else:
                raise NameError("Illegitimate path name !")
        except Exception as e:
            print(e)
