from unittest import TestCase

from Images_on_site.count_images import get_page_numbers


class FindMyNameTest(TestCase):
    def test_get_page_numbers(self):
        self.assertTrue(get_page_numbers(url)) is tuple


url = 'https://www.tassphoto.com/ru/asset/fullTextSearch/search/' \
          '%D0%A1%D0%B5%D0%BC%D0%B5%D0%BD%20%D0%9B%D0%B8%D1%85%D0%BE%D0%B4%D0%B5%D0%B5%D0%B2/page/'
