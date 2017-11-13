import pytest
import gdax
import os
import time

API_KEY=os.environ['API_KEY']
API_SECRET=os.environ['API_SECRET']
API_PASSPHRASE=os.environ['API_PASSPHRASE']

class AuthWebsocketClient(gdax.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.gdax.com"
        self.products = ["BTC-USD"]
        self.auth = True
        self.api_key=API_KEY
        self.api_secret=API_SECRET
        self.api_passphrase=API_PASSPHRASE
        self.messages = []
        self.opened = True
        self.channels = ['heartbeat']

    def on_message(self, msg):
        self.messages.append(msg)

    def on_close(self):
        self.opened = False

@pytest.fixture(scope='module')
def client():
    return AuthWebsocketClient()

@pytest.mark.usefixtures('client')
class TestAuthWebsocketClient(object):
    def test_can_open_close(self, client):
        client.start()
        assert client.opened
        client.close()
        assert not client.opened

    def test_get_heartbeat(self, client):
        client.start()
        assert client.opened
        time.sleep(5)
        num_messages = len(client.messages)
        print('Got {0} messages'.format(num_messages))
        assert num_messages >= 1
        client.close()
        assert not client.opened
