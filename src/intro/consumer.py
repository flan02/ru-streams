# Use Case: Streams example with Python
# ?  Usage: Part of Redis University RU202 courseware
from client import get_redis_client
from redis.exceptions import ResponseError
import time
import json
import socket
# import os


def write_to_data_warehouse(results):
    if len(results) > 0:
        print("Wrote " + json.dumps(results) + " to data warehouse.\n")


def main():
    redis = get_redis_client()

    stream_key = "stream:weather"
    group_name = "data_warehouse_writer"
    consumer_name = "consumer-" + socket.gethostname() + "-a"
    block_ms = 5000
    stream_offsets = {stream_key: ">"}

    if not redis.exists(stream_key):
        print(f"Stream {stream_key} does not exist.  Try running the producer first.")
        exit(0)

    try:
        redis.xgroup_create(stream_key, group_name)
    except ResponseError:
        print("Group already exists.")

    while True:
        results = redis.xreadgroup(
            group_name,
            consumer_name,
            stream_offsets,  # type: ignore
            None,
            block_ms,  # type: ignore
        )
        write_to_data_warehouse(results)
        time.sleep(1)


if __name__ == "__main__":
    main()
