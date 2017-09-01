import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get('https://google.com')
#assert 'Google' in browser.title

form = browser.find_element_by_id("lst-ib")
form.send_keys("""translate""" + Keys.RETURN)
time.sleep(1)
form = browser.find_element_by_id("tw-source-text-ta")
form.send_keys("fuck you lol")

voice_button = browser.find_element_by_id("tw-src-spkr-button")
voice_button.send_keys(Keys.RETURN)
time.clockl
time.sleep(5)
time.sleep
browser.quit()
