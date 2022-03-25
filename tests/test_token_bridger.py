from brownie import TokenBridger, reverts
from eth_utils import to_wei
from utils.config import (
    TERRA_WORMHOLE_CHAIN_ID,
    TERRA_RANDOM_ADDRESS,
)
from utils.constants import one_ether
from utils.encode import encode_terra_address
import pytest


@pytest.fixture(scope="function")
def token_bridger(deployer, token, bridge):
    return TokenBridger.deploy(
        token.address,
        bridge.address,
        TERRA_WORMHOLE_CHAIN_ID,
        encode_terra_address(TERRA_RANDOM_ADDRESS),
        0,
        {"from": deployer},
    )


def test_deploy_parameters(token_bridger, token, bridge):
    assert token_bridger.token() == token.address
    assert token_bridger.bridge() == bridge.address
    assert token_bridger.recipientChain() == TERRA_WORMHOLE_CHAIN_ID
    assert token_bridger.recipient() == encode_terra_address(TERRA_RANDOM_ADDRESS)
    assert token_bridger.arbiterFee() == 0


def test_auth_recover_ether(
    token_bridger, selfdestructable, stranger, another_stranger
):
    # top up token_bridger balance by self-destructing another contract
    prev_token_bridger_balance = token_bridger.balance()
    selfdestructable.destroy(
        token_bridger.address, {"value": one_ether, "from": stranger}
    )
    assert token_bridger.balance() == prev_token_bridger_balance + one_ether

    # recover ETH as the owner
    recipient = another_stranger
    prev_token_bridger_balance = token_bridger.balance()
    prev_recipient_balance = recipient.balance()
    token_bridger.recoverEther(recipient.address)
    assert recipient.balance() == prev_recipient_balance + prev_token_bridger_balance


def test_unauth_recover_ether(
    token_bridger, selfdestructable, stranger, another_stranger
):
    # top up token_bridger balance by self-destructing another contract
    prev_token_bridger_balance = token_bridger.balance()
    selfdestructable.destroy(
        token_bridger.address, {"value": one_ether, "from": stranger}
    )
    assert token_bridger.balance() == prev_token_bridger_balance + one_ether

    # try to recover ETH as a non-owner
    with reverts("Ownable: caller is not the owner"):
        token_bridger.recoverEther(another_stranger.address, {"from": another_stranger})


def test_recover_tokens(token, token_bridger, token_holder):
    # send tokens to token_bridger
    token_holder_tokens = token.balanceOf(token_holder.address)
    token_bridger_tokens = token.balanceOf(token_bridger.address)
    token.transfer(token_bridger.address, one_ether, {"from": token_holder})
    assert token.balanceOf(token_holder.address) == token_holder_tokens - one_ether
    assert token.balanceOf(token_bridger.address) == token_bridger_tokens + one_ether

    # recover tokens
    token_holder_tokens = token.balanceOf(token_holder.address)
    token_bridger_tokens = token.balanceOf(token_bridger.address)
    token_bridger.recoverERC20(token.address, token_holder.address)
    assert (
        token.balanceOf(token_holder.address)
        == token_holder_tokens + token_bridger_tokens
    )
    assert token.balanceOf(token_bridger.address) == 0
