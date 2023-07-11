from Images_on_site.count_images import get_page_numbers
from Images_on_site.first_enter import first_enter


def extract_images_info(images_on_page, thumbs_data, soup, count):
    for i in range(images_on_page):
        image_date = thumbs_data[i].find(class_="date").text
        image_id = thumbs_data[i].find(class_="title").text
        image_title = thumbs_data[i].find('p').text
        if soup.find('ul', id="mosaic") is not None:
            image_caption = soup.find('ul', id="mosaic").find_all(class_="thumb-text")[i].text.strip().split('\n')[
                -1].lstrip().replace(' Семен Лиходеев/ТАСС', '').replace(' Фото ИТАР-ТАСС/ Семен Лиходеев', '')
        else:
            image_caption = "Some problem with caption"
        image_link = soup.find('ul', id="mosaic").find_all('a', class_="zoom")[i].find('img').get('src')
        count += 1
        print(count, image_id, image_date)
        print(image_title)
        print(image_caption)
        print(image_link)
    return count


def images_on_page_info(soup):
    thumbs_data = soup.find('ul', id="mosaic").find_all('div', class_="thumb-content thumb-width thumb-height")
    images_on_page = len(soup.find('ul', id="mosaic").find_all('a', class_="zoom"))
    return thumbs_data, images_on_page


def main():
    browser = first_enter()
    page_number, images_online = get_page_numbers(url, browser)  # 2. get number of images on site
    print(f'{page_number = }')
    return browser


url = 'https://www.tassphoto.com/ru/asset/fullTextSearch/search/' \
      '%D0%A1%D0%B5%D0%BC%D0%B5%D0%BD%20%D0%9B%D0%B8%D1%85%D0%BE%D0%B4%D0%B5%D0%B5%D0%B2/page/'

if __name__ == '__main__':
    # start = rotate_page()
    start = main()
    start.close()
    start.quit()
