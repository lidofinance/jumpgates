from brownie import Relay, network

from utils.config import (
    ERC20_TOKEN_ADDRESS,
    TERRA_RANDOM_ADDRESS,
    TERRA_WORMHOLE_CHAIN_ID,
    WORMHOLE_TOKEN_BRIDGE_ADDRESS,
)

# from utils.encode import encode_terra_address
from utils.account import get_account
from utils.encode import encode_terra_address
import utils.log as log
from utils.network import is_dev


def main():
    chain_id = network.chain.id
    log.info("Network and chain id", (network.show_active(), chain_id))

    deployer = get_account()
    log.info("Deployer", deployer.address)

    token_address = ERC20_TOKEN_ADDRESS.get(chain_id)
    log.info("Token", token_address)

    bridge_address = WORMHOLE_TOKEN_BRIDGE_ADDRESS.get(chain_id)
    recipient = encode_terra_address(TERRA_RANDOM_ADDRESS)
    arbiter_fee = 0

    Relay.deploy(
        token_address,
        bridge_address,
        TERRA_WORMHOLE_CHAIN_ID,
        recipient,
        arbiter_fee,
        {"from": deployer},
        publish_source=not is_dev(),
    )
