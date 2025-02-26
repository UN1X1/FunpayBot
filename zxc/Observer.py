import re
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import string

token = 'd1e6d8ecb0acfca8bbc0265706d0e3d4'
url = 'https://funpay.com/account/login'
funpay_login = 'qwerty8541'
funpay_password = 'Gde-DilleR-854'

symbols = string.ascii_letters + string.digits + string.digits + string.digits

def password_generator(old_password):
    return ''.join([random.choice(symbols) for i in range(4)]) + 'Unix' + ''.join([random.choice(symbols) for i in range(4)])


# Параметры для браузера
useragent = UserAgent()
options = Options()

options.add_experimental_option('detach', True)
#options.add_argument({'proxy':{'http': 'http://a616c4b4b7:e01b7c64a4@192.162.59.28:36202', 'https': 'http://a616c4b4b7:e01b7c64a4@192.162.59.28:36202', 'no_proxy': 'localhost,151.252.94.161'}})
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'user-agent={useragent.random}')
# Создаем объект браузера
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Функция наблюдателя
def observer(login_funpay, password_funpay, token):
    sitekeyx = '//*[@id="content"]/div/div/div/form/div[4]/div'
    browser.get(url)
    time.sleep(2)
    # Вводим логин пароль
    login = browser.find_element(By.NAME, 'login')
    password = browser.find_element(By.NAME, 'password')
    login.send_keys(login_funpay)
    password.send_keys(password_funpay)
    # 6LdTYk0UAAAAAGgiIwCu8pB3LveQ1TcLUPXBpjDh
    sitekey = WebDriverWait(browser, 5).until(
        expected_conditions.presence_of_element_located((By.XPATH, sitekeyx))).get_attribute(
        'outerHTML')
    # Задаем параметры для решения капчи
    clean_sitekey = sitekey.split('"')[3]
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(token)
    solver.set_website_url(url)
    solver.set_website_key(clean_sitekey)
    # Получаем решенную капчу
    for i in range(10):
        try:
            gresponse = solver.solve_and_return_solution()

            if gresponse:
                print(gresponse)
            else:
                print('error', solver.error_code)
            # Вставляем в соответсвующее поле решение капчи
            browser.execute_script(
                'var element=document.getElementById("g-recaptcha-response"); element.style.display="";')
            time.sleep(1)
            browser.execute_script(
                """document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", gresponse)
            time.sleep(1)
            browser.execute_script(
                'var element=document.getElementById("g-recaptcha-response"); element.style.display="none";')
            time.sleep(2)

            submit = browser.find_element(By.XPATH, '//button[@class="btn btn-primary btn-block"]')
            time.sleep(2)
            submit.click()
            time.sleep(1)
            # Заходим в продажи
            orders_button = browser.find_element(By.CLASS_NAME, 'menu-item-trade')
            orders_button.click()
        except Exception as e:
            print('Ошибка при прохождении капчи', e)
            continue
        break
    previous_order = '777'

    # Бесконечный цикл который чекает новые заказы
    while True:
        flag = False
        # Чекаем наличие новых сообщений
        browser.refresh()
        time.sleep(1)
        try:
            # Пытаемся найти новый заказ
            order = browser.find_element(By.XPATH, "//a[@class='tc-item info']")
            flag = True
            order_html = order.get_attribute('innerHTML')
        except Exception:
            print('Ни один не подтвержденный заказ не найден')
        # Если заказ подходит по критериям
        if flag and previous_order not in order_html and ('аренда' in order_html or 'Аренда' in order_html):
            previous_order = order.find_element(By.CLASS_NAME, 'tc-order').get_attribute('innerHTML')
            order.click()
            msgs = browser.find_elements(By.XPATH, '//div[@class="chat-msg-item chat-msg-with-head"]')[::-1]
            # Пролистываем сообщения с покупателем
            for i, msg in enumerate(msgs[:15]):
                try:
                    # Ищем сообщение автовыдачи
                    msg_text = msg.find_element(By.CLASS_NAME, 'chat-msg-text').text
                    match = re.findall(r'Логин: ([\w\d]+) Пароль: [\w\d]+', msg_text)
                    # Если находим
                    if match:
                        print(match[0], 'логин')
                        with open('AvailableScripts.txt', 'r') as file:
                            first_avaible_script = file.readline()
                            rest_scripts = file.readlines()
                        with open('AvailableScripts.txt', 'w') as file:
                            file.writelines(rest_scripts)

                        with open(f'{match[0]}.txt', 'r') as file:
                            lines = file.read()
                            lines = lines.replace('\n', ' ')
                        # Отправляем запрос на смену пароля первому доступному скрипту
                        with open('request.txt', 'w') as file:
                            file.write(f'{first_avaible_script} {lines}')

                        print(lines, 'данные')

                        info = info[1:]

                        scripts_emails = scripts_emails[1:]
                        print('break')
                        break
                    else:
                        print('нема')
                except Exception as e:
                    print('Не то сообщение', e)
            # Возвращаемся на страницу с продажами
            orders_button = browser.find_element(By.CLASS_NAME, 'menu-item-trade')
            orders_button.click()
            print(previous_order)
            print(list(msgs))
            # Цикл повторяется

# r'\s*[Лл]огин\s*:* ([\w\d]+) [Пп]ароль\s*:* [\w\d]+\s*'
# Вызов функции наблюдателя
observer(funpay_login, funpay_password, token)
