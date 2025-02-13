import re
import time
import imaplib
import email
from email.header import decode_header
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def read_codes_from_steam(imap_server, email_address, password):
    # Обрабатываем биг ашипку
    try:
        # Устанавливаем соединение с имап сервером
        mail = imaplib.IMAP4_SSL(imap_server, port=993)
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
                                    result = re.findall(r'Код подтверждения вашего аккаунта:\n*\s*\n*\w{5}|Login Code\s*\n*\s*\w{5}', body)

                        else:
                            body = email_message.get_payload(decode=True).decode()
                            result = re.findall(r'Код подтверждения вашего аккаунта:\s*\w{5}|Login Code\s*\n\s*\w{5}', body)
                        # Если в тексте сообщения есть код
                        if result != []:
                            code = result[0].split()[-1]
                            # Выводим в консоль
                            print(f"Почта: {email_address}")
                            print(f'Код: {code}')
                            return code
        # Обработка ашипак
            else:
                pass
                #print(f'На почте {email_address} нет писем.')
        else:
            pass
            #print(f'Не удалось найти письма на почте {email_address}.')

    # Апять обработка биг ашипки
    except Exception as e:
        print(f'Ошибка при работе с почтой {email_address}: {e}')

#zxcvbn8541
login = 'zxcvbn85411'
#nr4s8cx1
password = 'nr4s8cx1'

new_password = 'nr4s8cx12'

email = 'johnjohnson1995@agglutinmail.ru'

email_password = 'ayexmpqi9110'



options = Options()
options.add_experimental_option('detach', True)

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

browser.get('https://store.steampowered.com/login/?redir=&redir_ssl=1&snr=1_4_4__global-header')
time.sleep(1)
login_button, password_button = browser.find_elements(By.CLASS_NAME, '_2GBWeup5cttgbTw8FM3tfx')



login_button.send_keys(login)
password_button.send_keys(password)

button = browser.find_element(By.CLASS_NAME, 'DjSvCZoKKfoNSmarsEcTS')
button.click()

time.sleep(3)

pulldown = browser.find_element(By.ID, 'account_pulldown')
pulldown.click()

account = browser.find_elements(By.CLASS_NAME, 'popup_menu_item')[1]
account.click()
time.sleep(1)
change_password = browser.find_elements(By.CLASS_NAME, 'account_manage_link')[-5]

change_password.click()
time.sleep(3)

send_code = browser.find_element(By.XPATH, "//a[@class='help_wizard_button help_wizard_arrow_right']")
send_code.click()
time.sleep(2)
forgot_password = browser.find_element(By.XPATH, '//input[@id="forgot_login_code"]')
#rebeccawhitney1986@agglutinmail.ru    qucgbfpm7271
while True:
    code = read_codes_from_steam('imap.firstmail.ru', email, email_password)
    if code != None:
        break

forgot_password.send_keys(code)

submit = browser.find_element(By.XPATH, '//input[@type="submit"]')
submit.click()
time.sleep(1)
password_reset = browser.find_element(By.ID, 'password_reset')
password_reset_confirm = browser.find_element(By.ID, 'password_reset_confirm')
time.sleep(1)
password_reset.send_keys(new_password)
password_reset_confirm.send_keys(new_password)
time.sleep(1)
last_submit = browser.find_element(By.XPATH, '//input[@type="submit"]')
last_submit.click()