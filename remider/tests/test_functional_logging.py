from .base import FunctionalTest, check_internet_connection
from django.shortcuts import reverse
from django.test import override_settings
from selenium.webdriver.common.keys import Keys

from unittest import skipIf


class LoggingTest(FunctionalTest):

    @override_settings(DEBUG=True, SECRET_KEY="mycoolsecretkey")
    def test_templates(self):
        response = self.client.get(reverse("menu") + "?key=mycoolsecretkey")
        self.assertTemplateUsed(response, "remider/menu.html")
        self.assertEqual(response.status_code, 200)

    @skipIf(not check_internet_connection(), "internet disconnect")
    @override_settings(SECRET_KEY="mycoolsecretkey", LANGUAGE_CODE='en', app_name="benc-test", DEBUG=True)
    def test_google_redirect(self):
        self.browser.get(self.live_server_url)
        self.wait_for_finding(lambda: self.browser.find_element_by_id("OK-btn")).click()
        self.wait_and_assertUrlNow("https://www.google.com/")

    @override_settings(SECRET_KEY="mycoolsecretkey", LANGUAGE_CODE='en', app_name="benc-test", DEBUG=True)
    def test_logging(self):
        self.browser.get(self.live_server_url)
        self.wait_for_finding(lambda: self.browser.find_element_by_id("continue_buton")).click()
        self.assertUrlNow(url="get_secret")
        input = self.wait_for_finding(lambda: self.browser.find_element_by_id("id_apisecret"))

        input.send_keys("mycoolsecretkey")
        input.send_keys(Keys.ENTER)
        self.wait_and_assertUrlNow(url="menu")

        self.browser.get(self.live_server_url + reverse("get_secret"))
        input = self.wait_for_finding(lambda: self.browser.find_element_by_id("id_apisecret"))

        input.send_keys("mynotcoolsecretkey")
        input.send_keys(Keys.ENTER)
        self.wait_and_assertUrlNow(url="menu", status=403)