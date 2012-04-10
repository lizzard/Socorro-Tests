#!/usr/bin/env python
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from pages.page import Page
from pages.base import CrashStatsBasePage
from selenium.webdriver.support.select import Select


class CrashStatsHomePage(CrashStatsBasePage):
    '''
        Page Object for Socorro
        https://crash-stats.allizom.org/
    '''
    _first_product_top_crashers_link_locator = (By.CSS_SELECTOR, '.release_channel > ul > li:nth-of-type(1) > a')
    _top_crashers_regions_locator = (By.CSS_SELECTOR, '.release_channel')
    _top_crashers_elements_locator = (By.CSS_SELECTOR, 'ul > li:nth-of-type(1) > a')
    _top_changers_elements_locator = (By.CSS_SELECTOR, '.release_channel > ul > li:nth-of-type(2) > a')
    _top_selected_locator = (By.CSS_SELECTOR, '.selected')

    def __init__(self, testsetup, product=None):
        '''
            Creates a new instance of the class and gets the page ready for testing
        '''
        CrashStatsBasePage.__init__(self, testsetup)

        if product is None:
            self.selenium.get(self.base_url)

    def click_on_top_(self, element):
        topElement = self.selenium.find_element(*getattr(self, 'link=Top %s' % element))
        topElement.click()
        if element == 'Changers':
            self.find_element(*self._top_changers_elements_locator).find_element(*self._top_selected_locator).is_displayed()
        else:
            self.find_element(*self._top_crashers_regions_locator).find_element(*self._top_crashers_elements_locator).find_element(*self._top_selected_locator).is_displayed()

    def click_first_product_top_crashers_link(self):
        self.selenium.find_element(*self._first_product_top_crashers_link_locator).click()
        return CrashStatsTopCrashers(self.testsetup)

    @property
    def top_crashers(self):
        return [self.CrashReportsRegion(self.testsetup, element) for element in self.selenium.find_elements(*self._top_crashers_regions_locator)]

    class CrashReportsRegion(CrashStatsBasePage):

        _elements_locator = (By.CSS_SELECTOR, 'li:nth-of-type(1) > a')
        _header_release_channel_locator = (By.CSS_SELECTOR, 'h4')

        def __init__(self, testsetup, element):
            CrashStatsBasePage.__init__(self, testsetup)
            self._root_element = element

        @property
        def version_name(self):
            return self._root_element.find_element(*self._header_release_channel_locator).text

        def click_top_crasher(self):
            self._root_element.find_element(*self._elements_locator).click()
            return CrashStatsTopCrashers(self.testsetup)


class CrashReport(Page):

    _reports_tab_locator = (By.ID, 'reports')
    _reports_row_locator = (By.CSS_SELECTOR, '#reportsList tbody tr')
    _report_tab_button_locator = (By.CSS_SELECTOR, '#report-list-nav li:nth-of-type(4) > a')

    @property
    def reports(self):
        return [self.Report(self.testsetup, element) for element in self.selenium.find_elements(*self._reports_row_locator)]

    def click_reports(self):
        self.selenium.find_element(*self._report_tab_button_locator).click()
        WebDriverWait(self.selenium, 10).until(lambda s: self.is_element_visible(None, *self._reports_tab_locator))

    class Report(Page):
        _product_locator = (By.CSS_SELECTOR, 'td:nth-of-type(3)')
        _version_locator = (By.CSS_SELECTOR, 'td:nth-of-type(4)')

        def __init__(self, testsetup, element):
            Page.__init__(self, testsetup)
            self._root_element = element

        @property
        def product(self):
            return self._root_element.find_element(*self._product_locator).text

        @property
        def version(self):
            return self._root_element.find_element(*self._version_locator).text


