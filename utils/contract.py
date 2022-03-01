from brownie import Contract
from utils.config import wormhole_token_bridge, ldo
import json


def get_wormhole_token_bridge_contract(chain_id):
    with open("abis/wormhole_token_bridge.json") as abi_json:
        abi = json.loads(abi_json.read())

    return Contract.from_abi(
        "Wormhole: Token Bridge", wormhole_token_bridge.get(chain_id), abi
    )


def get_ldo_contract(chain_id, owner):
    return Contract.from_explorer(ldo.get(chain_id), owner=owner)
