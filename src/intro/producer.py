# Use Case: Streams example with Python
# ? Usage: Part of Redis University RU202 courseware
# from redis import Redis
from client import get_redis_client
import random
import time
import json
# import os


class Measurement:
    def __init__(self):
        self.postal_codes = [94016, 80014, 60659, 10011]
        self.current_temp = 50
        self.max_temp = 100
        self.min_temp = 0

    def get_next(self):
        if random.random() >= 0.5:
            if self.current_temp + 1 <= self.max_temp:
                self.current_temp += 1
        elif self.current_temp - 1 >= self.min_temp:
            self.current_temp -= 1

        return {
            "postal_code": random.choice(self.postal_codes),
            "temp_f": self.current_temp,
        }


def main():
    redis = get_redis_client()
    stream_key = "stream:weather"
    measurement = Measurement()

    while True:
        entry = measurement.get_next()
        id = redis.xadd(stream_key, entry, "*")  # type: ignore
        print("Wrote " + json.dumps(entry) + " with ID " + id)  # type: ignore
        time.sleep(1)


if __name__ == "__main__":
    main()

# python -m src.intro.producer
