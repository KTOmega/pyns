import config
import json
import threading

_contents = {}
_lock = threading.Lock()

def init():
    global _contents
    _lock.acquire()
    
    with open(config.db, "r") as db_fd:
        _contents = json.load(db_fd)

    _lock.release()

def has(name):
    _lock.acquire()
    res = name in _contents
    _lock.release()

    return res

def get(name):
    _lock.acquire()
    res = _contents[name]
    _lock.release()
    
    return res

def set(name, value):
    _lock.acquire()

    _contents[name] = value

    with open(config.db, "w") as db_fd:
        json.dump(_contents, db_fd)

    _lock.release()

def get_all():
    _lock.acquire()

    res = _contents.copy()

    _lock.release()

    return res
