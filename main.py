import pandas as pd
import matplotlib as mp
import zipfile

ARCHIVE_PATH = "data/archive.zip"
DESTINATION_PATH = "data/"
def un_zipper(zip_path: str, dest_path: str):

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract all the contents of the zip file to the specified directory
        zip_ref.extractall(dest_path)

un_zipper(ARCHIVE_PATH, DESTINATION_PATH)

