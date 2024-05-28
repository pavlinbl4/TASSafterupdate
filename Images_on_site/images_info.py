def get_image_caption(i, soup):
    if soup.find('ul', id="mosaic") is not None:
        image_caption = soup.find('ul', id="mosaic").find_all(class_="thumb-text")[i].text.strip().split('\n')[
            -1].lstrip().replace(' Семен Лиходеев/ТАСС', '').replace(' Фото ИТАР-ТАСС/ Семен Лиходеев', '')
    else:
        image_caption = "Some problem with caption"
    return image_caption
