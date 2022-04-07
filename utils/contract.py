from brownie import network, Contract, Jumpgate
from utils.env import get_env
import utils.log as log


def init_contract(address, name="Contract", abi=None):
    log.info("Initializing contract", name)

    if get_env("ETHERSCAN_TOKEN"):
        contract = Contract.from_explorer(address)
        log.okay(f"{name} initialized from explorer.")
    else:
        contract = Contract.from_abi(name, address, abi)
        log.okay(f"{name} initialized from abi.")

    return contract


def init_jumpgate(address):
    return init_contract(address, "Jumpgate", Jumpgate.abi)
