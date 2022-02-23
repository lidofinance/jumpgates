import pytest


@pytest.mark.parametrize("supply", [0, 1000, 1000000])
def test_token_deploy(Token, accounts, supply):
    token = Token.deploy(supply, {"from": accounts[0]})
    assert token.balanceOf(accounts[0]) == supply


def test_token_name(Token, accounts):
    token = Token.deploy(1000, {"from": accounts[0]})
    assert token.name() == "Token"


def test_token_symbol(Token, accounts):
    token = Token.deploy(1000, {"from": accounts[0]})
    assert token.symbol() == "TKN"


def test_token_transfer(Token, accounts):
    token = Token.deploy(1000, {"from": accounts[0]})
    token.transfer(accounts[1].address, 200)

    assert token.balanceOf(accounts[0]) == 800
    assert token.balanceOf(accounts[1]) == 200
