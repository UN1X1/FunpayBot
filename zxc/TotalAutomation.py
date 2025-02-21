import re
import time
import smtplib
import imaplib
import email
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

token = 'd1e6d8ecb0acfca8bbc0265706d0e3d4'
url = 'https://funpay.com/account/login'
funpay_login = 'qwerty3569'
funpay_password = 'Gde-DilleR-854'
observer_mail = 'observer1.0@mail.ru'
observer_password = 'CKUPxQATVjsuUZe26hEw'


# Параметры для браузера
useragent = UserAgent()
options = Options()
options.add_experimental_option('detach', True)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'user-agent={useragent.random}')
# Создаем объект браузера
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

scripts_emails = ['qwerty.zxc.1@mail.ru', 'qwerty.zxc.2@mail.ru', 'qwerty.zxc.3@mail.ru']

server = smtplib.SMTP_SSL('smtp.mail.ru', 465)



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
        print(f'Ошибка при работе с почтой {email_address}: {e}')


def send_email(sender, pasword, getter, msg_text):
    msg = MIMEText(f'{msg_text}', 'plain', 'utf-8')
    msg['Subject'] = 'Данные об аккаунте стим'
    msg['To'] = getter
    server.login(sender, pasword)
    server.sendmail(sender, getter, msg.as_string())


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
    time.sleep(1)
    browser.execute_script(
        """document.getElementById("g-recaptcha-response").innerHTML = arguments[0]""", gresponse)
    time.sleep(1)
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

    # Бесконечный цикл который чекает новые заказы
    while True:
        flag = False
        message = check_email(observer_mail, observer_password)
        if message != None:
            print(message.split())
            scripts_emails.append(message.split()[0])
        browser.refresh()
        time.sleep(1)
        try:
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
            # Пролистываем сообщения
            for i, msg in enumerate(msgs[:15]):
                try:
                    msg_text = msg.find_element(By.CLASS_NAME, 'chat-msg-text').text
                    match = re.findall(r'Логин: ([\w\d]+) Пароль: [\w\d]+', msg_text)
                    if match:
                        print(match[0])
                        # suytreso@bonjourfmail.com     svojwisxS!1955
                        send_email(observer_mail, observer_password, scripts_emails[0], 'zxcvbn8541 Q1Fs3f74!1234 Q1Fs3f74!12345 rebeccawhitney1986@agglutinmail.ru  qucgbfpm7271 Russia Blue 0.0001')
                        print('zxcvbn8541 Q1Fs3f74!1 Q1Fs3f74!12 rebeccawhitney1986@agglutinmail.ru  qucgbfpm7271 ARK ark 0.0001')
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

# r'\s*[Лл]огин\s*:* ([\w\d]+) [Пп]ароль\s*:* [\w\d]+\s*'
observer(funpay_login, funpay_password, token)