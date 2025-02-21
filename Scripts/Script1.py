import re
import time
import imaplib
import email
from smtplib import SMTP_SSL, SMTP_SSL_PORT

from appium.options.common.prerun_option import PrerunOption
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from email.mime.text import MIMEText
import smtplib




useragent = UserAgent()
options = Options()
options.add_experimental_option('detach', True)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'user-agent={useragent.random}')

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def funpay_update(steam_login, steam_password, keywordtitle, keywordlot):
    sitekeyx = '//*[@id="content"]/div/div/div/form/div[4]/div'
    browser.get('https://funpay.com/account/login')
    time.sleep(2)
    login = browser.find_element(By.NAME, 'login')
    password = browser.find_element(By.NAME, 'password')
    login.send_keys('qwerty8541')
    password.send_keys('Gde-DilleR-854')
    # 6LdTYk0UAAAAAGgiIwCu8pB3LveQ1TcLUPXBpjDh
    sitekey = WebDriverWait(browser, 5).until(
        expected_conditions.presence_of_element_located((By.XPATH, sitekeyx))).get_attribute(
        'outerHTML')

    clean_sitekey = sitekey.split('"')[3]

    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key('d1e6d8ecb0acfca8bbc0265706d0e3d4')
    solver.set_website_url('https://funpay.com/account/login')
    solver.set_website_key(clean_sitekey)

    gresponse = solver.solve_and_return_solution()

    if gresponse:
        print(gresponse)
    else:
        print('error', solver.error_code)

    browser.execute_script(
        'var element=document.getElementById("g-recaptcha-response"); element.style.display="";')
    time.sleep(1)
    browser.execute_script(
        """document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", gresponse)
    time.sleep(1)
    browser.execute_script(
        'var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')
    time.sleep(3)
    submit = browser.find_element(By.XPATH, '//button[@class="btn btn-primary btn-block"]')
    submit.click()
    time.sleep(1)

    browser.get('https://funpay.com/users/11085243/')

    titles = browser.find_elements(By.CLASS_NAME, 'offer-list-title')
    pencils = browser.find_elements(By.XPATH, '//a[@class="btn btn-default btn-plus"]')

    for i, title in enumerate(titles):
        if keywordtitle in title.get_attribute('innerHTML'):
            pencils[i].click()
            break

    lots = browser.find_elements(By.CLASS_NAME, 'tc-item')
    isactive = browser.find_elements(By.XPATH, '//div[@class="tc-amount hidden-xxs"]')

    flag = False

    for isact, lot in zip(isactive, lots):
        if keywordlot in lot.get_attribute('innerHTML'):
            if '0' in isact.get_attribute('outerHTML'):
                flag = True
            lot.click()
            break

    time.sleep(1)

    textarea = browser.find_element(By.XPATH,'//textarea[@class="form-control textarea-lot-secrets"]')

    textarea.send_keys(f'\nЛогин: {steam_login} Пароль: {steam_password}')

    if flag:
        zxc = browser.find_elements(By.XPATH, '//i')[-3]
        zxc.click()

    last_submit = browser.find_element(By.XPATH,
                                       '//button[@class="btn btn-primary btn-block js-btn-save"]')
    last_submit.click()

funpay_update('qwe', 'zxc', 'asd', 'vbn')