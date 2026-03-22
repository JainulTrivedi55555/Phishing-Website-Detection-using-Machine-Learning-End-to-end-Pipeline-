import os

from networksecurity.logging.logger import logging


class S3Sync:
    def sync_folder_to_s3(self, folder, aws_bucket_url):
        logging.info(f"S3 sync skipped (no AWS configured): {folder} -> {aws_bucket_url}")

    def sync_folder_from_s3(self, folder, aws_bucket_url):
        logging.info(f"S3 sync skipped (no AWS configured): {aws_bucket_url} -> {folder}")
