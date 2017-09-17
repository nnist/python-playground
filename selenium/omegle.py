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
    
bot_messages = ["hi! i'm jennifer", "hiiiiiiiii girl", "hello, im lucy",
    "waanna shareg phoatos ?", "wnant 2 shpare pix ?", "hi hun, ",
    "are you sick of", "19f and u?", "21 female", "waanna pswap pix ?",
    "youre the person i was just chatting to ????",
    "brunette girl here wanna chat?", "hit me up on", "woman 22", ".pro/"]

def check_bot_message(message):
    # Check if message is something a bot would say
    message = message.lower()
    
    for bot_message in bot_messages:
        if message.startswith(bot_message) or bot_message in message:
            return True
        else:
            return False

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

    timeout = 60
    stranger_1_msg_time = None
    stranger_2_msg_time = None

    # TODO filter out bots
    while True:
        msg1 = get_messages(browser1)
        for msg in msg1:
            if msg not in messages1:
                # Check if captcha has appeared
                try:
                    recaptcha_area = browser1.find_element_by_css_selector(".logitem > iframe:nth-child(1)")
                except:
                    pass
                else:
                    print("\033[33mError\033[0m: Session 1 requires captcha to be solved.")
                    messages1.append(msg)
               
                if check_bot_message(msg[10:]):
                    print("\033[2mBot detected. Disconnected, finding a new partner...\033[0m")
                    messages1 = []
                    disconnect(browser1)
                    connect(browser1)
                    stranger_1_msg_time = None
                elif msg.startswith("Stranger:"):
                    messages1.append(msg)
                    print("\033[31mStranger 1\033[0m: {}".format(msg[10:]))
                    send_message(browser2, msg[10:])
                    stranger_1_msg_time = time.time()
                elif msg == "Stranger has disconnected." or msg == "You have disconnected.":
                    print("\033[2mStranger 1 has disconnected, finding a new partner...\033[0m")
                    messages1 = []
                    connect(browser1)
                    stranger_1_msg_time = None
                elif msg.startswith("You're now chatting with a random stranger. Say hi!"):
                    print("\033[2mStranger 1 connected.\033[0m")
                    messages1.append(msg)
                    stranger_1_msg_time = time.time()
        
        msg2 = get_messages(browser2)
        for msg in msg2:
            if msg not in messages2:
                # Check if captcha has appeared
                try:
                    recaptcha_area = browser2.find_element_by_css_selector(".logitem > iframe:nth-child(1)")
                except:
                    pass
                else:
                    print("\033[33mError\033[0m: Session 2 requires captcha to be solved.")
                    messages2.append(msg)
                
                if check_bot_message(msg[10:]):
                    print("\033[2mBot detected. Disconnected, finding a new partner...\033[0m")
                    messages2 = []
                    disconnect(browser2)
                    connect(browser2)
                    stranger_2_msg_time = None
                elif msg.startswith("Stranger:"):
                    messages2.append(msg)
                    print("\033[32mStranger 2\033[0m: {}".format(msg[10:]))
                    send_message(browser1, msg[10:])
                    stranger_2_msg_time = time.time()
                elif msg == "Stranger has disconnected." or msg == "You have disconnected.":
                    print("\033[2mStranger 2 has disconnected, finding a new partner...\033[0m")
                    messages2 = []
                    connect(browser2)
                    stranger_2_msg_time = None
                elif msg.startswith("You're now chatting with a random stranger. Say hi!"):
                    print("\033[2mStranger 2 connected.\033[0m")
                    messages2.append(msg)
                    stranger_2_msg_time = None

        time.sleep(0.5)

        # Check for timeouts
        if stranger_1_msg_time is not None and time.time() - stranger_1_msg_time > timeout:
            print("Session 1 timed out, connecting to someone else.")
            disconnect(browser1)
            connect(browser1)
            stranger_1_msg_time = None
        if stranger_2_msg_time is not None and time.time() - stranger_2_msg_time > timeout:
            print("Session 2 timed out, connecting to someone else..")
            disconnect(browser2)
            connect(browser2)
            stranger_2_msg_time = None

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

