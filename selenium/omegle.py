#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import argparse
import sys
import time
import os

def send_message(browser, keys):
    element = browser.find_element_by_css_selector(".chatmsg")
    for key in keys:
        element.send_keys(key)
        #time.sleep(0.02)
    element.send_keys(Keys.RETURN)

def get_messages(browser):
    messages = []
    log_items = browser.find_elements_by_css_selector(".logitem")
    for item in log_items:
        try:
            messages.append(item.text)
        except:
            pass
    return messages

def connect(browser):
    disconnect_button = browser.find_element_by_css_selector(".disconnectbtn")
    disconnect_button.click()

def disconnect(browser):
    disconnect_button = browser.find_element_by_css_selector(".disconnectbtn")
    disconnect_button.click()
    time.sleep(0.1)
    disconnect_button.click()

def main(argv):
    print("Starting browsers...")
    browser1 = webdriver.Firefox()
    browser1.get('http://omegle.com/')
    browser2 = webdriver.Firefox()
    browser2.get('http://omegle.com/')
    assert "Omegle" in browser1.title
    assert "Omegle" in browser2.title
    print("Browsers started.")

    # Click text chat button
    text_button = browser1.find_element_by_id("textbtn")
    text_button.click()
    text_button = browser2.find_element_by_id("textbtn")
    text_button.click()
    print("Started chat sessions.")

    messages1 = []
    messages2 = []

    # TODO filter out bots
    # TODO reconnect on timeout
    while True:
        msg1 = get_messages(browser1)
        for msg in msg1:
            if msg not in messages1:
                if msg.startswith("Stranger:"):
                    messages1.append(msg)
                    print("\033[31mStranger 1\033[0m: {}".format(msg[10:]))
                    send_message(browser2, msg[10:])
                elif msg == "Stranger has disconnected." or msg == "You have disconnected.":
                    print("\033[2mStranger 1 has disconnected, finding a new partner...\033[0m")
                    connect(browser1)
                elif msg.startswith("You're now chatting with a random stranger. Say hi!"):
                    print("\033[2mStranger 1 connected..\033[0m")
                    messages1.append(msg)
        
        msg2 = get_messages(browser2)
        for msg in msg2:
            if msg not in messages2:
                if msg.startswith("Stranger:"):
                    messages2.append(msg)
                    print("\033[32mStranger 2\033[0m: {}".format(msg[10:]))
                    send_message(browser1, msg[10:])
                elif msg == "Stranger has disconnected." or msg == "You have disconnected.":
                    print("\033[2mStranger 2 has disconnected, finding a new partner...\033[0m")
                    connect(browser2)
                elif msg.startswith("You're now chatting with a random stranger. Say hi!"):
                    print("\033[2mStranger 1 connected..\033[0m")
                    messages2.append(msg)

        time.sleep(0.5)

    disconnect(browser1)
    disconnect(browser2)

    #time.sleep(5)

    #messages = get_messages(browser)
    #print(messages)

    #disconnect(browser)
    
    #time.sleep(1)
    #browser.quit()

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print('Interrupted by user.')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

