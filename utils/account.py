from brownie import network, accounts
from utils.secrets import get_private_key
from utils.network import is_dev


def get_account():
    if not is_dev():
        return accounts.add(get_private_key())
    else:
        return accounts[0]
