import os


class Config:

    # Main parameters
    DEBUG = bool(os.getenv("DEBUG") or False)
    TESTING = bool(os.getenv("DEBUG") or False)

    # Memcached params
    MEMCACHED_HOST = os.getenv("MEMCACHED_HOST") or "localhost"
    MEMCACHED_PORT = int(os.getenv("MEMCACHED_PORT") or 11211)

    # App params
    REQUEST_LIMITS = {
        10: 1000,
        60: 3000,
        3600: 20000
    }
