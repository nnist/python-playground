import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get('https://translate.google.com/')
#assert 'Google' in browser.title

# Enter text into source field
form = browser.find_element_by_id("source")
form.send_keys("""Ik ben een vriendelijke robot die dingen doet met Google translate.""" + Keys.RETURN)
time.sleep(1)

# Copy translated text
result_text = browser.find_element_by_id("result_box")
result_text.send_keys(Keys.CONTROL, 'c')
time.sleep(0.5)

# Paste translated text into source field
form.send_keys(Keys.CONTROL, 'v')
time.sleep(1)

# Click dropdown menu
dropdown = browser.find_element_by_id("gt-tl-gms")
dropdown.click()

# 8 groups
# Click random language
random_number = random.randrange(5)
group = browser.find_element_by_id("goog-menuitem-group-{}".format(random_number))
print(random_number)
languages = group.find_elements_by_class_name("goog-menuitem")
#len(languages) > 8

#print(languages)
#time.sleep(1)

#browser.quit()
