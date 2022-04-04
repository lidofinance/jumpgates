from brownie import network, accounts, Contract
from utils.env import get_env

import utils.log as log
from utils.config import (
    SOLANA_WORMHOLE_CHAIN_ID,
    TERRA_WORMHOLE_CHAIN_ID,
)

NETWORK = get_env("NETWORK")
SUPPORTED_CHAINS = [TERRA_WORMHOLE_CHAIN_ID, SOLANA_WORMHOLE_CHAIN_ID]

# deploy essentials
WEB3_INFURA_PROJECT_ID = get_env("WEB3_INFURA_PROJECT_ID")
PRIVATE_KEY = get_env("PRIVATE_KEY")

JUMPGATE = get_env("JUMPGATE")


def main():
    if not NETWORK:
        log.error("`NETWORK` not found!")
        return

    if network.show_active() != NETWORK:
        log.error(f"Wrong network! Expected `{NETWORK}` but got", network.show_active())
        return

    if not JUMPGATE:
        log.error("`JUMPGATE` not found!")
        return

    if not WEB3_INFURA_PROJECT_ID:
        log.error("`WEB3_INFURA_PROJECT_ID` not found!")
        return

    if not PRIVATE_KEY:
        log.error("`PRIVATE_KEY` not found!")
        return

    log.okay("All enviroment variables present!")

    sender = accounts.add(PRIVATE_KEY)
    log.info("sender", sender.address)
    log.info("Jumpgate", JUMPGATE)

    proceed = log.prompt_yes_no("Procced?")
    if not proceed:
        log.error("Script stopped!")
        return

    log.info("Calling `bridgeTokens` on", JUMPGATE)
    jumpgate = Contract.from_explorer(JUMPGATE)
    jumpgate.bridgeTokens({"from": sender})
    log.info("Transaction successful")
