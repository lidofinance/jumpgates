from brownie import interface, Contract
from utils.env import get_env
import utils.log as log


def init_contract(address, construct):
    try:
        contract = Contract.from_explorer(address)
        log.okay(f"{address} initialized from explorer.")
    except:
        contract = construct(address)
        log.okay(f"{address} initialized from abi.")

    return contract


def init_jumpgate(address):
    return init_contract(address, interface.Jumpgate)


def init_ldo(address):
    return init_contract(address, interface.LDO)


def init_erc20(address):
    return init_contract(address, interface.ERC20)


def init_bridge(address):
    return init_contract(address, interface.IWormholeTokenBridge)


def init_rarible_nft(address):
    return init_contract(address, interface.RaribleNFT)


def init_rarible_mt(address):
    return init_contract(address, interface.RaribleMT)


def init_easytrack(address):
    return init_contract(address, interface.EasyTrack)


def init_reward_programs_registry(address):
    return init_contract(address, interface.RewardProgramsRegistry)


def init_add_reward_program_evm_script_factory(address):
    return init_contract(address, interface.AddRewardProgramEvmScriptFactory)


def init_top_up_reward_program_evm_script_factory(address):
    return init_contract(address, interface.TopUpRewardProgramEvmScriptFactory)
