import datetime
import time


def logtime(func):
    """Measure how long does it take for a function to run """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)

        total_time = time.time() - start_time
        print(f'Time Elapsed {str(datetime.timedelta(seconds=total_time)).split(".")[0]}')
        return result

    return wrapper


def printfun(func):
    """Print function return"""

    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(result)
        return result

    return wrapper
