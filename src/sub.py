from datetime import time
import time

import redis_core
from redis_core import db


def handle_raw_data(raw_data):
	pickle_data = raw_data
	print(pickle_data)

def redis_ttl(timestamp):
	if redis_core.DEFAULT_TTL_SEC != 0:
		# Trim TTL_SEC + 1 for remove data over TTL limits
		db.xtrim(
			name=redis_core.STREAM_NAME,
			maxlen=None,
			minid=timestamp - (redis_core.DEFAULT_TTL_SEC + 1) * 1000
		)

if __name__ == '__main__':
	last_timestamp = 0
	last_sys_timestamp = redis_core.db_time_ms()
	last_len = db.xlen(name=redis_core.STREAM_NAME)

	while(1):
		# In first action, fetch the latest data from stream
		if last_timestamp == 0:
			raw_data = db.xread(streams={redis_core.STREAM_NAME: "$"}, block=redis_core.TIMEOUT_MS)
		# From second actions, fetch the data which pass the lastest timestamp from stream 
		else:
			raw_data = db.xread(streams={redis_core.STREAM_NAME: last_timestamp}, block=redis_core.TIMEOUT_MS)

		# Parse data and call callback			
		if raw_data != []:
			recv_data = raw_data[0][1][0][1]
			last_timestamp = raw_data[0][1][0][0]
			handle_raw_data(recv_data)

		# Remove elements by TTL
		if time.time_ns() - last_sys_timestamp > redis_core.DEFAULT_TTL_INTV_MS * 1000_000:
			last_sys_timestamp = redis_core.db_time_ms()
			redis_ttl(last_sys_timestamp)