from brownie import Relay
from utils.config import (
    TERRA_WORMHOLE_CHAIN_ID,
    TERRA_RANDOM_ADDRESS,
)
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


# @pytest.mark.parametrize("transfer_amount", [0, 1000, 1000000])
# def test_token_balance(relay, token, deployer, transfer_amount):
#     token.transfer(relay.address, transfer_amount, {"from": deployer})
#     assert token.balanceOf(relay.address) == transfer_amount


# def test_increment_nonce(relay, token, deployer):
#     tx = token.transfer(relay.address, 1000, {"from": deployer})
#     relay.bridgeTokens()
#     assert relay.nonce() == 1

#     tx.wait()
