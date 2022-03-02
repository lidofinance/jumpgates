from eth_utils import from_wei, to_wei
import utils.log as log
from utils.account import get_account
from brownie import network, MockERC20Token
from utils.network import is_dev


def main():
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
