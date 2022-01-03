from selenium import webdriver
# from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome('./chromedriver')
driver.get('http://206.189.101.191:5000/orders')

sender_name = driver.find_element_by_id("sender_name")
sender_name.click()
sender_name.send_keys('Dan Hughes')

sender_address = driver.find_element_by_id("sender_address")
sender_address.click()
sender_address.send_keys('22 Example Road, Marple Bridge')

sender_city = driver.find_element_by_id("sender_city")
sender_city.click()
sender_city.send_keys('Stockport')

sender_country = driver.find_element_by_id("sender_country")
sender_country.click()
sender_country.send_keys('United Kingdom')

recipient_name = driver.find_element_by_id("recipient_name")
recipient_name.click()
recipient_name.send_keys('John Anderson')

recipient_address = driver.find_element_by_id("recipient_address")
recipient_address.click()
recipient_address.send_keys('112 Example Road')

recipient_city = driver.find_element_by_id("recipient_city")
recipient_city.click()
recipient_city.send_keys('Hull')

recipient_country = driver.find_element_by_id("recipient_country")
recipient_country.click()
recipient_country.send_keys('United Kingdom')

package_value = driver.find_element_by_id("package_value")
package_value.click()
package_value.send_keys('183.52')

contents_declaration = driver.find_element_by_id("contents_declaration")
contents_declaration.click()
contents_declaration.send_keys('Cookies')

despatch_date = driver.find_element_by_id("despatch_date")
despatch_date.click()
despatch_date.send_keys('03/01/2022')

insurance = driver.find_element_by_id("insurance")
insurance.click()


submit_button = driver.find_element_by_id("submit")
submit_button.click()
