from brownie import MockERC20Token, Contract, network
from utils.config import WORMHOLE_TOKEN_BRIDGE_ADDRESS, ERC20_TOKEN_ADDRESS
import json
from eth_utils import from_wei, to_wei
import utils.log as log
from utils.account import get_account
from utils.network import is_dev


def get_wormhole_token_bridge_contract(chain_id):
    with open("abis/wormhole_token_bridge.json") as abi_json:
        abi = json.loads(abi_json.read())

    return Contract.from_abi(
        "Wormhole: Token Bridge", WORMHOLE_TOKEN_BRIDGE_ADDRESS.get(chain_id), abi
    )


def get_erc20_token_contract(chain_id, owner):
    return Contract.from_explorer(ERC20_TOKEN_ADDRESS.get(chain_id), owner=owner)


def deploy_mock_erc20_token():
    log.info("Checking network...")
    if network.show_active() == "mainnet":
        log.error("Shouldn't deploy a mock ERC20 token on mainnet. Aborting...")

    log.okay(f"Network is {network.show_active()}. Proceeding...")

    deployer = get_account()

    log.info("Deployer balance", from_wei(deployer.balance(), "ether"))

    dev = is_dev()
    one_billion = to_wei(10**9, "ether")
    log.info("Deploying MockERC20Token...")

    mock_erc20_token = MockERC20Token.deploy(
        one_billion, {"from": deployer}, publish_source=not dev
    )

    log.okay("Deploy complete!")

    log.info(
        "Deployer MockERC20Token balance",
        from_wei(mock_erc20_token.balanceOf(deployer.address), "ether"),
    )
