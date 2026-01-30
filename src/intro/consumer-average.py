# Use Case: Streams example with Python
# Usage: Part of Redis University RU202 courseware
from client import get_redis_client
from redis.exceptions import ResponseError
from collections import deque
import time
import json
import socket


def print_yellow(text):
    print("\033[93m" + text + "\033[0m")


def get_rolling_average(results, window):
    total = 0
    for result in results[0][1]:
        values = result[1]
        temperature = int(values["temp_f"])
        if len(window) < 10:
            window.append(temperature)
        else:
            window.popleft()
            window.append(temperature)
    for measurement in window:
        total += measurement

    return total / len(window)


def main():
    redis = get_redis_client()

    stream_key = "stream:weather"
    group_name = "rolling_average_printer"
    consumer_name = "consumer-" + socket.gethostname() + "-a"
    block_ms = 5000
    stream_offsets = {stream_key: ">"}
    window = deque([])

    if not redis.exists(stream_key):
        print(f"Stream {stream_key} does not exist.  Try running the producer first.")
        exit(0)

    try:
        redis.xgroup_create(stream_key, group_name)
    except ResponseError:
        print_yellow("Group already exists.")

    while True:
        results = redis.xreadgroup(
            group_name,
            consumer_name,
            stream_offsets,  # type: ignore
            None,
            block_ms,  # type: ignore
        )

        if len(results) > 0:  # type: ignore
            print_yellow("Processing: " + json.dumps(results))
            print_yellow(
                "Rolling Average: " + str(get_rolling_average(results, window))
            )

        time.sleep(1)


if __name__ == "__main__":
    main()
