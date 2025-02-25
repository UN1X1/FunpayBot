import re
import time
import smtplib
import imaplib
import email
import random
from selenium import webdriver
from email.mime.text import MIMEText
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
observer_mail = 'observer1.0@mail.ru'
observer_password = 'CKUPxQATVjsuUZe26hEw'

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
# Список доступных скриптов
scripts_emails = ['qwerty.zxc.1@mail.ru', 'qwerty.zxc.2@mail.ru', 'qwerty.zxc.3@mail.ru']
info = ['zxcvbn8541111 nr4s8cx1 nr4s8cx12 clairegeorge1904@agglutinmail.ru axbhuxee4411 Russia Blue 0.0001',
        'zxcvbn8541111 nr4s8cx12 nr4s8cx123 clairegeorge1904@agglutinmail.ru axbhuxee4411 ARK ark 0.0001',
        'zxcvbn8541111 nr4s8cx123 nr4s8cx1234 clairegeorge1904@agglutinmail.ru axbhuxee4411 Russia Red 0.01',
        'zxcvbn8541111 nr4s8cx1234 nr4s8cx12345 clairegeorge1904@agglutinmail.ru axbhuxee4411 Russia Blue 0.0001',
        'zxcvbn8541111 nr4s8cx12345 nr4s8cx123456 clairegeorge1904@agglutinmail.ru axbhuxee4411 ARK ark 0.0001',
        'zxcvbn8541111 nr4s8cx123456 nr4s8cx1234567 clairegeorge1904@agglutinmail.ru axbhuxee4411 Russia Red 0.01'
        ]


# Функция которая чекает почту
def check_email(email_address, password):
    # Обрабатываем биг ашипку
    try:
        # Устанавливаем соединение с имап сервером
        mail = imaplib.IMAP4_SSL('imap.mail.ru', port=993)
        mail.login(email_address, password)
        mail.select('inbox')
        # Список всех айдишников сообщений
        status, messages = mail.search(None, 'unseen')
        # Проверка на случай если ипанет ашипка
        if status == 'OK':
            message_ids = messages[0].split()
            # Проверка на случай если нет сообщений
            if message_ids:
                # Берем каждое сообщение отдельно
                for id in message_ids:
                    status, msg_data = mail.fetch(id, '(RFC822)')
                    if status == 'OK':
                        email_message = email.message_from_bytes(msg_data[0][1])

                        # Достаем текст сообщения
                        if email_message.is_multipart():
                            for part in email_message.walk():
                                content_type = part.get_content_type()
                                if content_type == 'text/plain':
                                    body = part.get_payload(decode=True).decode()

                        else:
                            body = email_message.get_payload(decode=True).decode()

                        # Выводим в консоль
                        print(f"Почта: {email_address}")
                        print(f'Текст: {body}')
                        return body

    # Апять обработка биг ашипки
    except Exception as e:
        print(f'Ошибка')
# Функция для отправки сообщений на почту
def send_email(sender, pasword, getter, msg_text):
    server = smtplib.SMTP('smtp.mail.ru', 587)
    server.starttls()
    msg = MIMEText(f'{msg_text}', 'plain', 'utf-8')
    msg['Subject'] = 'Данные об аккаунте стим'
    msg['To'] = getter
    server.login(sender, pasword)
    server.sendmail(sender, getter, msg.as_string())

# Функция наблюдателя
def observer(login_funpay, password_funpay, token):
    global scripts_emails
    global info
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
        message = check_email(observer_mail, observer_password)
        if message != None and message.split()[0] == 'UNIX8541':

            lst_message = message.split()

            with open('ValidScripts.txt', 'a') as file:
                file.write(f'\n{lst_message[1]}')

            with open(f'{lst_message[2]}.txt', 'r') as file:
                lines = file.read().split('\n')
            lines[1] = lst_message[3]
            lines[2] = password_generator(lines[2])

            with open(f'{match[0]}.txt', 'w') as file:
                print(*lines, sep='\n', file=file)
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
                        with open('ValidScripts.txt', 'r') as file:
                            first_avaible_script = file.readline()
                            rest_scripts = file.readlines()
                        with open('ValidScripts.txt', 'w') as file:
                            file.writelines(rest_scripts)

                        with open(f'{match[0]}.txt', 'r') as file:
                            lines = file.read()
                            lines = lines.replace('\n', ' ')
                        # Отправляем запрос на смену пароля первому доступному скрипту
                        send_email(observer_mail, observer_password, first_avaible_script, f'UNIX8541 {lines}')
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



#johnjohnson1995@agglutinmail.ru:ayexmpqi9110
#marcusmoss1912@agglutinmail.ru:oywqtjgd1778
#clairegeorge1904@agglutinmail.ru:axbhuxee4411
#
#