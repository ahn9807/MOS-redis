from sqlite3 import Timestamp
import redis

redis_conn = redis.Redis(host='localhost', port=6379, db=0)

STREAM_NAME = "MOS_STREAM"
STREAM_DATA_STR = "data"
DEFAULT_TTL_SEC = 10
TIMEOUT_SEC = 1

def db_time_us():
    cur_time = redis_conn.time()
    return cur_time[0] * 1000_000 + cur_time[1]

def db_time_ms():
	return int(db_time_us() / 1000)