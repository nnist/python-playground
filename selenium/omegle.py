from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import argparse
import sys
import time
import os

def send_message(element, keys):
    for key in keys:
        element.send_keys(key)
        time.sleep(0.1)
    element.send_keys(Keys.RETURN)

def close_all_popups(driver):
    driver.window_handles
    for h in driver.window_handles[1:]:
        driver.switch_to_window(h)
        driver.close()
    driver.switch_to_window(driver.window_handles[0])

def main(argv):
    browser = webdriver.Firefox()

    browser.get('http://omegle.com/')
   
    assert "Omegle" in browser.title

    text_button = browser.find_element_by_id("textbtn")
    text_button.click()

    time.sleep(2)

    field = browser.find_element_by_css_selector(".chatmsg")
   
    print("You're now chatting with a random stranger. Say hi!")
    text = input("")

    send_message(field, text)
    time.sleep(0.2)
    send_message(field, "i like kittens")
    time.sleep(0.1)
    send_message(field, "goodbye.")
   
    disconnect_button = browser.find_element_by_css_selector(".disconnectbtn")
    disconnect_button.click()
    time.sleep(0.1)
    disconnect_button.click()
    time.sleep(1)

    browser.quit()
    sys.exit(0)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

