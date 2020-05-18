import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class VideoConsumer(WebsocketConsumer):
    def connect(self):
        """
        When connecting to WebSocket a group is created for every single WebSocket instance
        :return:
        """
        self.progress_name = self.scope['url_route']['kwargs']['id']
        self.progress_group_name = 'group_%s' % self.progress_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.progress_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        """
        Upon receiving of WebSocket Message, a response is send back to specific progress instance ( its own group)
        :param text_data: text to send back to client
        :return:
        """
        self.channel_layer.group_send(
            self.progress_group_name,
            {
                'type': 'message',
                'message': "pong"
            }
        )

    def disconnect(self, close_code):
        """
        Progress group is deleted
        :param close_code:
        :return:
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.progress_group_name,
            self.channel_name
        )

    # def channel_message(self, event):
    #     """
    #     Simply send a message to a channel/group
    #     :param event: Triggering the sending
    #     :return:
    #     """
    #     message = event['message']
    #     # Send message to WebSocket
    #     self.send(text_data=json.dumps({
    #         'back': 'received'
    #     }))
