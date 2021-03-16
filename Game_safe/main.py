from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
import random
import sys
from datetime import datetime
sys.path.insert(0, '../')

token = "c5f759ca8743782c2343cc1947a08b88c9be5a89b80044fe71597dda90c830e94227b202bc68c2bc8c652"
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print("Сообщение пришло в: " + str(datetime.strftime(datetime.now(), "%H:%M:%S")))
            print("Текст сообщения: " + str(event.text))
            print(event.user_id)
            response = event.text.lower()
            if event.from_user and not (event.from_me):
                if response == 'привет':
                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Приветик!', 'random_id': 0})
                elif response == 'пока':
                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'До скорой встречи!', 'random_id': 0})
                elif response == 'сейф':
                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Введите трехзначный код: ', 'random_id': 0})
                    for event in longpoll.listen():
                        if event.from_user and not (event.from_me):
                            if event.type == VkEventType.MESSAGE_NEW:
                                response1 = event.text.lower()
                                k = len(set(response1))  # количество различных цифр
                                if k == 3:  # Все разные
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Все OK!', 'random_id': 0})
                                    break
                                elif k == 2:  # Две одинаковые
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'В числе две одинаковые цифры!', 'random_id': 0})
                                    break
                                else:  # Все одинаковые
                                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'В числе три одинаковые цифры!', 'random_id': 0})
                                    break
                else:
                    vk_session.method('messages.send', {'user_id': event.user_id, 'message': 'Я не понимаю, что Вы сказали', 'random_id': 0})