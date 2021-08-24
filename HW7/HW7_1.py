import selenium.common.exceptions
from selenium import webdriver
import time
from pymongo import MongoClient
driver = webdriver.Chrome('chromedriver.exe')

client = MongoClient('localhost', 27017)
db = client['mail']
series_collection = db.mail
login = 'geekbrains11'  # Указать логин от Yandex почты
pwd = '123321qweewQ'  # Указать пароль от Yandex почты


def auth():
    url = 'https://passport.yandex.ru/'
    driver.get(url)

    username = driver.find_element_by_xpath('//*[@id="passp-field-login"]')
    username.send_keys(login)
    button = driver.find_element_by_xpath('//*[@id="passp:sign-in"]')
    button.click()

    time.sleep(2)
    password = driver.find_element_by_xpath('//*[@id="passp-field-passwd"]')
    password.send_keys(pwd)
    button2 = driver.find_element_by_xpath('//*[@id="passp:sign-in"]')
    button2.click()
    time.sleep(2)
    try:
        button3 = driver.find_element_by_xpath('//*[@id="root"]/div/div[2]/div[2]/div/div/div[2]/div[3]/div/div/form/div[3]/button')
        button3.click()
    except selenium.common.exceptions.NoSuchElementException:
        pass


def parse():
    mail_url = 'https://mail.yandex.ru'
    driver.get(mail_url)
    time.sleep(1)
    links = [i.get_attribute('href') for i in driver.find_elements_by_css_selector('div.mail-Layout-Inner  div.mail-MessageSnippet-Wrapper  a.mail-MessageSnippet')]

    mails = {}
    for i in links:
        driver.get(i)
        time.sleep(1)
        mails['from_name'] = driver.find_element_by_class_name('ns-view-message-head-sender-name').text
        mails['from_email'] = driver.find_element_by_class_name('mail-Message-Sender-Email').text
        mails['date'] = driver.find_element_by_class_name('ns-view-message-head-date').text
        mails['subject'] = driver.find_element_by_class_name('mail-Message-Toolbar-Subject').text
        mails['text_messege'] = driver.find_element_by_class_name('mail-Message-Body-Content').text
        series_collection.insert_one(mails)
        mails = {}


auth()
parse()
driver.quit()