class CrashStatsAdvancedSearch(CrashStatsBasePage):
    #https://crash-stats.allizom.org/query/query
    # This po covers both initial adv search page and also results
    _page_title = 'Query Results - Mozilla Crash Reports'

    _product_multiple_select = (By.ID, 'product')
    _version_multiple_select = (By.ID, 'version')
    _os_multiple_select = (By.ID, 'platform')
    _filter_crash_reports_button = (By.ID, 'query_submit')
    _data_table = (By.CSS_SELECTOR, '#signatureList')
    _data_table_first_signature = (By.CSS_SELECTOR, 'table#signatureList > tbody > tr > td > a')
    _data_table_first_signature_results = (By.CSS_SELECTOR, 'table#signatureList > tbody > tr > td:nth-child(3)')

    _query_results_text = (By.CSS_SELECTOR, '.body.notitle p')

    _build_id_locator = (By.ID, 'build_id')

    _radio_items_locator = (By.CSS_SELECTOR, '.radio-item > label > input')

    _data_table_signature_column_locator = (By.CSS_SELECTOR, 'table#signatureList > tbody > tr > td:nth-child(2)')
    _data_table_signature_browser_icon_locator = (By.CSS_SELECTOR, 'div > img.browser')
    _data_table_signature_plugin_icon_locator = (By.CSS_SELECTOR, 'div > img.plugin')
    _next_locator = (By.CSS_SELECTOR, '.pagination>a:contains("Next")')
    _plugin_filename_header_locator = (By.CSS_SELECTOR, 'table#signatureList  thead .header:nth-of-type(3)')
    _data_table_rows_locator = (By.CSS_SELECTOR, 'tbody > tr td:nth-of-type(2) > a')

    def adv_select_product(self, product):
        element = self.selenium.find_element(*self._product_multiple_select)
        select = Select(element)
        select.select_by_visible_text(product)

    def adv_select_version(self, version):
        element = self.selenium.find_element(*self._version_multiple_select)
        select = Select(element)
        select.select_by_visible_text(version)

    def adv_select_os(self, os):
        element = self.selenium.find_element(*self._os_multiple_select)
        select = Select(element)
        select.select_by_visible_text(os)

    def filter_reports(self):
        self.selenium.find_element(*self._filter_crash_reports_button).click()

    def click_first_signature(self):
        self.selenium.find_element(*self._data_table_first_signature).click()
        return CrashStatsSignatureReport(self.testsetup)

    def build_id_field_input(self, value):
        self.selenium.find_element(*self._build_id_locator).send_keys(value)

    @property
    def build_id(self):
        return str(self.selenium.execute_script('navigator.buildID'))

    @property
    def first_signature_name(self):
        return self.selenium.find_element(*self._data_table_first_signature).text

    @property
    def first_signature_number_of_results(self):
        return self.selenium.find_element(*self._data_table_first_signature_results).text

    @property
    def currently_selected_product(self):
        element = self.selenium.find_element(*self._product_multiple_select)
        select = Select(element)
        return select.first_selected_option.text

    @property
    def product_list(self):
        return [element.text for element in self.selenium.find_elements(*self._product_multiple_select)]

    @property
    def results_found(self):
        try:
            return len(self.selenium.find_elements(*self._data_table_rows_locator)) > 0
        except NoSuchElementException:
            return False

    @property
    def results_count(self):
        try:
            return len(self.selenium.find_element(*self._data_table).find_elements(By.CSS_SELECTOR, '> tbody > tr'))
        except NoSuchElementException:
            return 0

    def query_results_text(self, index):
        result = self.selenium.find_elements(*self._query_results_text)
        return result[index].text

    def select_radio_button(self, lookup):
        radio_buttons = self.selenium.find_elements(*self._radio_items_locator)
        radio_buttons[lookup].click()

    @property
    def is_plugin_icon_visible(self):
        return self.selenium.find_element(*self._data_table_signature_column_locator).find_element(*self._data_table_signature_plugin_icon_locator).is_displayed()

    @property
    def is_browser_icon_visible(self):
        return self.selenium.find_element(*self._data_table_signature_column_locator).find_element(*self._data_table_signature_browser_icon_locator).is_displayed()

    def click_next(self):
        self.selenium.find_element(*self._next_locator).click()

    def click_plugin_filename_header(self):
        self.selenium.find_element(*self._plugin_filename_header_locator).click()

    def plugin_filename_results_list(self):
        # TODO remove lower() pending resolution of: https://github.com/AutomatedTester/unittest-zero/issues/9
        return [(self.selenium.get_text('%s tr:nth(%s) > td:nth-child(3)' % (self._data_table, (i + 1)))).lower() for i in range(0, self.results_count)]


