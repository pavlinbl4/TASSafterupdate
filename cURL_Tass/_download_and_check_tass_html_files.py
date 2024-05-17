# this function download all tass html pages for future work

import requests
from urllib.parse import quote
from must_have.create_sub_directory import create_directory
from must_have.delete_html_folder import delete_folder
from parse_tass_offline import number_of_pages, main_check_downloaded_files

from tass_curl_2 import cookies, headers
from tqdm import trange


def get_response(url):
    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response
    except requests.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None


def save_response_as_html(url, path, filename):
    response = get_response(url)
    if response:
        with open(f"{path}/{filename}.html", 'w', encoding='utf-8') as html_file:
            html_file.write(response.text)


def download_page(page_number, path):
    url = f'https://www.tassphoto.com/ru/asset/fullTextSearch/search/Семен+Лиходеев/page/{page_number}'
    encoded_url = quote(url, safe=':/')
    filename = f'rezult_tass_{page_number}'
    save_response_as_html(encoded_url, path, filename)


def determine_total_pages(path):
    # Download the first page to determine the total number of pages
    download_page(1, path)
    return number_of_pages(f'{path}/rezult_tass_1.html')


def main():
    path_to_html_files = create_directory(".", 'tass_html')
    total_pages = determine_total_pages(path_to_html_files)
    for page_number in trange(1, total_pages + 1, desc='Downloading HTML pages', unit='page'):
        download_page(page_number + 1, path_to_html_files)
    main_check_downloaded_files(path_to_html_files)
    delete_folder(path_to_html_files)


if __name__ == '__main__':
    main()
