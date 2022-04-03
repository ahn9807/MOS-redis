from datetime import time
import time

import redis_core
from redis_core import db


def redis_callback(raw_data):
	pickle_data = raw_data
	print(pickle_data)

def redis_ttl():
	if redis_core.DEFAULT_TTL_SEC != 0:
		db.xtrim(
			name=redis_core.STREAM_NAME,
			maxlen=None,
			minid=redis_core.db_time_ms() - (redis_core.DEFAULT_TTL_SEC + 1) * 1000
		)

if __name__ == '__main__':
	last_timestamp = time.time_ns()
	last_len = db.xlen(name=redis_core.STREAM_NAME)

	while(1):
		raw_data = db.xread(streams={redis_core.STREAM_NAME: "$"}, block=5000)
		redis_callback(raw_data)

		# Remove elements by TTL
		if time.time_ns() - last_timestamp > redis_core.DEFAULT_TTL_SEC * 1000_000_000:
			last_timestamp = time.time_ns()
			redis_ttl()