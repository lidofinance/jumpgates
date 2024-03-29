import pytest
from brownie import (
    ZERO_ADDRESS,
    Jumpgate,
    Destrudo,
    accounts,
    MockERC20,
    MockERC721,
    MockERC1155,
)
from utils.amount import get_bridgeable_amount
from utils.config import (
    ADD_REWARD_PROGRAM_EVM_SCRIPT_FACTORY,
    BRIDGE_DUST_CUTOFF_DECIMALS,
    BRIDGING_CAP,
    EASYTRACK,
    LDO,
    LDO_HOLDER,
    REWARD_PROGRAMS_REGISTRY,
    SOLANA_RANDOM_ADDRESS,
    SOLANA_WORMHOLE_CHAIN_ID,
    TETHER,
    TOP_UP_REWARD_PROGRAM_EVM_SCRIPT_FACTORY,
    WORMHOLE_TOKEN_BRIDGE_ADDRESS,
)
from utils.contract import (
    init_add_reward_program_evm_script_factory,
    init_easytrack,
    init_ldo,
    init_reward_programs_registry,
    init_tether,
    init_top_up_reward_program_evm_script_factory,
)
from utils.encode import encode_solana_address


@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass


@pytest.fixture(scope="session")
def owner(accounts):
    return accounts[0]


@pytest.fixture(scope="session")
def non_owner(accounts):
    return accounts[1]


@pytest.fixture(scope="session")
def stranger(accounts):
    return accounts[2]


@pytest.fixture(scope="session")
def zero_address(accounts):
    return accounts.at(ZERO_ADDRESS, True)


# test asset recovery for actual recipient and burns
@pytest.fixture(scope="session", params=["stranger", "zero_address"])
def recipient(request):
    return request.getfixturevalue(request.param)


# test as the owner and a non-owner
@pytest.fixture(scope="session", params=["owner", "non_owner"])
def sender(request):
    return request.getfixturevalue(request.param)


@pytest.fixture(
    params=[
        (SOLANA_WORMHOLE_CHAIN_ID, SOLANA_RANDOM_ADDRESS),
    ]
)
def deploy_params(request):
    return request.param


@pytest.fixture
def zero_amount():
    return 0


@pytest.fixture
def smallest_denomination_amount():
    return 1


@pytest.fixture
def bridge_cutoff_amount(token, smallest_denomination_amount):
    if token.decimals() > BRIDGE_DUST_CUTOFF_DECIMALS:
        return 10 ** (token.decimals() - BRIDGE_DUST_CUTOFF_DECIMALS)
    return smallest_denomination_amount


@pytest.fixture
def bridge_cutoff_amount_minus_one(bridge_cutoff_amount, smallest_denomination_amount):
    return bridge_cutoff_amount - smallest_denomination_amount


@pytest.fixture
def human_denomination_amount(token):
    return 10 ** token.decimals()


@pytest.fixture
def amount_with_trailing_nonzero_decimals(
    human_denomination_amount, smallest_denomination_amount
):
    return human_denomination_amount + smallest_denomination_amount


@pytest.fixture
def max_bridging_amount(token):
    if token.decimals() > BRIDGE_DUST_CUTOFF_DECIMALS:
        return (BRIDGING_CAP - 1) * 10 ** (token.decimals() - BRIDGE_DUST_CUTOFF_DECIMALS)
    else:
        return BRIDGING_CAP - 1


@pytest.fixture
def amount_exceeding_cap(token):
    if token.decimals() > BRIDGE_DUST_CUTOFF_DECIMALS:
        return BRIDGING_CAP * 10 ** (token.decimals() - BRIDGE_DUST_CUTOFF_DECIMALS)
    else:
        return BRIDGING_CAP



