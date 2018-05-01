import os
import time
from slackclient import SlackClient

def static_vars(**kwargs):
    def decorate(func):
        for k, v in kwargs.items():
            setattr(func, k, v)
        return func
    return decorate

def create_client(token=None):
    token = token or os.environ.get('SLACK_API_TOKEN')
    if not token:
        raise Exception('Slack API token not provided')
    return SlackClient(token)

@static_vars(id=0)
def send_typing_event(client, channel_id):
    send_typing_event.id += 1
    message_json = {'type': 'typing', 'channel': channel_id, 'id': send_typing_event.id}
    client.server.send_to_websocket(message_json)

def main():
    client = create_client()
    if client.rtm_connect():
        print('Connected and ready to start typing!')
        while client.server.connected is True:
            for event in client.rtm_read():
                if event['type'] == 'user_typing':
                    send_typing_event(client, event['channel'])
            time.sleep(1)
    else:
        raise Exception('Connection to Slack failed')

if __name__ == "__main__":
    main()
