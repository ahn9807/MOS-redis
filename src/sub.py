import redis_core
from redis_core import redis_conn


def handle_raw_data(raw_data):
    pickle_data = raw_data
    print(pickle_data)


if __name__ == '__main__':
    pubsub = redis_conn.pubsub()

    pubsub.subscribe(redis_core.STREAM_NAME)

    while True:
        raw_data = pubsub.get_message(timeout=redis_core.TIMEOUT_SEC)
        if raw_data != None:
            handle_raw_data(raw_data)
