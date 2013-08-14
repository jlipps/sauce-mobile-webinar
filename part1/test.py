import os
import unittest
from selenium import webdriver
from random import randint


class AppiumTestCase(unittest.TestCase):

    def setUp(self):
        user = os.environ.get('SAUCE_USERNAME')
        pw = os.environ.get('SAUCE_ACCESS_KEY')
        appium = "http://%s:%s@ondemand.saucelabs.com:%s/wd/hub" % (user, pw, 80)
        self.desired_caps.update({
            'device': 'iPhone Simulator',
            'platform': 'Mac 10.8',
            'version': '6.1',
        })
        self.driver = webdriver.Remote(appium, self.desired_caps)
        self.driver.implicitly_wait(30)

    def tearDown(self):
        self.driver.quit()


class CalculatorAppTestCase(AppiumTestCase):

    values = []

    def setUp(self):
        app = "http://appium.s3.amazonaws.com/TestApp6.1.app.zip"
        self.desired_caps = {
            'app': app,
            'name': 'Calculator App Test'
        }
        AppiumTestCase.setUp(self)

    def test_calculator_addition(self):
        # populate text fields with two random number
        elems = self.driver.find_elements_by_tag_name('textField')
        for elem in elems:
            rand_num = randint(0, 10)
            elem.send_keys(rand_num)
            self.values.append(rand_num)

        # trigger computation by using the button
        button = self.driver.find_element_by_name("ComputeSumButton")
        button.click()

        # test validity of result
        result = self.driver.find_element_by_xpath("//text[1]")
        self.assertEqual(int(result.text), sum(self.values))
