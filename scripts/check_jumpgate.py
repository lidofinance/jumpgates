from brownie import network
import sys

from utils.check import check_deploy_param, check_env_var
from utils.contract import (
    init_add_reward_program_evm_script_factory,
    init_bridge,
    init_easytrack,
    init_erc20,
    init_jumpgate,
    init_reward_programs_registry,
    init_top_up_reward_program_evm_script_factory,
)
import utils.log as log
from utils.config import (
    ADD_REWARD_PROGRAM_EVM_SCRIPT_FACTORY,
    EASYTRACK,
    REWARD_PROGRAMS_REGISTRY,
    SOLANA_WORMHOLE_CHAIN_ID,
    TOP_UP_REWARD_PROGRAM_EVM_SCRIPT_FACTORY,
)
from utils.encode import get_address_encoder
from utils.simulate import simulate_full_flow

SUPPORTED_CHAINS = [SOLANA_WORMHOLE_CHAIN_ID]


def main():

    log.info("Checking environment variables...")

    check_env_var("WEB3_INFURA_PROJECT_ID", display=False, prompt=False)

    log.info("Checking jumpgate...")

    JUMPGATE = check_env_var("JUMPGATE", prompt=False)
    OWNER = check_env_var("OWNER", prompt=False)
    TOKEN = check_env_var("TOKEN", prompt=False)
    BRIDGE = check_env_var("BRIDGE", prompt=False)
    RECIPIENT_CHAIN = int(check_env_var("RECIPIENT_CHAIN", prompt=False))
    RECIPIENT = check_env_var("RECIPIENT", prompt=False)
    ARBITER_FEE = int(check_env_var("ARBITER_FEE", prompt=False))

    encode_address = get_address_encoder(RECIPIENT_CHAIN)

    jumpgate = init_jumpgate(JUMPGATE)

    check_deploy_param("OWNER", OWNER, jumpgate.owner())
    check_deploy_param("TOKEN", TOKEN, jumpgate.token())
    check_deploy_param("BRIDGE", BRIDGE, jumpgate.bridge())
    check_deploy_param("RECIPIENT_CHAIN", RECIPIENT_CHAIN, jumpgate.recipientChain())
    check_deploy_param("RECIPIENT", encode_address(RECIPIENT), jumpgate.recipient())
    check_deploy_param("ARBITER_FEE", ARBITER_FEE, jumpgate.arbiterFee())

    log.okay("Deploy parameters are correct!")

    if "fork" not in network.show_active():
        log.warn("Active network is not a fork, stopping the script.")
        sys.exit()

    log.info("Simulating jumpgate flow with easy track...")

    token = init_erc20(TOKEN)
    easytrack = init_easytrack(EASYTRACK.get(network.chain.id))
    bridge = init_bridge(BRIDGE)
    reward_programs_registry = init_reward_programs_registry(
        REWARD_PROGRAMS_REGISTRY.get(network.chain.id)
    )
    add_reward_program_evm_script_factory = init_add_reward_program_evm_script_factory(
        ADD_REWARD_PROGRAM_EVM_SCRIPT_FACTORY.get(network.chain.id)
    )
    top_up_reward_program_evm_script_factory = (
        init_top_up_reward_program_evm_script_factory(
            TOP_UP_REWARD_PROGRAM_EVM_SCRIPT_FACTORY.get(network.chain.id)
        )
    )

    simulate_full_flow(
        token,
        jumpgate,
        easytrack,
        bridge,
        reward_programs_registry,
        add_reward_program_evm_script_factory,
        top_up_reward_program_evm_script_factory,
        OWNER,
        0,
    )

    log.okay("Full flow simulated successfully!")
