from brownie import Token, accounts


def main():
    Token.deploy(1000, {"from": accounts[0]})
