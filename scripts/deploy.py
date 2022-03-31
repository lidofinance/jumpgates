from brownie import network, accounts, Jumpgate
import json

import utils.log as log
from utils.config import (
    SOLANA_WORMHOLE_CHAIN_ID,
    TERRA_RANDOM_ADDRESS,
    TERRA_WORMHOLE_CHAIN_ID,
)
from utils.encode import encode_terra_address
from utils.secrets import get_env

NETWORK = get_env("NETWORK")

# deploy essentials
WEB3_INFURA_PROJECT_ID = get_env("WEB3_INFURA_PROJECT_ID")
PRIVATE_KEY = get_env("PRIVATE_KEY")

# deploy parameters
TOKEN = get_env("TOKEN")
BRIDGE = get_env("BRIDGE")
RECIPIENT_CHAIN = int(get_env("RECIPIENT_CHAIN"))
RECIPIENT = get_env("RECIPIENT")
ARBITER_FEE = get_env("ARBITER_FEE") or 0

SUPPORTED_CHAINS = [TERRA_WORMHOLE_CHAIN_ID, SOLANA_WORMHOLE_CHAIN_ID]


def main():
    if not NETWORK:
        log.error("`NETWORK` not found!")
        return

    if network.show_active() != NETWORK:
        log.error(f"Wrong network! Expected `{NETWORK}` but got", network.show_active())
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

    log.info("NETWORK", NETWORK)
    log.info("Deployer", deployer.address)
    log.info("TOKEN", TOKEN)
    log.info("BRIDGE", BRIDGE)
    log.info("RECIPIENT_CHAIN", RECIPIENT_CHAIN)
    log.info("RECIPIENT", RECIPIENT)
    log.info("ARBITER_FEE", ARBITER_FEE)

    proceed = log.prompt_yes_no("Proceed?")

    if not proceed:
        log.error("Script stopped!")
        return

    log.okay("Proceeding...")

    # log.info("Deploying Jumpgate to Ropsten")

    # token = ROPSTEN_MOCK_ERC20
    # bridge = ROPSTEN_WORMHOLE_TOKEN_BRIDGE
    # recipientChain = TERRA_WORMHOLE_CHAIN_ID
    # recipient = encode_terra_address(TERRA_RANDOM_ADDRESS)
    # arbiterFee = 0

    # Jumpgate.deploy(
    #     token,
    #     bridge,
    #     recipientChain,
    #     recipient,
    #     arbiterFee,
    #     {"from": deployer},
    #     publish_source=True,
    # )

    # log.info("Jumpgate deployed successfully")

    # with open(f"deployed-{network.show_active()}.json", "w") as outfile:
    #     json.dump(
    #         {
    #             "token": token,
    #             "bridge": bridge,
    #             "recipientChain": recipientChain,
    #             "recipient": TERRA_RANDOM_ADDRESS,
    #             "arbiterFee": 0,
    #         },
    #         outfile,
    #     )
