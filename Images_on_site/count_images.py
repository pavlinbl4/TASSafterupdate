from must_have.soup import get_soup, get_html


def get_page_numbers(url):  # get number of images on site
    soup = get_soup(get_html(f'{url}1'))
    images_online = int(str(soup.select(".result-counter#nb-result"))[42:47])
    page_number = images_online // 20 + 1
    return page_number, images_online


if __name__ == '__main__':
    url = 'https://www.tassphoto.com/ru/asset/fullTextSearch/search/' \
          '%D0%A1%D0%B5%D0%BC%D0%B5%D0%BD%20%D0%9B%D0%B8%D1%85%D0%BE%D0%B4%D0%B5%D0%B5%D0%B2/page/'
    print(get_page_numbers(url))