class CrashStatsSignatureReport(CrashStatsBasePage):

    # https://crash-stats.allizom.org/report/list?

    _total_items = (By.CSS_SELECTOR, 'span.totalItems')
    _reports_page_locator = (By.CSS_SELECTOR, '.ui-state-default.ui-corner-top:nth-of-type(4) > a > span')

    def click_reports(self):
        self.selenium.find_element(*self._reports_page_locator).click()

    @property
    def total_items_label(self):
        return self.selenium.find_element(*self._total_items).text.replace(",", "")


class CrashStatsPerActiveDailyUser(CrashStatsBasePage):

    _page_title = 'Crashes per Active Daily User for Firefox'

    _product_select_locator = (By.ID, 'daily_search_version_form_products')
    _date_start_locator = (By.CSS_SELECTOR, '.daily_search_body .date[name="date_start"]')
    _generate_button_locator = (By.ID, 'daily_search_version_form_submit')
    _table_locator = (By.ID, 'crash_data')
    _row_table_locator = (By.CSS_SELECTOR, '#crash_data > tbody > tr')
    _last_row_date_locator = (By.CSS_SELECTOR, '#crash_data > tbody > tr > td:nth-child(1):not(:last):last')

    @property
    def product_select(self):
        element = self.selenium.find_element(*self._product_select_locator)
        select = Select(element)
        return select.first_selected_option.text

    def type_start_date(self, date):
        date_element = self.selenium.find_element(*self._date_start_locator)
        date_element.clear()
        date_element.send_keys(date)

    def click_generate_button(self):
        self.selenium.find_element(*self._generate_button_locator).click()

    @property
    def is_mixed_content_warning_shown(self):
        return self.is_alert_present()

    @property
    def is_table_visible(self):
        return self.is_element_visible(None, *self._table_locator)

    @property
    def table_row_count(self):
        return len(self.selenium.find_elements(self._row_table_locator))

    @property
    def last_row_date_value(self):
        return self.selenium.find_element(*self._last_row_date_locator).text


