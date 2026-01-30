import os
from redis import Redis
from dotenv import load_dotenv

load_dotenv()


def get_redis_client():
    """Configura y retorna el cliente de Redis."""
    host = os.getenv("REDIS_HOST", "localhost")
    port = int(os.getenv("REDIS_PORT", 18601))
    username = os.getenv("REDIS_USER", "default")
    password = os.getenv("REDIS_PASSWORD")

    client_kwargs = {
        "host": host,
        "port": port,
        "decode_responses": True,
        "username": username,
        "password": password,
    }

    return Redis(**client_kwargs)


# Instancia única para usar en todo el curso
redis_client = get_redis_client()

__all__ = ["redis_client"]
