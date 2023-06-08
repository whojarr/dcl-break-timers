import json
from skpy import Skype


class SkypeClient():

    def __init__(self, username, password):

        self.skype_obj = Skype(username, password)

    def chats_recent(self):
        result = []

        chats = self.skype_obj.chats.recent()

        for id in chats:
            print(chats[id])
            chat_type = id.split(':')[0]
            chat_name = id.split(':')[1]
            if chat_type == '19':
                result.append({'id': id, 'name': chats[id].topic})
            else:
                result.append({'id': id, 'name': chat_name})

        return result


    def chat_send(self, channel_id, msg):
        channel = self.skype_obj.chats.chat(channel_id) 
        channel.sendMsg(msg)


if __name__ == "__main__":
    sc = SkypeClient('whojarr@gmail.com', 'Augur5032020')

    print(sc.chat_send('19:4ca88a0066964629978ad3a4576bff36@thread.skype', 'test message: direct from timer.html'))