import logging
import os
import time
from logging import handlers

import ctranslate2
from transformers import T5Tokenizer

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create file handler that logs debug and higher level messages
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
sh.setFormatter(formatter)

file_logger = bool(os.environ.get("FILE_LOGGER", False))
if file_logger:
    # Set up file handler
    LOGFILE = "LOGS/t5_model.log"
    fh = handlers.RotatingFileHandler(LOGFILE, maxBytes=100000, backupCount=10)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
logger.addHandler(sh)


class S2S:
    TOKENIZER_NEW_WORDS = ["{", "}", "~", "\\", "\n"]

    def __init__(self, model_path, tokenizer_path, device="cuda"):
        logger.debug("-" * 80)
        logger.debug(f"***   device: {device}")
        logger.debug(f"***   model path:     {model_path}  exists:  {os.path.exists(model_path)}")
        logger.debug(f"***   tokenizer path: {tokenizer_path}  exists:  {os.path.exists(tokenizer_path)}")
        logger.debug("-" * 80)
        assert device in ["cuda", "cpu"]

        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        self.device = device.lower()
        self._tokenizer = None
        self._translator = None

    @property
    def tokenizer(self):
        if self._tokenizer is None:
            t1 = time.time()
            tknzr = T5Tokenizer.from_pretrained(self.tokenizer_path)
            new_words = self.TOKENIZER_NEW_WORDS
            tknzr.add_tokens(new_words)
            t2 = time.time()
            logger.info(f"Tokenizer loading time: {(t2 - t1):.2f} sec")
            self._tokenizer = tknzr
        return self._tokenizer

    @property
    def translator(self):
        if self._translator is None:
            t1 = time.time()
            trans = ctranslate2.Translator(model_path=self.model_path, device=self.device, compute_type="default")
            t2 = time.time()
            logger.info(f"Model loading time: {(t2 - t1):.2f} sec")
            self._translator = trans
        return self._translator

    def id_for_token(self, text):
        tokenized_data = self.tokenizer(text, return_length=True, return_tensors="pt")
        input_ids = tokenized_data.input_ids
        return [self.tokenizer.convert_ids_to_tokens([ele]) for ele in input_ids[0]]
