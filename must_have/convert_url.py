from urllib.parse import quote

url = 'https://www.tassphoto.com/ru/asset/fullTextSearch/search/Семен+Лиходеев/page/1'
encoded_url = quote(url, safe=':/')

print(encoded_url)