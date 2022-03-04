from eth_utils import to_wei
import pytest
from brownie import MockERC20Token
from utils.account import get_account


@pytest.fixture(scope="session")
def deployer():
    return get_account()


@pytest.fixture
def token(deployer):
    return MockERC20Token.deploy(to_wei(10**9, "ether"), {"from": deployer})
