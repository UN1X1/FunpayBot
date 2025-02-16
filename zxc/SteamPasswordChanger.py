import re
import time
import imaplib
import email
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


token = 'd1e6d8ecb0acfca8bbc0265706d0e3d4'
url = 'https://funpay.com/account/login'


def read_codes_from_steam(email_address, password):
    # Обрабатываем биг ашипку
    try:
        # Устанавливаем соединение с имап сервером
        mail = imaplib.IMAP4_SSL('imap.firstmail.ru', port=993)
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
                            print(f'Почта: {email_address}')
                            print(f'Код: {code}')
                            return code

    # Апять обработка биг ашипки
    except Exception as e:
        print(f'Ошибка при работе с почтой {email_address}: {e}')


#zxcvbn8541
steam_login = 'zxcvbn854111'  # логин стим
#nr4s8cx1
steam_password = 'nr4s8cx12345678' #

new_steam_password = 'nr4s8cx123456789'

email_adr = 'marcusmoss1912@agglutinmail.ru'

email_password = 'oywqtjgd1778'

funpay_login = 'qwerty8541'

funpay_password = 'Gde-DilleR-854'


useragent = UserAgent()
options = Options()
options.add_experimental_option('detach', True)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'user-agent={useragent.random}')

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def password_changer(login_steam, password_steam, new_password_steam, adr_email, password_email):
    browser.get('https://store.steampowered.com/login/?redir=&redir_ssl=1&snr=1_4_4__global-header')
    time.sleep(1)
    login_button, password_button = browser.find_elements(By.CLASS_NAME, '_2GBWeup5cttgbTw8FM3tfx')

    login_button.send_keys(login_steam)
    password_button.send_keys(password_steam)

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
    time.sleep(2)

    send_code = browser.find_element(By.XPATH, "//a[@class='help_wizard_button help_wizard_arrow_right']")
    send_code.click()
    time.sleep(2)
    forgot_password = browser.find_element(By.XPATH, '//input[@id="forgot_login_code"]')
    #rebeccawhitney1986@agglutinmail.ru    qucgbfpm7271

    while True:
        code = read_codes_from_steam(adr_email, password_email)
        print('working')
        if code != None:
            break

    forgot_password.send_keys(code)

    submit = browser.find_element(By.XPATH, '//input[@type="submit"]')
    submit.click()
    time.sleep(1)

    password_reset = browser.find_element(By.ID, 'password_reset')
    password_reset_confirm = browser.find_element(By.ID, 'password_reset_confirm')
    time.sleep(1)

    password_reset.send_keys(new_password_steam)
    password_reset_confirm.send_keys(new_password_steam)
    time.sleep(1)

    last_submit = browser.find_element(By.XPATH, '//input[@type="submit"]')
    last_submit.click()
    time.sleep(2)


def funpay_update(login, password, token, steam_login, steam_password):
    sitekeyx = '//*[@id="content"]/div/div/div/form/div[4]/div'
    browser.get(url)
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
    time.sleep(3)
    submit = browser.find_element(By.XPATH, '//button[@class="btn btn-primary btn-block"]')
    submit.click()

    browser.get('https://funpay.com/users/11085243/')

    titles = browser.find_elements(By.CLASS_NAME, 'offer-list-title')
    pencils = browser.find_elements(By.XPATH, '//a[@class="btn btn-default btn-plus"]')

    for i, title in enumerate(titles):
        if 'Black Russia' in title.get_attribute('innerHTML'):
            pencils[i].click()
            break

    lots = browser.find_elements(By.CLASS_NAME, 'tc-item')
    isactive = browser.find_elements(By.XPATH, '//div[@class="tc-amount hidden-xxs"]')

    flag = False

    for isact, lot in zip(isactive, lots):
        if 'Samara' in lot.get_attribute('innerHTML'):
            if '0' in isact.get_attribute('outerHTML'):
                flag = True
            lot.click()
            break

    time.sleep(1)

    textarea = browser.find_element(By.XPATH,
                                    '//textarea[@class="form-control textarea-lot-secrets"]')

    textarea.send_keys(f'\nЛогин: {steam_login} Пароль: {new_steam_password}')

    if flag:
        zxc = browser.find_elements(By.XPATH, '//i')[-3]
        zxc.click()

    last_submit = browser.find_element(By.XPATH,
                                       '//button[@class="btn btn-primary btn-block js-btn-save"]')
    last_submit.click()


def main():
    password_changer(steam_login, steam_password, new_steam_password, email_adr, email_password)
    funpay_update(funpay_login, funpay_password, token, steam_login, steam_password)


if __name__ == '__main__':
    main()