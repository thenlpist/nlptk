import logging
import os.path
import re
from pathlib import Path

import mammoth
import pymupdf
from markdownify import markdownify as md

from nlptk import PreProcess

logger = logging.getLogger(__name__)
LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logger.setLevel(LOGLEVEL)
# create file handler that logs debug and higher level messages
sh = logging.StreamHandler()
sh.setLevel(LOGLEVEL)
formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
sh.setFormatter(formatter)
logger.addHandler(sh)


class FileReader:
    ENCODING = "utf-8"
    TMP_PREFIX = "tmp"
    TMP_DIR = "TMP_FILES"

    # def __init__.py(self, filename, file_obj: tempfile.SpooledTemporaryFile):
    def __init__(self):
        self.prep = PreProcess()

    def parse_document(self, path: Path):
        extension = path.suffix.lower()
        match extension:
            case ".docx":
                logger.info("Docx filetype detected")
                text = self._parse_docx(path)
            case ".pdf":
                logger.info("PDF filetype detected")
                text = self._parse_pdf(path)
            case ".txt":
                logger.info("Txt filetype detected")
                text = self._parse_txt(path)
            case _:
                logger.warning(
                    f"Unknown filetype {extension} detected. Must be one of .docx, .pdf, or .txt"
                )
                text = self._unrecognized(path)
        # self._remove_tmp_file()
        text = self.prep.process(text)
        return text

    def extract_text(self, path: Path) -> str:
        text = self.parse_document(path)
        return text

    def _normalize_filename(self, filename):
        p = Path(filename)
        if p.suffix.lower() == ".doc":
            return str(p.with_suffix(".docx"))
        else:
            return filename

    # def _get_tmp_file_path(self):
    #     return f"{self.TMP_DIR}/{self.TMP_PREFIX}_{str(Path)}"

    # def _remove_tmp_file(self):
    #     tmp_file = self._get_tmp_file_path()
    #     if os.path.exists(tmp_file):
    #         logger.debug(f"deleting temp file: {tmp_file}")
    #         os.remove(tmp_file)

    # def _persist_temp_data(self, byte_data):
    #     os.makedirs(self.TMP_DIR, exist_ok=True)
    #     try:
    #         logger.debug(f"persisting temp file: {self._get_tmp_file_path()}")
    #         with open(self._get_tmp_file_path(), "wb") as fo:
    #             fo.write(byte_data)
    #     except Exception:
    #         logger.error(f"There was an error persisting temp file for {self.filename}")

    # --------------------
    #  Parse Docx files
    # --------------------
    def _parse_docx(self, path):
        try:
            html = self._docx_to_html(path)
            md_text = self._html_to_markdown(html)
            logger.debug(f"Docx md_text length: {len(md_text)}")
            return md_text
        except Exception as e:
            logger.error(e)
            return ""

    # --------------------
    # Parse PDF files
    # --------------------
    def _parse_pdf(self, path):
        try:
            html = self._any_doc_to_html(path)
            md_text = self._html_to_markdown(html)
            logger.debug(f"PDF md_text length: {len(md_text)}")
            # if pdf is an image it can't be parsed and will return an empty string
            if len(md_text.strip()) == 0:
                logger.error(
                    f"PDF is empty after extracting text for file: {path.name}"
                )
            return md_text
        except Exception as e:
            logger.error(e)
            return ""

    def _docx_to_html(self, docx_file):
        # Convert <b> bold to <h2> tags
        # custom_styles = "b => h2"

        with open(docx_file, "rb") as docx_file:
            # result = mammoth.convert_to_html(docx_file, style_map=custom_styles)
            result = mammoth.convert_to_html(docx_file)
            html = re.sub("</?(table|thead|tr|th|td)>", "", result.value)
            return html

    def _any_doc_to_html(self, path):
        """Use library PymuPDF to parse document to text"""
        text = ""
        doc = pymupdf.open(path)
        for page in doc:  # iterate the document pages
            # text += page.get_text("html")
            text += page.get_text("xhtml")  # simpler html converter
        # Get rid of duplicate headings
        text = re.sub("<h2><h2>", "<h2>", text)
        text = re.sub("</h2></h2>", "</h2>", text)
        return text

    # --------------------
    # Parse PDF files. Deprecated
    # --------------------
    # def _pdf_to_text(self):
    #     """Use library PyPDF2 to parse PDF document to text"""
    #     text = ""
    #     doc = PyPDF2.PdfReader(self.file_obj)
    #     for page in doc.pages:
    #         text += page.extract_text()
    #     return StatusCode.OK, text

    # --------------------------------------------------------------------------------
    # Convert HTML to Markdown
    # --------------------------------------------------------------------------------
    def _html_to_markdown(self, html):
        html = re.sub("<(br|hr)>", "\n", html)
        html = re.sub("&nbsp;", " ", html)
        html = re.sub("(</?)h([1-2])>", r"\n\1h2>\n", html)
        # remove headers below <h2>
        html = re.sub("(</?)h([3-9])>", "", html)
        # normalize headers to h2
        # html = re.sub("(</?)h([1-9])>", r"\1h2>", html)
        return md(
            html,
            heading_style="ATX",
            escape_asterisks=False,
            escape_underscores=False,
            escape_misc=False,
            bullets=["-"],
            strip=["img", "b", "i", "em", "strong"],
        )

    # --------------------
    #  Parse Txt files
    # --------------------
    def _parse_txt(self, path):
        try:
            text = open(path).read()
            if isinstance(text, bytes):
                logger.debug(f"Txt file is loaded as bytes: {path.name}")
                text = text.decode(self.ENCODING)
            logger.debug(f"Txt text length: {len(text)}")
            return text
        except:
            return ""

    # --------------------
    #  Handle unrecognized files
    # --------------------
    def _unrecognized(self, path):
        logger.warning(f"Unsupported filetype for document: {path.name}")
        return ""
