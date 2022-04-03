from sqlite3 import Timestamp
from attr import fields
import redis_core
from redis_core import db


def push_object(data):
    pickle_data = data

    oid = db.xadd(name=redis_core.STREAM_NAME, fields={
        redis_core.STREAM_DATA_STR: pickle_data,
    })