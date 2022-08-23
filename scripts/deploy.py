from brownie import network, accounts, Jumpgate
import json
from utils.check import check_env_var
import sys

import utils.log as log
from utils.config import (
    SOLANA_WORMHOLE_CHAIN_ID,
)
from utils.encode import get_address_encoder
from ..utils.network import is_development


SUPPORTED_CHAINS = [SOLANA_WORMHOLE_CHAIN_ID]


def main():

    log.info("Checking environment variables...")

    check_env_var("WEB3_INFURA_PROJECT_ID", display=False)
    ETHERSCAN_TOKEN = check_env_var("ETHERSCAN_TOKEN", display=False)

    publish_source = not is_development() and bool(ETHERSCAN_TOKEN)

    if not publish_source:
        log.warn("Source code will not be verified on Etherscan!")

        proceed = log.prompt_yes_no("Procced?")

        if not proceed:
            log.error("Script stopped!")
            sys.exit()

    log.info("Checking deploy parameters...")

    DEPLOYER = check_env_var("DEPLOYER")

    try:
        deployer = accounts.load(DEPLOYER)
    except FileNotFoundError:
        log.error(f"Local account with id `{DEPLOYER}` not found!")
        sys.exit()

    OWNER = check_env_var("OWNER")
    TOKEN = check_env_var("TOKEN")
    BRIDGE = check_env_var("BRIDGE")
    RECIPIENT_CHAIN = int(check_env_var("RECIPIENT_CHAIN"))
    RECIPIENT = check_env_var("RECIPIENT")
    ARBITER_FEE = int(check_env_var("ARBITER_FEE"))

    log.okay("Deploy parameters are present!")

    log.info("Here is the full deploy config:")
    log.info("DEPLOYER", deployer.address)
    log.info("NETWORK", network.show_active())
    log.info("TOKEN", TOKEN)
    log.info("BRIDGE", BRIDGE)
    log.info("RECIPIENT_CHAIN", RECIPIENT_CHAIN)
    log.info("RECIPIENT", RECIPIENT)
    log.info("ARBITER_FEE", ARBITER_FEE)

    proceed = log.prompt_yes_no("Proceed?")

    if not proceed:
        log.error("Script stopped!")
        sys.exit()

    log.okay("Proceeding...")

    log.info(f"Deploying Jumpgate...")

    encode_address = get_address_encoder(RECIPIENT_CHAIN)

    owner = OWNER
    token = TOKEN
    bridge = BRIDGE
    recipientChain = RECIPIENT_CHAIN
    recipient = encode_address(RECIPIENT)
    arbiterFee = ARBITER_FEE

    jumpgate = Jumpgate.deploy(
        owner,
        token,
        bridge,
        recipientChain,
        recipient,
        arbiterFee,
        {"from": deployer},
        publish_source=publish_source,
    )

    log.okay("Jumpgate deployed successfully!")

    deployed_filename = f"./deployed/{network.show_active()}-{RECIPIENT}.json"
    with open(deployed_filename, "w") as outfile:
        json.dump(
            {
                "network": network.show_active(),
                "jumpgate": jumpgate.address,
                "owner": OWNER,
                "token": token,
                "bridge": bridge,
                "recipientChain": recipientChain,
                "recipient": RECIPIENT,
                "recipientEncoded": recipient,
                "arbiterFee": arbiterFee,
            },
            outfile,
        )

    log.okay("Deploy data dumped to", deployed_filename)
