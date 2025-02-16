from FunPayAPI import Account, Runner, types, enums


TOKEN = "0vspp63qr7h9x3ogym6cd9r0bj5h6dlc"

# Создаем класс аккаунта и сразу же получаем данные аккаунта.
acc = Account(TOKEN).get()

# Создаем класс "прослушивателя" событий.
runner = Runner(acc)


acc.send_message(113580727, "789")  # отправляем ответное сообщение