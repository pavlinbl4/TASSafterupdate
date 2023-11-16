# this function download all tass html pages for future work

import requests
from urllib.parse import quote

from must_have.create_sub_directory import create_directory
from must_have.delete_html_folder import delete_folder
from parse_tass_offline import number_of_pages, main_check_downloaded_files

from tass_curl import cookies, headers
from tqdm import trange


def get_response(url):
    response = requests.get(
        url=url,
        cookies=cookies,
        headers=headers,
    )
    return response


def save_response_as_html(url, path_to_html_files):
    response = get_response(url)

    with open(f"{path_to_html_files}/rezult_tass_{url.split('/')[-1]}.html", 'w') as html_file:
        html_file.write(response.text)


def page_pagination(page_number, path_to_html_files):
    url = f'https://www.tassphoto.com/ru/asset/fullTextSearch/search/Семен+Лиходеев/page/{page_number}'
    url = quote(url, safe=':/')
    save_response_as_html(url, path_to_html_files)


def find_pages_number(path_to_html_files):
    #  how many pages I want to save

    # save first page
    page_pagination(1, path_to_html_files)

    # get amount of pages from first html file
    return number_of_pages(f'{path_to_html_files}/rezult_tass_1.html')


def main():
    # create directory to html files
    path_to_html_files = create_directory(".", 'tass_html')

    # find number of pages to parce
    pages_count = int(find_pages_number(path_to_html_files))

    #  start to save pages from number 2
    for i in trange(1, pages_count + 1, desc='Downloading html pages', colour='Green'):
        page_pagination(i + 1, path_to_html_files)

    main_check_downloaded_files(path_to_html_files)
    delete_folder(path_to_html_files)


if __name__ == '__main__':
    main()
