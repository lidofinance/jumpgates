from brownie import network, accounts, Contract
import json

import utils.log as log
from utils.config import (
    SOLANA_WORMHOLE_CHAIN_ID,
    TERRA_WORMHOLE_CHAIN_ID,
)
from utils.encode import encode_terra_address, get_address_encoder
from utils.secrets import get_env

NETWORK = get_env("NETWORK")

# deploy essentials
WEB3_INFURA_PROJECT_ID = get_env("WEB3_INFURA_PROJECT_ID")
PRIVATE_KEY = get_env("PRIVATE_KEY")

# deploy parameters
JUMPGATE = get_env("JUMPGATE")
TOKEN = get_env("TOKEN")
BRIDGE = get_env("BRIDGE")
RECIPIENT_CHAIN = int(get_env("RECIPIENT_CHAIN"))
RECIPIENT = get_env("RECIPIENT")
ARBITER_FEE = get_env("ARBITER_FEE")

SUPPORTED_CHAINS = [TERRA_WORMHOLE_CHAIN_ID, SOLANA_WORMHOLE_CHAIN_ID]


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

    if not TOKEN:
        log.error("`TOKEN` not found!")
        return

    if not BRIDGE:
        log.error("`BRIDGE` not found!")
        return

    if not RECIPIENT_CHAIN:
        log.error("`RECIPIENT_CHAIN` not found!")
        return

    if RECIPIENT_CHAIN not in SUPPORTED_CHAINS:
        log.error("`RECIPIENT_CHAIN` not supported!")
        return

    if not RECIPIENT:
        log.error("`RECIPIENT` not found!")
        return

    deployer = accounts.add(PRIVATE_KEY)

    log.okay("All environment variables are present!")

    log.info("Checking deploy parameters")

    jumpgate = Contract.from_explorer(JUMPGATE)

    encode_address = get_address_encoder(RECIPIENT_CHAIN)

    assert jumpgate.token() == TOKEN
    log.okay("Token matches", TOKEN)

    assert jumpgate.bridge() == BRIDGE
    log.okay("Bridge matches", BRIDGE)

    assert jumpgate.recipientChain() == RECIPIENT_CHAIN
    log.okay("Recipient chain matches", RECIPIENT_CHAIN)

    assert jumpgate.recipient() == encode_address(RECIPIENT)
    log.okay("Recipient matches", RECIPIENT)

    assert jumpgate.arbiterFee() == ARBITER_FEE
    log.okay("Arbiter fee matches", ARBITER_FEE)

    log.okay("Deploy parameters are correct!")
