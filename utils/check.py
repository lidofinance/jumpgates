from .env import get_env
import utils.log as log
import sys


def check_env_var(variable, display=True):
    log.info(f"Checking `{variable}`...")

    value = get_env(variable)

    if value:
        log.okay(variable, value if display else mask(value))
        proceed = log.prompt_yes_no("Proceed?")

        if not proceed:
            log.error("Script stopped manually!")
            sys.exit()
    else:
        log.error(f"`{variable}` not found!")

        proceed = log.prompt_yes_no("Proceed?")
        if not proceed:
            log.error("Script stopped manually!")
            sys.exit()

    return value


def mask(text):
    return len(text[:-4]) * "#" + text[-4:]
