from selenium import webdriver
import selenium
from selenium.webdriver.common.by import By
import time
import os

URL="http://web.whatsapp.com"
SELECTORS = {
    'firstrun':"#wrapper",
    'qrCode':"#window > div.entry-main > div.qrcode > img",
    'mainPage':".app.two",
    'chatList':".infinite-list-viewport",
    'messageList':"#main > div > div:nth-child(1) > div > div.message-list",
    'unreadMessageBar':"#main > div > div:nth-child(1) > div > div.message-list > div.msg-unread",
    'searchBar':"#side > div.search-container > div > label > input",
    'searchCancel':".icon-search-morph",
    'chats':".infinite-list-item",
    'chatBar':'div.input',
    'sendButton':'button.icon:nth-child(3)',
}

driver = webdriver.Firefox()

def init():
    "Initialises the browser"
    driver.get(URL)
    driver.implicitly_wait(10)
    while True:
        try:
            time.sleep(1)
            element = driver.find_element_by_css_selector(SELECTORS['mainPage'])
        except:
            firstrun()
            continue
        break
    run()

def firstrun():
    print "first run"
    screen = driver.save_screenshot('temp.png')
    ok = input("waiting")

def press_send():
    "Presses the send button"
    driver.find_element_by_css_selector(SELECTORS['sendButton']).click()

def enter_message(message):
    "Enters the message onto the chat bar"
    driver.find_element_by_css_selector(SELECTORS['chatBar']).send_keys(message)

def select_contact(contact, entry = None):
    """
    Searches for the contact, as either name or number. If multiple exists, returns the
    'entry'th contact. If entry is not sent, return all the rows.
    """

    # Focusing before sending keys solves many problems
    driver.find_element_by_css_selector(SELECTORS['searchBar']).click()

    element = driver.find_element_by_css_selector(SELECTORS['searchBar']).send_keys(contact)
    time.sleep(1)

    try:
        result = get_user_list()
    except NoSuchElementException:
        return False

    # To get the most recent chat first, we reverse it
    contacts = result.find_elements_by_css_selector(SELECTORS['chats'])[::-1]
    time.sleep(1)

    if len(contacts) == 1:
        result.find_elements_by_css_selector(SELECTORS['chats'])[0].click()
    elif entry is None:
        driver.find_element_by_css_selector(SELECTORS['searchCancel']).click()
        return contacts
    else:
        contacts[entry].click()
    return True

def get_user_list():
    element = driver.find_element_by_css_selector(SELECTORS['chatList'])
    return element

def run():
    pass

init()
if __name__ == "__main__":
    time.sleep(1)
    get_user_list()
    time.sleep(1)
    select_contact("9704170702")
