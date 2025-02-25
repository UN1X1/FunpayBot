import re
import time
import imaplib
import email
import random
import string
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


class SteamError(Exception):
    pass

class FunpayError(Exception):
    pass

script_email = 'qwerty.zxc.1@mail.ru' # имэйл скрипта
script_password = 'mFzk2sYkJ8LRTLTapvZL'
script_name = 'Script2'

symbols = string.ascii_letters + string.digits + string.digits + string.digits

def password_generator(old_password):
    return ''.join([random.choice(symbols) for i in range(4)]) + 'Unix' + ''.join([random.choice(symbols) for i in range(4)])





# Функция для чтения кодов от стима
def read_codes_from_steam(email_address, password):
    try:
        url = f"https://api.firstmail.ltd/v1/mail/one?username={email_address}&password={password}"
        headers = {
            "accept": "application/json",
            "X-API-KEY": "a7abdc28-c922-4c86-a752-54b9e9f44497"
        }

        response = requests.get(url, headers=headers)

        email_json = response.text

        zxc = json.loads(email_json)

        result = re.findall(
            r'Код подтверждения вашего аккаунта:\n*\s*\n*\w{5}|Login Code\s*\n*\s*\w{5}',
            zxc['text'])
        if result:
            code = result[0].split()[-1]
            print(f'Почта: {email_address}\nКод: {code}')
            return code
        else:
            return False
    except Exception as e:
        print(f'Ошибка при работе с почтой {email_address}', e)




def write_file(file_name, text):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(text)

def read_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        file_info = file.read().strip().split()
    with open(file_name, 'w') as file:
        pass
    return file_info


# Задаем параметы браузера
useragent = UserAgent()
options = Options()
options.add_experimental_option('detach', True)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'user-agent={useragent.random}')
# Создаем объект браузера

# Функция для смены пароля в стиме
def password_changer(browser, login_steam, password_steam, new_password_steam, adr_email, password_email):
    browser.get('https://store.steampowered.com/login/?redir=&redir_ssl=1&snr=1_4_4__global-header')
    time.sleep(1)
    # Вводим логин пароль
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
    # Вводим код с почты для смены пароля
    time.sleep(15)
    while True:
        code = read_codes_from_steam(adr_email, password_email)
        if code:
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

# Функция для апдейта паролей на фанпей
def funpay_update(browser, steam_login, steam_password, keywordtitle, keywordlot):
    browser.get('https://funpay.com/account/login')
    time.sleep(2)
    # Вводим логин пароль
    login = browser.find_element(By.NAME, 'login')
    password = browser.find_element(By.NAME, 'password')
    login.send_keys('qwerty8541')
    password.send_keys('Gde-DilleR-854')
    # 6LdTYk0UAAAAAGgiIwCu8pB3LveQ1TcLUPXBpjDh
    sitekeyx = '//*[@id="content"]/div/div/div/form/div[4]/div'
    sitekey = WebDriverWait(browser, 5).until(
        expected_conditions.presence_of_element_located((By.XPATH, sitekeyx))).get_attribute(
        'outerHTML')
    # Решаем капчу
    clean_sitekey = sitekey.split('"')[3]
    # Задаем параметры для решения капчи
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key('d1e6d8ecb0acfca8bbc0265706d0e3d4')
    solver.set_website_url('https://funpay.com/account/login')
    solver.set_website_key(clean_sitekey)
    # Получаем решенную капчу
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
    time.sleep(3)
    submit = browser.find_element(By.XPATH, '//button[@class="btn btn-primary btn-block"]')
    submit.click()
    time.sleep(1)

    browser.get('https://funpay.com/users/11085243/')

    titles = browser.find_elements(By.CLASS_NAME, 'offer-list-title')
    pencils = browser.find_elements(By.XPATH, '//a[@class="btn btn-default btn-plus"]')
    # Ищем нужный раздел
    for i, title in enumerate(titles):
        if keywordtitle in title.get_attribute('innerHTML'):
            pencils[i].click()
            break
    # Ищем нужное объявление
    lots = browser.find_elements(By.CLASS_NAME, 'tc-item')
    isactive = browser.find_elements(By.XPATH, '//div[@class="tc-amount hidden-xxs"]')

    flag = False
    # Проверяем активно ли оно
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

    last_submit = browser.find_element(By.XPATH,'//button[@class="btn btn-primary btn-block js-btn-save"]')
    last_submit.click()


def main():
    # Чекаем сообщения на почте
    while True:
        with open('request.txt', 'r') as file:
            txt = file.read()
        # Если пришло
        if script_name in txt:
            with open('request.txt', 'w') as file:
                pass
            id, steam_login, steam_password, new_steam_password, email_adr, email_password, key_word_in_title, key_word_in_lot, t = txt.split()
            time.sleep(float(t) * 3600)
            browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            # Меняем пароль
            for i in range(3):
                try:
                    password_changer(browser, steam_login, steam_password, new_steam_password, email_adr, email_password)
                except Exception as e:
                    print('в смене пароля стим произошла ошибка', e)
                    continue
                break
            else:
                raise SteamError('Скорее всего программа не смогла поменять пароль на стим')
            # Кидаем его на фп
            for i in range(5):
                try:
                    funpay_update(browser, steam_login, new_steam_password, key_word_in_title, key_word_in_lot)
                except Exception as e:
                    print('на фп произошла ошибка', e)
                    continue
                break
            else:
                raise FunpayError('Произошла ошибка при обновлении данных на фанпей')
            # Отправляем запрос от том что скрипт закончил работу
            with open('ValidScripts.txt', 'a') as file:
                file.write(f'{script_name}\n')

            with open(f'{steam_login}.txt', 'r') as file:
                lines = file.read().split('\n')
            lines[1] = new_steam_password
            lines[2] = password_generator(lines[2])

            with open(f'{steam_login}.txt', 'w') as file:
                print(*lines, sep='\n', file=file)

            print('script2 поменял пароль и обновил данные на фп')


print('Script2')
main()
