from must_have.soup import get_soup, get_html


def get_page_numbers(url, browser):  # get number of images on site
    soup = get_soup(get_html(url, browser))
    images_online = int(str(soup.select(".result-counter#nb-result"))[42:47])
    page_number = images_online // 20 + 1
    return page_number, images_online



