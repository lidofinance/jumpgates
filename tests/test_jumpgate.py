from brownie import Jumpgate, reverts
from eth_utils import to_wei
from utils.config import (
    TERRA_WORMHOLE_CHAIN_ID,
    TERRA_RANDOM_ADDRESS,
)
from utils.constants import one_ether
from utils.encode import encode_terra_address
import pytest


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


def test_deploy_parameters(jumpgate, token, bridge):
    assert jumpgate.token() == token.address
    assert jumpgate.bridge() == bridge.address
    assert jumpgate.recipientChain() == TERRA_WORMHOLE_CHAIN_ID
    assert jumpgate.recipient() == encode_terra_address(TERRA_RANDOM_ADDRESS)
    assert jumpgate.arbiterFee() == 0


def test_auth_recover_ether(jumpgate, selfdestructable, stranger, another_stranger):
    # top up jumpgate balance by self-destructing another contract
    prev_jumpgate_balance = jumpgate.balance()
    selfdestructable.destroy(jumpgate.address, {"value": one_ether, "from": stranger})
    assert jumpgate.balance() == prev_jumpgate_balance + one_ether

    # recover ETH as the owner
    recipient = another_stranger
    prev_jumpgate_balance = jumpgate.balance()
    prev_recipient_balance = recipient.balance()
    jumpgate.recoverEther(recipient.address)
    assert recipient.balance() == prev_recipient_balance + prev_jumpgate_balance


def test_unauth_recover_ether(jumpgate, selfdestructable, stranger, another_stranger):
    # top up jumpgate balance by self-destructing another contract
    prev_jumpgate_balance = jumpgate.balance()
    selfdestructable.destroy(jumpgate.address, {"value": one_ether, "from": stranger})
    assert jumpgate.balance() == prev_jumpgate_balance + one_ether

    # try to recover ETH as a non-owner
    with reverts("Ownable: caller is not the owner"):
        jumpgate.recoverEther(another_stranger.address, {"from": another_stranger})


def test_recover_tokens(token, jumpgate, token_holder):
    # send tokens to jumpgate
    token_holder_tokens = token.balanceOf(token_holder.address)
    jumpgate_tokens = token.balanceOf(jumpgate.address)
    token.transfer(jumpgate.address, one_ether, {"from": token_holder})
    assert token.balanceOf(token_holder.address) == token_holder_tokens - one_ether
    assert token.balanceOf(jumpgate.address) == jumpgate_tokens + one_ether

    # recover tokens
    token_holder_tokens = token.balanceOf(token_holder.address)
    jumpgate_tokens = token.balanceOf(jumpgate.address)
    jumpgate.recoverERC20(token.address, token_holder.address)
    assert (
        token.balanceOf(token_holder.address) == token_holder_tokens + jumpgate_tokens
    )
    assert token.balanceOf(jumpgate.address) == 0
