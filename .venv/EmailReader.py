# Импортируем много блатни библиотек
import re
import imaplib
import email
from email.header import decode_header
from idlelib.iomenu import encoding
import telebot

bot = telebot.TeleBot('7550686496:AAGlbFQky77g8XH3iDcHyuYS6Sy2xvm-scY')



# Функция которая считывает все коды Стим с одной почты
def read_codes_from_steam(email_address, password):
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
                                    #result = re.findall(r'Код подтверждения вашего аккаунта:\n*\s*\n*\w{5}|Login Code\s*\n*\s*\w{5}', body)

                        else:
                            body = email_message.get_payload(decode=True).decode()
                            #result = re.findall(r'Код подтверждения вашего аккаунта:\s*\w{5}|Login Code\s*\n\s*\w{5}', body)
                        # Если в тексте сообщения есть код
                        if body != []:
                            #code = result[0].split()[-1]
                            # Кидаем в тг
                            #bot.send_message(5734729388, f"Почта: {email_address}\nИгра: {game}")
                            #bot.send_message(5734729388, code)
                            # Выводим в консоль
                            print(f"Почта: {email_address}")
                            print(f'Код: {body}')
                            return body
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


# Це типо дата бэйз с логами почт
email_accounts = [
    {
        'imap_server': 'imap.firstmail.ru',
        'email': 'amosmain1981@directoromail.ru',
        'password': 'ckhamsre5899',
        'game': 'assetto corsa'
    },
    {
        'imap_server': 'imap.firstmail.ru',
        'email': 'loviehorn1979@directoromail.ru',
        'password': 'jpitmphb1472',
        'game': 'assetto corsa'
    },
    {
        'imap_server': 'imap.firstmail.ru',
        'email': 'zqhluhsh@lamesamail.com',
        'password': 'guddemGta2',
        'game': 'forest'
    },
    {
        'imap_server': 'imap.firstmail.ru',
        'email': 'ejgxjswm@lamesamail.com',
        'password': 'guddemGta2',
        'game': 'forest'
    },
    {
        'imap_server': 'imap.firstmail.ru',
        'email': 'qvupaowc@lapasamail.com',
        'password': 'guddemGta2',
        'game': 'forest'
    },
    {
        'imap_server': 'imap.firstmail.ru',
        'email': 'simondial2011@directoromail.ru',
        'password': 'guddemGta2',
        'game': 'The outlast Trials'
    },
    {
        'imap_server': 'imap.firstmail.ru',
        'email': 'thomasriley1953@uranosc.ru',
        'password': 'guddemGta2',
        'game': 'RDR2'
    },
    {
        'imap_server': 'imap.firstmail.ru',
        'email': 'samanthamorgan1901@firstmailler.net',
        'password': 'guddemGta2',
        'game': 'It takes two'
    },
    {
        'imap_server': 'imap.firstmail.ru',
        'email': 'samathastarns2014@firstmailler.net',
        'password': 'guddemGta2',
        'game': 'It takes two'
    },
    {
        'imap_server': 'imap.firstmail.ru',
        'email': 'sammiedavis1936@firstmailler.net',
        'password': 'guddemGta2',
        'game': 'It takes two'
    },
    {
        'imap_server': 'imap.firstmail.ru',
        'email': 'katebray2004@directoromail.ru',
        'password': 'hrcqtuxy7951',
        'game': 'HOI4'
    },
    {
        'imap_server': 'imap.firstmail.ru',
        'email': 'sammynichols1996@firstmailler.net',
        'password': 'guddemGta2',
        'game': 'Battlefield 5'
    },
    {
        'imap_server': 'imap.firstmail.ru',
        'email': 'michaelalexander1923@directoromail.ru',
        'password': 'ksmqdbuy7452',
        'game': 'Asseto Corza + Competizione'
    }
]

#

# Бесконечный цикл
while True:
    # Проходимся по почтам и чекаем есть ли там не прочитанные сообщения
    #for account in email_accounts:
        #t = read_codes_from_steam(account['imap_server'], account['email'], account['password'], account['game'])
    read_codes_from_steam('observer1.0@mail.ru', 'CKUPxQATVjsuUZe26hEw')

    print("-" * 50)
