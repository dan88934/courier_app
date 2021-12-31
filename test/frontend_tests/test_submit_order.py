from selenium import webdriver
from datetime import datetime, date
import unittest


class SubmitOrder(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('./test/frontend_tests/chromedriver')
        self.driver.get('http://127.0.0.1:5000/orders')

        self.sender_name = self.driver.find_element_by_id("sender_name")
        self.sender_name.click()
        self.sender_name.send_keys('Dan Hughes')

        self.sender_address = self.driver.find_element_by_id("sender_address")
        self.sender_address.click()
        self.sender_address.send_keys('22 Example Road, Marple Bridge')

        self.sender_city = self.driver.find_element_by_id("sender_city")
        self.sender_city.click()
        self.sender_city.send_keys('Stockport')

        self.sender_country = self.driver.find_element_by_id("sender_country")
        self.sender_country.click()
        self.sender_country.send_keys('United Kingdom')

        self.recipient_name = self.driver.find_element_by_id("recipient_name")
        self.recipient_name.click()
        self.recipient_name.send_keys('John Anderson')

        self.recipient_address = self.driver.find_element_by_id("recipient_address")
        self.recipient_address.click()
        self.recipient_address.send_keys('112, Example Road')

        self.recipient_city = self.driver.find_element_by_id("recipient_city")
        self.recipient_city.click()
        self.recipient_city.send_keys('Hull')

        self.recipient_country = self.driver.find_element_by_id("recipient_country")
        self.recipient_country.click()
        self.recipient_country.send_keys('United Kingdom')

        self.contents_declaration = self.driver.find_element_by_id("contents_declaration")
        self.contents_declaration.click()
        self.contents_declaration.send_keys('Cookies')

        self.insurance = self.driver.find_element_by_id("insurance")
        self.insurance.click()

        #Get current date
        self.current_date = date.today().strftime('%d/%m/%Y') # Date must be formatted with / between each number, rather than -

    def test_invalid_despatch_date(self):
        despatch_date = self.driver.find_element_by_id("despatch_date")
        despatch_date.click()
        despatch_date.send_keys('22/12/2021') # Invalid date

        package_value = self.driver.find_element_by_id("package_value")
        package_value.click()
        package_value.send_keys('183.52') # Valid value

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        message = self.driver.find_element_by_xpath('//*[@id="fail"]/pre').text
        self.assertEqual(' Despatch date must be today or tomorrow.', message)

    def test_value_not_a_number(self):
        despatch_date = self.driver.find_element_by_id("despatch_date")
        despatch_date.click()
        despatch_date.send_keys(self.current_date) # Valid date

        package_value = self.driver.find_element_by_id("package_value")
        package_value.click()
        package_value.send_keys('asfsdf') # Not a number

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        message = self.driver.find_element_by_xpath('//*[@id="fail"]/pre').text 
        self.assertEqual(' Package value must be a number.', message)

    def test_value_a_negative_number(self):
        despatch_date = self.driver.find_element_by_id("despatch_date")
        despatch_date.click()
        despatch_date.send_keys(self.current_date)

        package_value = self.driver.find_element_by_id("package_value")
        package_value.click()
        package_value.send_keys('-5')

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        message = self.driver.find_element_by_xpath('//*[@id="fail"]/pre').text 
        self.assertEqual(' Package value must be a positive number.', message)

    def test_valid_despatch_date_and_number(self):
        despatch_date = self.driver.find_element_by_id("despatch_date")
        despatch_date.click()
        despatch_date.send_keys(self.current_date)

        package_value = self.driver.find_element_by_id("package_value")
        package_value.click()
        package_value.send_keys('183.52')

        submit_button = self.driver.find_element_by_id("submit")
        submit_button.click()

        message = self.driver.find_element_by_xpath('//*[@id="success"]/h2').text 
        self.assertEqual('Success - Your delivery reference number is:', message)

if __name__ == '__main__':
    unittest.main()