"""
As requested  by the company:

 * Get local or a remote file as input;
 * Categorize to know if the input file is a json or a csv;
 * Sort locations by the number of the clients on it.
"""
import os
import requests
import tablib
import validators


#Avoid 403 on pages that check user agents.
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)" \
             " Chrome/44.0.2403.157 Safari/537.36"

def check_is_local_file(input_file: str) -> str:
    """
    Check if the passed para is a valid file.
    """
    if os.path.isfile(input_file):
        with open(input_file, 'r', newline='') as localfile:
            content = localfile.read()
            return content

    return False


def check_is_remote_file(input_file: str) -> str:
    """
    Check if the file address passed is a valid URL.
    """
    if not validators.url(input_file):
        return False

    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(input_file, headers=headers)
    except (requests.exceptions.ConnectionError,):
        return False

    if response.status_code != 200:
        return False

    return response.text


def get_file_content(input_file: str) -> str:
    """
    Check and get the filename supplied.
    """
    ## Implement Custom Exceptions?
    islocal = check_is_local_file(input_file)
    isremote = check_is_remote_file(input_file)

    if not (islocal or isremote):
        raise Exception("""The supplied file name is not a valid local
                        or remote resource. Please check it and try again.""")

    content = [value for value in [islocal, isremote] if value]

    return content[0]

def parse_content(input_data: str) -> tablib.Dataset:
    """
    Parse content with 
    """
    try:
        dataset = tablib.Dataset().load(input_data)
    except  (tablib.core.UnsupportedFormat,):
        raise 

    return dataset
