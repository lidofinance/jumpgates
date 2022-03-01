from brownie import MockERC20, Relay, network
from utils.config import (
    ldo,
    wormhole_token_bridge,
    TERRA_WORMHOLE_CHAIN_ID,
    TERRA_RANDOM_ADDRESS,
)
from utils.encode import encode_terra_address
from utils.contract import get_ldo_contract, get_wormhole_token_bridge_contract
import pytest


# Relay contract
@pytest.fixture
def relay(accounts, chain):
    return Relay.deploy(
        ldo.get(chain.id),
        wormhole_token_bridge.get(chain.id),
        TERRA_WORMHOLE_CHAIN_ID,
        encode_terra_address(TERRA_RANDOM_ADDRESS),
        0,
        {"from": accounts[0]},
    )


# some ERC20 token, e.g. LDO
@pytest.fixture
def token(accounts):
    return MockERC20.deploy(10**9, {"from": accounts[0]})


@pytest.fixture
def bridge(chain, accounts):
    return get_wormhole_token_bridge_contract(chain.id)


# should be deployed with specified parameters
def test_relay_parameters(accounts, chain, relay):
    assert relay.token() == ldo.get(chain.id)
    assert relay.bridge() == wormhole_token_bridge.get(chain.id)
    assert relay.recipientChain() == TERRA_WORMHOLE_CHAIN_ID
    assert relay.recipient() == encode_terra_address(TERRA_RANDOM_ADDRESS)
    assert relay.arbiterFee() == 0
    assert relay.nonce() == 0


@pytest.mark.parametrize("transfer_amount", [0, 1000, 1000000])
def test_token_balance(relay, token, chain, accounts, transfer_amount):
    token.transfer(relay.address, transfer_amount, {"from": accounts[0]})
    assert token.balanceOf(relay.address) == transfer_amount


def test_bridge_transfer_tokens(token, bridge, accounts):
    bridge.transferTokens(
        token.address,
        1000,
        TERRA_WORMHOLE_CHAIN_ID,
        encode_terra_address(TERRA_RANDOM_ADDRESS),
        0,
        0,
        {"from": accounts[0]},
    )
    assert token.balanceOf(accounts[0]) == 10**9 - 1000


def test_increment_nonce(relay, token, bridge, accounts):
    token.transfer(relay.address, 1000, {"from": accounts[0]})
    relay.bridgeTokens()
    assert relay.nonce() == 1
