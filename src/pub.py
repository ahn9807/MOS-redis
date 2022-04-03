from email import message
import redis_core
from redis_core import redis_conn


def push_object(data):
    pickle_data = data

    redis_conn.publish(channel=redis_core.STREAM_NAME, message=pickle_data)