@pytest.fixture(
    params=[
        "zero_amount",
        "smallest_denomination_amount",
        "bridge_cutoff_amount_minus_one",
        "bridge_cutoff_amount",
        "human_denomination_amount",
        "amount_with_trailing_nonzero_decimals",
        "amount_exceeding_cap",
        "max_bridging_amount"
    ],
)
def send_amount(request):
    return request.getfixturevalue(request.param)


# ERC20
@pytest.fixture
def token_holder():
    return accounts.add()


# ERC20 with different decimals
@pytest.fixture(params=[24, 18, 12, 6, 0])
def token(token_holder, request):
    return MockERC20.deploy(request.param, {"from": token_holder})


# ERC721
@pytest.fixture
def nft_holder(accounts):
    return accounts.add()


@pytest.fixture
def nft(nft_holder):
    return MockERC721.deploy({"from": nft_holder})


@pytest.fixture
def nft_id():
    return 0


# ERC1155
@pytest.fixture
def multitoken_holder(accounts):
    return accounts.add()


@pytest.fixture(scope="function")
def multitoken(multitoken_holder):
    return MockERC1155.deploy({"from": multitoken_holder})


@pytest.fixture
def multitoken_id():
    return 0


@pytest.fixture(scope="function")
def destrudo(owner):
    return Destrudo.deploy({"from": owner})


@pytest.fixture(scope="function")
def jumpgate(owner, token, bridge):
    return Jumpgate.deploy(
        owner.address,
        token.address,
        bridge.address,
        SOLANA_WORMHOLE_CHAIN_ID,
        encode_solana_address(SOLANA_RANDOM_ADDRESS),
        0,
        {"from": owner},
    )


# Integrated tests


@pytest.fixture
def ldo_holder(accounts, chain):
    return accounts.at(LDO_HOLDER.get(chain.id), force=True)


@pytest.fixture
def ldo(chain):
    return init_ldo(LDO.get(chain.id))


@pytest.fixture()
def ldo_jumpgate(owner, ldo, bridge):
    return Jumpgate.deploy(
        owner.address,
        ldo.address,
        bridge.address,
        SOLANA_WORMHOLE_CHAIN_ID,
        encode_solana_address(SOLANA_RANDOM_ADDRESS),
        0,
        {"from": owner},
    )


@pytest.fixture
def bridge(interface, chain):
    return interface.IWormholeTokenBridge(WORMHOLE_TOKEN_BRIDGE_ADDRESS.get(chain.id))


@pytest.fixture
def easytrack(chain):
    return init_easytrack(EASYTRACK.get(chain.id))


@pytest.fixture
def reward_programs_registry(chain):
    return init_reward_programs_registry(REWARD_PROGRAMS_REGISTRY.get(chain.id))


@pytest.fixture
def add_reward_program_evm_script_factory(chain):
    return init_add_reward_program_evm_script_factory(
        ADD_REWARD_PROGRAM_EVM_SCRIPT_FACTORY.get(chain.id)
    )


@pytest.fixture
def top_up_reward_program_evm_script_factory(chain):
    return init_top_up_reward_program_evm_script_factory(
        TOP_UP_REWARD_PROGRAM_EVM_SCRIPT_FACTORY.get(chain.id)
    )


@pytest.fixture
def tether(chain):
    return init_tether(TETHER.get(chain.id))


@pytest.fixture
def tether_holder_balance(tether):
    decimals = tether.decimals()
    return 10 ** (9 + decimals)


@pytest.fixture
def smallest_tether_amount():
    return 1


@pytest.fixture
def one_tether(tether):
    decimals = tether.decimals()
    return 10**decimals


@pytest.fixture(
    params=["smallest_tether_amount", "one_tether", "tether_holder_balance"],
)
def tether_amount(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def tether_holder(tether, accounts, tether_holder_balance):
    tether_owner_address = tether.owner()
    tether_owner = accounts.at(tether_owner_address, True)
    tether.issue(tether_holder_balance, {"from": tether_owner})
    holder = accounts.add()
    tether.transfer(holder.address, tether_holder_balance, {"from": tether_owner})
    return holder
