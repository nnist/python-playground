import random
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import argparse
import sys

def main(argv):
    parser = argparse.ArgumentParser(
        description="""Translates text over and over using Google translate"""
    )
    parser.add_argument(
    "-t", "--text",
    help="Text to translate",
    default="Did you see that ludicrous display last night?"
    )
    parser.add_argument(
    "-i", "--iterations",
    help="Number of iterations",
    default=5, type=int
    )

    args = parser.parse_args()

    browser = webdriver.Firefox()

    browser.get('https://translate.google.com/')
    #assert 'Google' in browser.title
    
    # Enter text into source field
    form = browser.find_element_by_id("source")
    form.send_keys(args.text + Keys.RETURN)
    time.sleep(1)
    
    # Click listen button
    listen_button = browser.find_element_by_id("gt-res-listen")
    listen_button.click()
    time.sleep(4)
    
    for i in range(args.iterations):
        # Copy translated text
        result_text = browser.find_element_by_id("result_box")
        time.sleep(0.5)
        print("Translated text: {}".format(result_text.text))
        
        # Paste translated text into source field
        form.clear()
        form.send_keys(result_text.text)
        time.sleep(1)
        
        # Click dropdown menu
        dropdown = browser.find_element_by_id("gt-tl-gms")
        dropdown.click()
        
        # Click random language
        group = browser.find_element_by_id("goog-menuitem-group-{}".format(1 + random.randrange(6)))
        languages = group.find_elements_by_class_name("goog-menuitem")
        language = languages[random.randrange(len(languages))]
        print("Selected {}".format(language.text))
        language.click()
        time.sleep(1)
    
    # Click dropdown, select English
    dropdown = browser.find_element_by_id("gt-tl-gms")
    dropdown.click()
    time.sleep(1)
    language_english = browser.find_element_by_id(":3j")
    language_english.click()
    time.sleep(2)
    
    # Click listen button
    listen_button = browser.find_element_by_id("gt-res-listen")
    listen_button.click()
    time.sleep(7)
    
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
