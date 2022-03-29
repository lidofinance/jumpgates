import json
import pytest
from brownie import Contract, Destrudo
from utils.config import (
    LDO_ADDRESS,
    LDO_HOLDER,
    NFT_ID,
    RARIBLE_ADDRESS,
    VITALIK,
    WORMHOLE_TOKEN_BRIDGE_ADDRESS,
)
from utils.network import is_development


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@pytest.fixture(scope="session")
def deployer(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def stranger(accounts):
    return accounts[1]


@pytest.fixture(scope="session")
def another_stranger(accounts):
    return accounts[2]


@pytest.fixture
def token():
    return Contract.from_explorer(LDO_ADDRESS)


@pytest.fixture
def token_holder(accounts):
    return accounts.at(LDO_HOLDER, force=True)


@pytest.fixture(scope="function")
def nft():
    return Contract.from_explorer(RARIBLE_ADDRESS)


@pytest.fixture
def nft_id():
    return NFT_ID


@pytest.fixture(scope="function")
def nft_holder(accounts):
    return accounts.at(VITALIK, force=True)


@pytest.fixture(scope="function")
def destrudo(deployer):
    return Destrudo.deploy({"from": deployer})


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
