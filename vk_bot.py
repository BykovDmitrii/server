import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import requests

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id":123456})


url = input()
token = input()
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            r = requests.post(url, data=str({"text": event.text, "user_id": event.user_id}))
            print(r.text)
            write_msg(event.user_id, "Ваша заявка добавлено ее номер {}".format(r.text))
