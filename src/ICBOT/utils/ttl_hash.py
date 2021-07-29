import time


def get_ttl_hash(seconds: int) -> int:
    return round(time.time() / seconds)
