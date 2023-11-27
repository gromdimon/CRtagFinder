# net_file_utils.py

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import wget
import pathlib
import logging

def create_session_with_retries():
    """
    Create a requests session with retry capabilities.
    """
    session = requests.Session()
    retries = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def download_file(url, destination):
    """
    Download a file from a URL to a specified destination.
    :param url: URL of the file to be downloaded.
    :param destination: Path where the file will be saved.
    """
    try:
        wget.download(url, destination)
    except Exception as e:
        logging.error(f"Error downloading file from {url}: {e}")

def read_file(file_path):
    """
    Read the content of a file.
    :param file_path: Path of the file to be read.
    :return: Content of the file.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return None

def write_file(file_path, content):
    """
    Write content to a file.
    :param file_path: Path of the file to be written to.
    :param content: Content to be written to the file.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        logging.error(f"Error writing to file {file_path}: {e}")

def append_to_file(file_path, content):
    """
    Append content to a file.
    :param file_path: Path of the file to be appended to.
    :param content: Content to be appended to the file.
    """
    try:
        with open(file_path, 'a') as file:
            file.write(content)
    except Exception as e:
        logging.error(f"Error appending to file {file_path}: {e}")