class CrashStatsTopCrashers(CrashStatsBasePage):

    _page_heading_product_locator = (By.ID, 'current-product')
    _page_heading_version_locator = (By.ID, 'current-version')

    _filter_by_locator = (By.CSS_SELECTOR, '.tc-duration-type.tc-filter > li > a')
    _filter_days_by_locator = (By.CSS_SELECTOR, '.tc-duration-days.tc-filter > li > a')
    _current_days_filter_locator = (By.CSS_SELECTOR, 'ul.tc-duration-days li a.selected')
    _current_filter_type_locator = (By.CSS_SELECTOR, 'ul.tc-duration-type li a.selected')

    _data_table = (By.ID, 'signatureList')
    _signature_table_row_locator = (By.CSS_SELECTOR, '#signatureList tbody tr')

    @property
    def page_heading_product(self):
        return self.selenium.find_element(*self._page_heading_product_locator).text

    @property
    def page_heading_version(self):
        return self.selenium.find_element(*self._page_heading_version_locator).text

    @property
    def results_count(self):
        return len(self.selenium.find_elements(*self._signature_table_row_locator))

    @property
    def results_found(self):
        try:
            return self.results_count > 0
        except NoSuchElementException:
            return False

    def click_filter_by(self, option):
        for element in self.selenium.find_elements(*self._filter_by_locator):
            if element.text == option:
                element.click()
                return CrashStatsTopCrashers(self.testsetup)

    def click_filter_days_by(self, days):
        '''
            Click on the link with the amount of days you want to filter by
        '''
        for element in self.selenium.find_elements(*self._filter_days_by_locator):
            if element.text == days:
                element.click()
                return CrashStatsTopCrashers(self.testsetup)

    @property
    def current_days_filter(self):
        return self.selenium.find_element(*self._current_days_filter_locator).text

    @property
    def current_filter_type(self):
        return self.selenium.find_element(*self._current_filter_type_locator).text

    @property
    def signature_items(self):
        return [self.SignatureItem(self.testsetup, i) for i in self.selenium.find_elements(*self._signature_table_row_locator)]

    @property
    def valid_signature_items(self):
        return [self.SignatureItem(self.testsetup, i) for i in self.selenium.find_elements(*self._signature_table_row_locator) if i.text != 'empty signature']

    def click_first_valid_signature(self):
        return self.valid_signature_items[0].click()

    @property
    def first_valid_signature_text(self):
        return self.valid_signature_items[0].text

    class SignatureItem(Page):
        _signature_link_locator = (By.CSS_SELECTOR, 'a.signature')
        _browser_icon_locator = (By.CSS_SELECTOR, 'div img.browser')
        _plugin_icon_locator = (By.CSS_SELECTOR, 'div img.plugin')

        def __init__(self, testsetup, element):
                Page.__init__(self, testsetup)
                self._root_element = element

        def click(self):
            self._root_element.find_element(*self._signature_link_locator).click()
            return CrashReport(self.testsetup)

        @property
        def text(self):
            return self._root_element.find_element(*self._signature_link_locator).text

        @property
        def is_plugin_icon_visible(self):
            return self.is_element_visible(self._root_element, *self._plugin_icon_locator)

        @property
        def is_browser_icon_visible(self):
            return self.is_element_visible(self._root_element, *self._browser_icon_locator)


class CrashStatsTopCrashersBySite(CrashStatsBasePage):

    _product_header_locator = (By.ID, 'tcburl-product')
    _product_version_header_locator = (By.ID, 'tcburl-version')

    @property
    def product_header(self):
        return self.selenium.find_element(*self._product_header_locator).text

    @property
    def product_version_header(self):
        return self.selenium.find_element(self._product_version_header_locator).text


class CrashStatsNightlyBuilds(CrashStatsBasePage):

    _link_to_ftp_locator = (By.CSS_SELECTOR, '.notitle > p > a')

    @property
    def link_to_ftp(self):
        return self.selenium.find_element(*self._link_to_ftp_locator).get_attribute('href')

    def click_link_to_ftp(self):
        self.selenium.find_element(*self._link_to_ftp_locator).click()


class CrashStatsStatus(CrashStatsBasePage):

    _at_a_glance_locator = (By.CSS_SELECTOR, 'div.panel > div > table.server_status')
    _graphs_locator = (By.CSS_SELECTOR, 'div.panel > div > div.server-status-graph')
    _latest_raw_stats_locator = (By.CSS_SELECTOR, 'div.panel > div > table#server-stats-table')

    @property
    def is_at_a_glance_present(self):
        return self.is_element_present(*self._at_a_glance_locator)

    @property
    def are_graphs_present(self):
        return len(self.selenium.find_elements(*self._graphs_locator)) == 4

    @property
    def is_latest_raw_stats_present(self):
        return self.is_element_present(*self._latest_raw_stats_locator)


class ProductsLinksPage(CrashStatsBasePage):

    _heading_locator = (By.CSS_SELECTOR, '.title h2')

    def __init__(self, testsetup):
        CrashStatsBasePage.__init__(self, testsetup)
        self.selenium.get(self.base_url + '/products/')

    @property
    def page_heading(self):
        return self.selenium.find_element(*self._heading_locator).text

    def click_product(self, product):
        self.selenium.find_element(By.LINK_TEXT, product).click()
        return CrashStatsHomePage(self.testsetup, product)

class CrashStatsTopChangers(CrashStatsBasePage):

    pass
