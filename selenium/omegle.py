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
    try:
        disconnect_button.click()
        time.sleep(0.1)
        disconnect_button.click()
    except:
        pass

bot_messages = ["hi! i'm jennifer", "hiiiiiiiii girl", "hello, im lucy",
    "waanna shareg phoatos ?", "wnant 2 shpare pix ?", "hi hun, ",
    "are you sick of", "19f and u?", "21 female", "waanna pswap pix ?",
    "youre the person i was just chatting to ????", "19 female", "bit.ly"
    "ur the person i was just talking to ????", "girl 25"
    "brunette girl here wanna chat?", "hit me up on", "woman 22", ".pro/",
    "im brooke,", "chick here..", "20 female", "18 female", ".site/",
    "heya! i'm jennifer", "heya! my name is", "damn a-girl0)", "got a -(kik)-"
    "18 f wanna talk??", "check this site adult-omegle.com",
    "watch-me", "hey wassup yall", "u should kik me at",
    "why don't you open kik messenger", "Enter the web and",
    "I'm doing a sexcam show"]

def check_bot_message(message):
    # Check if message is something a bot would say
    message = message.lower()
    for bot_message in bot_messages:
        if message.startswith(bot_message) or bot_message in message:
            return True
    
    return False

def handle_log_items(browser, other_browser, session_num, prev_log_items):
    log_items = browser.find_elements_by_css_selector(".logitem")
    new_log_items = list(set(log_items) - set(prev_log_items))

    for item in new_log_items:
        try:
            text = item.text
        except:
            print("item.text no longer exists lol")
        else:
            if text == "You have disconnected.": # Manually disconnected
                print("\033[2mSession {} manually disconnected. Finding a new partner...\033[0m".format(session_num))
                prev_log_items = []
                time.sleep(1)
                connect(browser)
                break
            elif text == "Stranger has disconnected.": # Stranger disconnected
                print("\033[2mStranger {} has disconnected, finding a new partner...\033[0m".format(session_num))
                prev_log_items = []
                time.sleep(1)
                connect(browser)
                break
            elif text == "You're now chatting with a random stranger. Say hi!":
                print("\033[2mStranger {} connected.\033[0m".format(session_num))
                # TODO Update timeout
            elif text.startswith("Stranger:"): # Stranger said something
                message = text[10:]
                if check_bot_message(message):
                    print("\033[2mSession {}: Bot detected. ({}) Disconnected, finding a new partner...\033[0m".format(session_num, message))
                    prev_log_items = []
                    time.sleep(1)
                    disconnect(browser)
                    time.sleep(1)
                    connect(browser)
                    break
                else:
                    print("\033[31mStranger {}\033[0m: {}".format(session_num, message))
                    # TODO Update timeout
                    # TODO Filter out bad words
                    send_message(other_browser, message)

    return log_items

def main(argv):
    # TODO Sometimes stranger doesn't say anything at all; make that timeout too
    # TODO Option to greet on connect
    # TODO Fix 'Connection refused' error on Ctrl-C
    # TODO Print timeout message on timeout, instead of 'manually connected'
    # TODO Log messages
    # TODO Count similar messages for bot checking
    parser = argparse.ArgumentParser(description='Connect two people on Omegle to eachother.')
    parser.add_argument(
        '-v', '--verbose',
        help='Be verbose',
        action='store_true'
    )
    parser.add_argument(
        '-t', '--timeout',
        help='Timeout idle chats after t seconds',
        type=int, default=60
    )

    args = parser.parse_args()
    
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

    timeout = args.timeout
    stranger_1_msg_time = None
    stranger_2_msg_time = None

    while True:
        # TODO Check both browsers for captcha on page
        
        messages1 = handle_log_items(browser1, browser2, 1, messages1)

        messages2 = handle_log_items(browser2, browser1, 2, messages2)

        # TODO Handle timeout

