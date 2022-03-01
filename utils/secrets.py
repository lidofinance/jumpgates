import os


def get_env(name):
    return os.getenv(name)


def get_private_key():
    return get_env("PRIVATE_KEY")
