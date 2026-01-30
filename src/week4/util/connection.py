"""
Redis connection utilities
"""

import os
from redis import Redis
from dotenv import load_dotenv


load_dotenv()


def get_connection(name=None):
    """Returns an optionally-named connection to Redis"""
    HOST = os.environ.get("REDIS_HOST", "localhost")
    PORT = int(os.environ.get("REDIS_PORT", 18601))
    USERNAME = os.environ.get("REDIS_USER", "default")
    PASSWORD = os.environ.get("REDIS_PASSWORD")

    # client_kwargs = {"host": HOST, "port": PORT, "decode_responses": True}
    client_kwargs = {
        "host": HOST,
        "port": PORT,
        "decode_responses": True,
        "username": USERNAME,
        "password": PASSWORD,
    }

    return Redis(**client_kwargs)


# Instancia única para usar en todo el curso
redis_client = get_connection()

__all__ = ["redis_client"]

# if USERNAME:
#     client_kwargs["username"] = USERNAME

# if PASSWORD:
#     client_kwargs["password"] = PASSWORD

# redis = Redis(**client_kwargs)

# if name is not None:
#     redis.client_setname(name)
# return redis