#    while True:
#        # Check if captcha has appeared
#        try:
#            recaptcha_area = browser1.find_element_by_css_selector(".logitem > iframe:nth-child(1)")
#        except:
#            pass
#        else:
#            print("\033[33mError\033[0m: Session 1 requires captcha to be solved.")
#            messages1.append(msg)
#        
#        # Check if captcha has appeared
#        try:
#            recaptcha_area = browser2.find_element_by_css_selector(".logitem > iframe:nth-child(1)")
#        except:
#            pass
#        else:
#            print("\033[33mError\033[0m: Session 2 requires captcha to be solved.")
#            messages2.append(msg)
#
#        # Check for new messages in browser 1
#        msg1 = get_messages(browser1)
#        for msg in msg1:
#            if msg not in messages1:
#                # Handle message
#                if msg.startswith("Stranger:"):
#                    if check_bot_message(msg[10:]):
#                        print("\033[2mSession 1: Bot detected. ({}) Disconnected, finding a new partner...\033[0m".format(msg[10:]))
#                        messages1 = []
#                        disconnect(browser1)
#                        connect(browser1)
#                        stranger_1_msg_time = None
#                    else:
#                        messages1.append(msg)
#                        print("\033[31mStranger 1\033[0m: {}".format(msg[10:]))
#                        send_message(browser2, msg[10:])
#                        stranger_1_msg_time = time.time()
#                elif msg == "Stranger has disconnected.":
#                    print("\033[2mStranger 1 has disconnected, finding a new partner...\033[0m")
#                    messages1 = []
#                    connect(browser1)
#                    stranger_1_msg_time = None
#                elif msg == "You have disconnected.":
#                    print("\033[2mSession 1 manually disconnected. Finding a new partner...\033[0m")
#                    messages1 = []
#                    connect(browser1)
#                    stranger_1_msg_time = None
#                elif msg.startswith("You're now chatting with a random stranger. Say hi!"):
#                    print("\033[2mStranger 1 connected.\033[0m")
#                    messages1.append(msg)
#                    stranger_1_msg_time = time.time()
#        
#        # Check for new messages in browser 2
#        msg2 = get_messages(browser2)
#        for msg in msg2:
#            if msg not in messages2:
#                # Handle message
#                if msg.startswith("Stranger:"):
#                    if check_bot_message(msg[10:]):
#                        print("\033[2mSession 2: Bot detected. ({}) Disconnected, finding a new partner...\033[0m".format(msg[10:]))
#                        messages2 = []
#                        disconnect(browser2)
#                        connect(browser2)
#                        stranger_2_msg_time = None
#                    else:
#                        messages2.append(msg)
#                        print("\033[32mStranger 2\033[0m: {}".format(msg[10:]))
#                        send_message(browser1, msg[10:])
#                        stranger_2_msg_time = time.time()
#                elif msg == "Stranger has disconnected.":
#                    print("\033[2mStranger 2 has disconnected, finding a new partner...\033[0m")
#                    messages2 = []
#                    connect(browser2)
#                    stranger_2_msg_time = None
#                elif msg == "You have disconnected.":
#                    print("\033[2mSession 2 manually disconnected. Finding a new partner...\033[0m")
#                    messages2 = []
#                    connect(browser2)
#                    stranger_2_msg_time = None
#                elif msg.startswith("You're now chatting with a random stranger. Say hi!"):
#                    print("\033[2mStranger 2 connected.\033[0m")
#                    messages2.append(msg)
#                    stranger_2_msg_time = None
#
#        time.sleep(0.5)
#
#        # Check for timeouts
#        if stranger_1_msg_time is not None and time.time() - stranger_1_msg_time > timeout:
#            print("\033[2mSession 1 timed out, connecting to someone else.\033[0m")
#            messages1 = []
#            disconnect(browser1)
#            connect(browser1)
#            stranger_1_msg_time = None
#        if stranger_2_msg_time is not None and time.time() - stranger_2_msg_time > timeout:
#            print("\033[2mSession 2 timed out, connecting to someone else..\033[0m")
#            messages2 = []
#            disconnect(browser2)
#            connect(browser2)
#            stranger_2_msg_time = None

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

