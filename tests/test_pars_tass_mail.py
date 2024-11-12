from unittest import TestCase
import re

from work_with_tass_sales_report.pars_tass_mail import get_year_from_report_date


class TestGetYearFromReportDate(TestCase):
    def test_valid_date(self):

        self.assertEqual(get_year_from_report_date("Report for 2024"), '2024')

    def test_wrong_date(self):
        self.assertEqual(get_year_from_report_date("Report for 024"), 'No 4 digits')

    def test_empty_string(self):
        self.assertEqual(get_year_from_report_date(""), 'No 4 digits')


