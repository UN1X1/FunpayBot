import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


options = Options()
options.add_experimental_option('detach', True)

browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

browser.get('https://store.steampowered.com/login/?redir=&redir_ssl=1&snr=1_4_4__global-header')
time.sleep(1)
email, password = browser.find_elements(By.CLASS_NAME, '_2GBWeup5cttgbTw8FM3tfx')


email.send_keys('jrwth85360')

password.send_keys('cetq00619F')

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

send_code = browser.find_element(By.ID, 'help_wizard_button help_wizard_arrow_right')
ы