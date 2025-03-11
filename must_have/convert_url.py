from urllib.parse import quote,unquote

url = 'https://www.tassphoto.com/ru/asset/fullTextSearch/search/Семен+Лиходеев/page/1'
encoded_url = quote(url, safe=':/')

url = 'https://www.tassphoto.com/ru/asset/fullTextSearch/search/%D0%92%D0%B0%D0%BB%D0%B5%D0%BD%D1%82%D0%B8%D0%BD%20%D0%90%D0%BD%D1%82%D0%BE%D0%BD%D0%BE%D0%B2%2F%D0%A2%D0%90%D0%A1%D0%A1/page/1'
decoded_url = unquote(url)
print(encoded_url)
print(decoded_url)