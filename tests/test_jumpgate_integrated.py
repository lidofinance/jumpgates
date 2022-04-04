def test_full_flow(
    deployer, accounts, jumpgate, reward_program_registry, evm_script_executor
):
    trusted_caller = accounts.at("0x87d93d9b2c672bf9c9642d853a8682546a5012b5", True)
    tx = reward_program_registry.addRewardProgram(
        jumpgate.address, "Jumpgate Recipient #1", {"from": trusted_caller}
    )

    assert jumpgate.address in reward_program_registry.getRewardPrograms()
