import brownie as b
from eth_utils import to_wei
from utils.account import get_account
from utils.config import (
    TERRA_RANDOM_ADDRESS,
    TERRA_WORMHOLE_CHAIN_ID,
)
from utils.encode import encode_terra_address
from utils.network import is_dev


def main():
    deployer = get_account()
    bridge = b.MockWormholeTokenBridge.deploy({"from": deployer})
