import argparse
import asyncio
import json
import logging
import os
from asyncio import Semaphore
from pathlib import Path

import boto3
import botocore
from botocore.exceptions import ClientError

# create console handler with a higher log level
logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(ch)
logger.setLevel(logging.INFO)


class S3CVDownloader:
    def __init__(self, out_dir: Path, aws_account: str, bucket_name: str, semaphore_count: int = 6):
        self.out_dir = out_dir
        self.bucket_name = bucket_name
        self.aws_account = aws_account  # one of {"legacy", "staging"}
        self.semaphore_count = semaphore_count

    async def process(self, document_paths: list[str]):
        session = boto3.Session(profile_name=self.aws_account)
        s3_client = session.client("s3")

        await self.download_files_async(s3_client, document_paths)
        logger.info("Done S3CVDownloader")
        logger.info("*" * 80)

    # ----------------------------------------
    # Download async
    # ----------------------------------------
    async def download_files_async(self, s3_client, document_paths):
        n = len(document_paths)
        sem: Semaphore = asyncio.Semaphore(self.semaphore_count)
        tasks = [self.task(document_path, s3_client, sem, idx, n) for idx, document_path in enumerate(document_paths)]
        await asyncio.gather(*tasks)

    async def task(self, document_path, s3_client, sem: Semaphore, idx, n):
        outpath = self._define_outpath(document_path)
        async with sem:
            if not os.path.exists(outpath):

                # if idx % 1000 == 0:
                logger.info(f"{idx}/{n} Downloading {document_path}")
                self._download_file(s3_client, document_path, outpath)
            else:
                logger.info(f"{idx}/{n}  Skipping. Document path exists:{document_path}")

    def _define_outpath(self, doc_path):
        outpath = Path(self.out_dir).joinpath(doc_path)
        os.makedirs(outpath.parent, exist_ok=True)
        return outpath

    def _download_file(self, s3_client, document_path, outpath):
        try:
            s3_client.download_file(self.bucket_name, document_path, outpath)
        except botocore.exceptions.ClientError as err:
            logger.error("boto error")
            logger.error(err)


# =====================================================================================================================
# Helper functions
# =====================================================================================================================

def uniquify(items):
    return [x for x in set(items) if x]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="input_file", help="input JSONL file")
    parser.add_argument("-o", dest="out_dir", help="output directory")
    parser.add_argument("-a", dest="aws_account", default="legacy", help="AWS profile")
    parser.add_argument("-b", dest="bucket_name", help="S3 Bucket name")
    parser.add_argument("-s", dest="semaphore_count", type=int, default=6, help="Number of semaphores to use")

    args = parser.parse_args()
    logger.info(f"input JSONL file:      {args.input_file}")
    logger.info(f"output directory:      {args.out_dir}")
    logger.info(f"AWS Profile:           {args.aws_account}")
    logger.info(f"S3 Bucket name:        {args.bucket_name}")
    logger.info(f"Semaphore count:       {args.semaphore_count}")

    data = [json.loads(x) for x in open(args.input_file)]
    print(f"len(data): {len(data)} ")
    print(f"type(data): {type(data)} ")
    document_paths = [d["document_path"] for d in data]
    logger.info(f"Number of document paths loaded: {len(document_paths)}")

    document_paths = uniquify(document_paths)
    logger.info(f"Number of unique document paths: {len(document_paths)}")

    downloader = S3CVDownloader(out_dir=args.out_dir,
                                aws_account=args.aws_account,
                                bucket_name=args.bucket_name,
                                semaphore_count=args.semaphore_count)
    asyncio.run(downloader.process(document_paths))
