
import os
import shutil


def clean_dir(directory: str):
    if os.path.exists(directory):
        shutil.rmtree(directory)