import requests
from multiprocessing import Process
import time
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import vk_api
import os

token = 'c5f759ca8743782c2343cc1947a08b88c9be5a89b80044fe71597dda90c830e94227b202bc68c2bc8c652'
vk_session = vk_api.VkApi(token=token)

session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
status = 0


def send_message(message, user_id):
    vk_session.method('messages.send',
                      {'user_id': user_id,
                       'message': message,
                       'random_id': get_random_id()})


def listen():
    while True:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                response = event.text.lower()
                if event.from_user and not event.from_me:
                    user_id = int(event.user_id)
                    print(user_id)
                    if response == 'start':
                        f = open('qwer', 'a')
                        lst = user_id
                        f.write(str(lst) + '\n')
                        f.close()
                        vk_session.method('messages.send', {'peer_id': user_id, 'message': 'Ready', 'random_id': 0})
                        P2 = Process(name='send', target=send)
                        P2.daemon = True
                        P2.start()
                    if response == 'status':
                        rBot = requests.get('http://localhost:5000/api/status').json()
                        status = rBot['status']
                        send_message(status, user_id)


def send():
    r = requests.get('http://localhost:5000/api/start').text
    if r == 'ok':
        while True:
            rBot = requests.get('http://localhost:5000/api/status').json()
            status = rBot['status']
            print(status)
            if status == 'Done':
                f = open('qwer')
                for l_u in f.readlines():
                    send_message('Done ', int(l_u))
                os.system(r'nul>qwer')
                break
            time.sleep(1)


if __name__ == '__main__':
    listen()
