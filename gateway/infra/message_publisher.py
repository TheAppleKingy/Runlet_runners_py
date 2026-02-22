import pika
import threading
import time

from pika.adapters.blocking_connection import BlockingChannel

from gateway.application.interfaces import MessagePublisherInterface


class RabbitPublisher(MessagePublisherInterface):
    def __init__(
        self,
        conn_url: str,
        queue_name: str
    ):
        self._conn_url = conn_url
        self._connection: pika.BlockingConnection = None
        self._channel: BlockingChannel = None
        self._queue_name = queue_name
        self._is_running = False

    def connect(self):
        if not self._connection or self._connection.is_closed:
            params = pika.URLParameters(self._conn_url)
            params.heartbeat = 120
            params.blocked_connection_timeout = 600.0
            self._connection = pika.BlockingConnection(
                params
            )
        self._is_running = True
        threading.Thread(target=self._heartbeat, daemon=True).start()

    def _heartbeat(self):
        while self._is_running:
            time.sleep(60)
            conn = self._check_connection()
            conn.process_data_events()

    def _check_connection(self):
        self.connect()
        return self._connection

    def _get_channel(self):
        if not self._channel or self._channel.is_closed:
            conn = self._check_connection()
            self._channel = conn.channel()
        return self._channel

    def publish(self, data: str):
        chan = self._get_channel()
        chan.basic_publish(
            "",
            self._queue_name,
            data,
            pika.BasicProperties(
                content_type="application/json",
                delivery_mode=2,
                headers={"task_name": "handle_test_result"}
            )
        )

    def disconnect(self):
        if self._channel and self._channel.is_open:
            self._channel.close()
        self._channel = None
        if self._connection and self._connection.is_open:
            self._connection.close()
        self._connection = None
