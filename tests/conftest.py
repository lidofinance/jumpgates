import pytest
from brownie import Contract, Jumpgate, Destrudo, accounts
from utils.config import (
    ADD_REWARD_PROGRAM_EVM_SCRIPT_FACTORY,
    EASYTRACK,
    LDO_ADDRESS,
    LDO_HOLDER,
    MULTITOKEN_ID,
    NFT_ID,
    RARIBLE_MT_ADDRESS,
    RARIBLE_NFT_ADDRESS,
    REWARD_PROGRAMS_REGISTRY,
    TERRA_RANDOM_ADDRESS,
    TERRA_WORMHOLE_CHAIN_ID,
    TOP_UP_REWARD_PROGRAM_EVM_SCRIPT_FACTORY,
    VITALIK,
    WORMHOLE_TOKEN_BRIDGE_ADDRESS,
)
from utils.encode import encode_terra_address


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


# ERC20
@pytest.fixture
def token():
    return Contract.from_explorer(LDO_ADDRESS)


@pytest.fixture
def token_holder(accounts):
    return accounts.at(LDO_HOLDER, force=True)


# ERC721
@pytest.fixture(scope="function")
def nft():
    return Contract.from_explorer(RARIBLE_NFT_ADDRESS)


@pytest.fixture
def nft_id():
    return NFT_ID


@pytest.fixture(scope="function")
def nft_holder(accounts):
    return accounts.at(VITALIK, force=True)


# ERC1155
@pytest.fixture(scope="function")
def multitoken():
    return Contract.from_explorer(RARIBLE_MT_ADDRESS)


@pytest.fixture
def multitoken_id():
    return MULTITOKEN_ID


@pytest.fixture(scope="function")
def multitoken_holder(accounts):
    return accounts.at(VITALIK, force=True)


@pytest.fixture(scope="function")
def destrudo(deployer):
    return Destrudo.deploy({"from": deployer})


@pytest.fixture
def token_holder(accounts):
    return accounts.at(LDO_HOLDER, force=True)


@pytest.fixture
def bridge(interface):
    return interface.IWormholeTokenBridge(WORMHOLE_TOKEN_BRIDGE_ADDRESS)


@pytest.fixture(scope="function")
def jumpgate(deployer, token, bridge):
    return Jumpgate.deploy(
        token.address,
        bridge.address,
        TERRA_WORMHOLE_CHAIN_ID,
        encode_terra_address(TERRA_RANDOM_ADDRESS),
        0,
        {"from": deployer},
    )


@pytest.fixture
def easytrack():
    return Contract.from_explorer(EASYTRACK)


@pytest.fixture
def reward_program_registry():
    return Contract.from_explorer(REWARD_PROGRAMS_REGISTRY)


@pytest.fixture
def add_reward_program_evm_script_factory():
    return Contract.from_explorer(ADD_REWARD_PROGRAM_EVM_SCRIPT_FACTORY)


@pytest.fixture
def top_up_reward_program_evm_script_factory():
    return Contract.from_explorer(TOP_UP_REWARD_PROGRAM_EVM_SCRIPT_FACTORY)
