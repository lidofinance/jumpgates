import json
from eth_utils import to_wei
import pytest
from brownie import Contract
from utils.config import LDO_ADDRESS, LDO_HOLDER, WORMHOLE_TOKEN_BRIDGE_ADDRESS
from utils.network import is_development


@pytest.fixture(scope="session")
def deployer(accounts):
    return accounts[0]


@pytest.fixture
def token():
    return Contract.from_explorer(LDO_ADDRESS)


@pytest.fixture
def token_holder(accounts):
    return accounts.at(LDO_HOLDER, force=True)


@pytest.fixture
def bridge():
    with open("abis/wormhole_token_bridge.json") as file:
        abi = json.loads(file.read())
    return Contract.from_abi(
        "Wormhole: Token Bridge", WORMHOLE_TOKEN_BRIDGE_ADDRESS, abi
    )
