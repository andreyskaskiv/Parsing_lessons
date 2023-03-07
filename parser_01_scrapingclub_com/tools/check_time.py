import time
from datetime import datetime


def check_time_sek(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        dtime = end - start
        print(f"Time game: {round(dtime, 3)} sek")
        return result

    return wrapper


def check_time(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        dtime = end - start
        print(f"Time game: {dtime}")
        return result

    return wrapper
