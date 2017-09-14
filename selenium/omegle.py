#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import argparse
import sys
import time
import os

def send_message(element, keys):
    for key in keys:
        element.send_keys(key)
        time.sleep(0.05)
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

    time.sleep(.5)

    field = browser.find_element_by_css_selector(".chatmsg")
   
    send_message(field, "hi")

    #print("You're now chatting with a random stranger. Say hi!")
    #text = input("You: ")
    
    # TODO allow input

    log_box = browser.find_element_by_css_selector(".logbox")
   
    log = []

    while True:
        # Retrieve log items
        log_items = browser.find_elements_by_css_selector(".logitem")
        for item in log_items:
            # Add item to log if it doesn't exist yet
            if item not in log:
                log.append(item)
                print(item.text)
                if not item.text.startswith("You"):
                    send_message(field, item.text)
        time.sleep(0.5)
    
    #send_message(field, "i like kittens")
    #time.sleep(0.1)
    #send_message(field, "goodbye.")

    # Disconnect
    disconnect_button = browser.find_element_by_css_selector(".disconnectbtn")
    disconnect_button.click()
    time.sleep(0.1)
    disconnect_button.click()
    
    time.sleep(1)
    browser.quit()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

