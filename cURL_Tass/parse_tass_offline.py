from icecream import ic
from tqdm import trange
from datetime import datetime
from must_have.clear_caption import clear_author
from must_have.files_work import find_files
from must_have.soup import make_soup_from_offline_file
from must_have.u_xlsx_writer import universal_xlsx_writer


def thumbs_date_on_page(soup):
    # thumbs_data - all information about image
    thumbs_data = soup.find('ul', id="mosaic").find_all('div', class_="thumb-content thumb-width thumb-height")
    images_on_page = len(soup.find('ul', id="mosaic").find_all('a', class_="zoom"))
    return thumbs_data, images_on_page


def number_of_pages(offline_html):
    soup = make_soup_from_offline_file(offline_html)
    # ic(soup.find('span', class_="count-pages").text)
    return soup.find('span', class_="count-pages").text


def image_info(thumbs_data, images_on_page):
    for image_number_on_page in trange(images_on_page, desc=f'Check page', colour='Green'):
        image_date = thumbs_data[image_number_on_page].find(class_="date").text
        image_id = thumbs_data[image_number_on_page].find(class_="title").text
        # image_title = thumbs_data[image_number_on_page].find('p').text
        image_caption = (thumbs_data[image_number_on_page].find('br')
                         .next_sibling.next_sibling.next_sibling.strip()
                         .replace(' Семен Лиходеев/ТАСС', '')).strip()
        image_pr_link = thumbs_data[image_number_on_page].find('img').get('src')

        image_caption = clear_author(image_caption)

        print(f'\n{image_number_on_page = }')
        print(image_id, image_date, image_caption)
        print(f'{image_pr_link = }')

        row_data = (image_id, image_date, image_caption, image_pr_link)

        today_date = f'{datetime.now().strftime("%d.%m.%Y")}'

        # save data to xlsx file
        universal_xlsx_writer(row_data=row_data,
                              columns_names=('image_id',
                                             'image date',
                                             'image caption',
                                             'image link'),
                              file_path='/Volumes/big4photo/Documents/TASS/Tass_data/added_TASS_images.xlsx',
                              sheet_name=today_date,
                              column_width=(15, 15, 110, 50))


def get_data(offline_html):
    soup = make_soup_from_offline_file(offline_html)
    thumbs_data, images_on_page = thumbs_date_on_page(soup)
    image_info(thumbs_data, images_on_page)


def main_check_downloaded_files(path_to_html_files):
    all_html_files = find_files(path_to_html_files, 'html')

    for file_number in trange(1, len(all_html_files) + 1, desc=f'Check pages', colour='Blue'):
        print(f'Page -  rezult_tass_{file_number}\n{"*" * 190}')
        get_data(f'{path_to_html_files}/rezult_tass_{file_number}.html')


if __name__ == '__main__':
    main_check_downloaded_files('tass_html')

    # ic(number_of_pages('tass_html/rezult_tass_1.html'))

    # check parsing of one page
    # get_data('tass_html/rezult_tass_1.html')

    # get_data(f'tass_html/rezult_tass_1.html')
