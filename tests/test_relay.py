from brownie import MockERC20Token, Relay
from utils.account import get_account
from utils.config import (
    ERC20_TOKEN_ADDRESS,
    WORMHOLE_TOKEN_BRIDGE_ADDRESS,
    TERRA_WORMHOLE_CHAIN_ID,
    TERRA_RANDOM_ADDRESS,
)
from utils.encode import encode_terra_address
from utils.contract import get_wormhole_token_bridge_contract
import pytest


# Relay contract
@pytest.fixture
def relay(deployer, chain):
    return Relay.deploy(
        ERC20_TOKEN_ADDRESS.get(chain.id),
        WORMHOLE_TOKEN_BRIDGE_ADDRESS.get(chain.id),
        TERRA_WORMHOLE_CHAIN_ID,
        encode_terra_address(TERRA_RANDOM_ADDRESS),
        0,
        {"from": deployer},
    )


@pytest.fixture
def bridge(chain):
    return get_wormhole_token_bridge_contract(chain.id)


# should be deployed with specified parameters
def test_relay_parameters(chain, relay):
    assert relay.token() == ERC20_TOKEN_ADDRESS.get(chain.id)
    assert relay.bridge() == WORMHOLE_TOKEN_BRIDGE_ADDRESS.get(chain.id)
    assert relay.recipientChain() == TERRA_WORMHOLE_CHAIN_ID
    assert relay.recipient() == encode_terra_address(TERRA_RANDOM_ADDRESS)
    assert relay.arbiterFee() == 0
    assert relay.nonce() == 0


@pytest.mark.parametrize("transfer_amount", [0, 1000, 1000000])
def test_token_balance(relay, token, deployer, transfer_amount):
    token.transfer(relay.address, transfer_amount, {"from": deployer})
    assert token.balanceOf(relay.address) == transfer_amount


def test_increment_nonce(relay, token, deployer):
    tx = token.transfer(relay.address, 1000, {"from": deployer})
    relay.bridgeTokens()
    assert relay.nonce() == 1

    tx.wait()
