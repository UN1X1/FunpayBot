import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent

token = 'd1e6d8ecb0acfca8bbc0265706d0e3d4'
url = 'https://funpay.com/account/login'
funpay_login = 'qwerty8541'
funpay_password = 'Gde-DilleR-854'


useragent = UserAgent()
options = Options()
options.add_experimental_option('detach', True)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'user-agent={useragent.random}')

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def observer(login_funpay, password_funpay, token):
    # Заходим на Фанпей и решаем капчу
    sitekeyx = '//*[@id="content"]/div/div/div/form/div[4]/div'
    browser.get(url)
    time.sleep(2)
    login = browser.find_element(By.NAME, 'login')
    password = browser.find_element(By.NAME, 'password')
    login.send_keys(login_funpay)
    password.send_keys(password_funpay)
    # 6LdTYk0UAAAAAGgiIwCu8pB3LveQ1TcLUPXBpjDh
    sitekey = WebDriverWait(browser, 5).until(
        expected_conditions.presence_of_element_located((By.XPATH, sitekeyx))).get_attribute(
        'outerHTML')

    clean_sitekey = sitekey.split('"')[3]

    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(token)
    solver.set_website_url(url)
    solver.set_website_key(clean_sitekey)

    gresponse = solver.solve_and_return_solution()

    if gresponse:
        print(gresponse)
    else:
        print('error', solver.error_code)

    browser.execute_script(
        'var element=document.getElementById("g-recaptcha-response"); element.style.display="";')
    time.sleep(0.5)
    browser.execute_script(
        """document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", gresponse)
    time.sleep(0.5)
    browser.execute_script(
        'var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')
    time.sleep(1)
    submit = browser.find_element(By.XPATH, '//button[@class="btn btn-primary btn-block"]')
    time.sleep(1)
    submit.click()
    time.sleep(1)
    # Заходим в продажи
    orders_button = browser.find_element(By.CLASS_NAME, 'menu-item-trade')
    orders_button.click()
    previous_order = '777'

    logins = []
    # Бесконечный цикл который чекает новые заказы
    while True:
        flag = False
        browser.refresh()
        time.sleep(1)
        try:
            order = browser.find_element(By.XPATH, "//a[@class='tc-item info']")
            flag = True
        except Exception:
            print('Ни один не подтвержденный заказ не найден')
        # Если заказ подходит по критериям
        if flag and previous_order not in order.get_attribute('innerHTML') and ('аренда' in order.get_attribute('innerHTML') or 'Аренда' in order.get_attribute('innerHTML')):
            previous_order = order.find_element(By.CLASS_NAME, 'tc-order').get_attribute('innerHTML')
            order.click()
            msgs = browser.find_elements(By.XPATH, '//div[@class="chat-msg-item chat-msg-with-head"]')[::-1]
            # Пролистываем сообщения
            for i, msg in enumerate(msgs[:15]):
                try:
                    msg_text = msg.find_element(By.CLASS_NAME, 'chat-msg-text').text
                    match = re.findall(r'\s*[Лл]огин\s*:* ([\w\d]+) [Пп]ароль\s*:* [\w\d]+\s*', msg_text)
                    if match:
                        print(match[0])
                        break
                    else:
                        print('нема')
                except Exception:
                    print('Не то сообщение')
            # Возвращаемся на страницу с продажами
            orders_button = browser.find_element(By.CLASS_NAME, 'menu-item-trade')
            orders_button.click()
            print(previous_order)
            print(msgs)


observer(funpay_login, funpay_password, token)