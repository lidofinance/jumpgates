from .env import get_env
import utils.log as log
import sys


def check_env_var(variable, display=True, prompt=True):
    log.info(f"Checking `{variable}`...")

    value = get_env(variable)

    if value:
        log.okay(variable, value if display else mask(value))
        if prompt:
            proceed = log.prompt_yes_no("Proceed?")

            if not proceed:
                log.error("Script stopped manually!")
                sys.exit()
    else:
        log.error(f"`{variable}` not found!")

        if prompt:
            proceed = log.prompt_yes_no("Proceed?")

            if not proceed:
                log.error("Script stopped manually!")
                sys.exit()

    return value


def mask(text):
    return len(text[:-4]) * "#" + text[-4:]


def check_deploy_param(variable, env_value, onchain_value):
    log.info(f"Checking {variable}...")
    log.info("ENV____", env_value)
    log.info("ONCHAIN", onchain_value)
    assert env_value == onchain_value
    log.okay(f"{variable} matches!")