from brownie import network, accounts, Jumpgate
import json

import utils.log as log
from utils.config import TERRA_RANDOM_ADDRESS, TERRA_WORMHOLE_CHAIN_ID
from utils.encode import encode_terra_address
from utils.secrets import get_private_key

ROPSTEN_ID = 3

# deploy parameters
ROPSTEN_MOCK_ERC20 = "0x9D6735b53D357626DD892F186411dd3fC58b4f02"
ROPSTEN_WORMHOLE_TOKEN_BRIDGE = "0xf174f9a837536c449321df1ca093bb96948d5386"


def main():
    if network.show_active() != "ropsten":
        log.error("Wrong network! Expected ropsten but got", network.show_active())
        return

    private_key = get_private_key()
    if not private_key:
        log.error("No private key found! Please specify `PRIVATE_KEY` in env")
        return

    deployer = accounts.add(private_key)
    log.info("Deployer address", deployer.address)

    log.info("Deploying Jumpgate to Ropsten")

    token = ROPSTEN_MOCK_ERC20
    bridge = ROPSTEN_WORMHOLE_TOKEN_BRIDGE
    recipientChain = TERRA_WORMHOLE_CHAIN_ID
    recipient = encode_terra_address(TERRA_RANDOM_ADDRESS)
    arbiterFee = 0

    Jumpgate.deploy(
        token,
        bridge,
        recipientChain,
        recipient,
        arbiterFee,
        {"from": deployer},
        publish_source=True,
    )

    log.info("Jumpgate deployed successfully")

    with open(f"deployed-{network.show_active()}.json", "w") as outfile:
        json.dump(
            {
                "token": token,
                "bridge": bridge,
                "recipientChain": recipientChain,
                "recipient": TERRA_RANDOM_ADDRESS,
                "arbiterFee": 0,
            },
            outfile,
        )
