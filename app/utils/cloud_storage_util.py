import re
import shutil
from pathlib import Path

from google.cloud import storage

import const


class CloudStorageUtil:

    @staticmethod
    def download_file_via_regex(bucket_name: str, pattern: str, directory: Path) -> list[Path]:

        print(f'Downloading files via pattern: {pattern}')

        storage_client = storage.Client(project=const.PROJECT_ID)

        bucket = storage_client.bucket(bucket_name)

        blobs = bucket.list_blobs()

        count = 0

        files: [Path] = []

        for blob in blobs:

            match = re.search(pattern, blob.name)
            if match:
                # This blob is not a directory
                f = directory.joinpath(blob.name.split('/')[-1])
                print(f'Downloading "{blob.name}" file')
                blob.download_to_filename(f)
                count += 1
                files.append(f)

        print(f'Downloaded {len(files)} files')
        return files


    @staticmethod
    def upload_blob_from_memory(bucket_name, contents, destination_blob_name, content_type: str = None):
        """Uploads a file to the bucket."""

        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The contents to upload to the file
        # contents = "these are my contents"

        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        storage_client = storage.Client(project=const.PROJECT_ID)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        if content_type:
            blob.upload_from_string(contents, content_type=content_type)
        else:
            blob.upload_from_string(contents)

        print(f"{destination_blob_name} uploaded to {bucket_name}.")

    @staticmethod
    def upload_blob_from_filesystem(bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""

        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"

        # The contents to upload to the file
        # contents = "these are my contents"

        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"

        storage_client = storage.Client(project=const.PROJECT_ID)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Optional: set a generation-match precondition to avoid potential race conditions
        # and data corruptions. The request to upload is aborted if the object's
        # generation number does not match your precondition. For a destination
        # object that does not yet exist, set the if_generation_match precondition to 0.
        # If the destination object already exists in your bucket, set instead a
        # generation-match precondition using its generation number.
        generation_match_precondition = None

        blob.upload_from_filename(source_file_name, if_generation_match=generation_match_precondition)

        print(f"{destination_blob_name} uploaded to {bucket_name}.")
