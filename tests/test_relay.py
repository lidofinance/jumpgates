from brownie import Relay
from eth_utils import to_wei
from utils.config import (
    TERRA_WORMHOLE_CHAIN_ID,
    TERRA_RANDOM_ADDRESS,
)
from utils.constants import one_ether
from utils.encode import encode_terra_address
import pytest


# Relay contract
@pytest.fixture(scope="function")
def relay(deployer, token, bridge):
    return Relay.deploy(
        token.address,
        bridge.address,
        TERRA_WORMHOLE_CHAIN_ID,
        encode_terra_address(TERRA_RANDOM_ADDRESS),
        0,
        {"from": deployer},
    )


# should be deployed with specified parameters
def test_relay_parameters(relay, token, bridge):
    assert relay.token() == token.address
    assert relay.bridge() == bridge.address
    assert relay.recipientChain() == TERRA_WORMHOLE_CHAIN_ID
    assert relay.recipient() == encode_terra_address(TERRA_RANDOM_ADDRESS)
    assert relay.arbiterFee() == 0
    assert relay.nonce() == 0


def test_recover_eth(relay, selfdestructable, stranger, another_stranger):
    # top up relay balance by self-destructing another contract
    prev_relay_balance = relay.balance()
    selfdestructable.destroy(relay.address, {"value": one_ether, "from": stranger})
    assert relay.balance() == prev_relay_balance + one_ether

    # recover ETH; using a different recipient to avoid gas calculations
    prev_relay_balance = relay.balance()
    prev_recipient_balance = another_stranger.balance()
    relay.recoverETH(another_stranger.address)
    assert another_stranger.balance() == prev_recipient_balance + prev_relay_balance


# @pytest.mark.parametrize("transfer_amount", [0, 1000, 1000000])
# def test_token_balance(relay, token, deployer, transfer_amount):
#     token.transfer(relay.address, transfer_amount, {"from": deployer})
#     assert token.balanceOf(relay.address) == transfer_amount


# def test_increment_nonce(relay, token, deployer):
#     tx = token.transfer(relay.address, 1000, {"from": deployer})
#     relay.bridgeTokens()
#     assert relay.nonce() == 1

#     tx.wait()
