<div style="display: flex;" align="center">
  <h1 align="center">Jumpgates</h1>
  <img src="https://raw.githubusercontent.com/lidofinance/jumpgates/main/img/logo.png" width="100" align="left" />
</div>

![solidity 0.8.§3](https://img.shields.io/badge/solidity-0.8.13-lightgray)
![python ~3.8.9](https://img.shields.io/badge/python-~3.8.9-blue)
![eth_brownie ^1.19.0](https://img.shields.io/badge/eth__brownie-^1.19.0-brown)
![license GPL](https://img.shields.io/badge/license-GPL-green)

Jumpgates facilitate cross-chain token transfers under the Lido DAO incentive programs. Although autonomous, jumpgates are meant to be part of the Easy Track Rewards Program pipeline.

## 🌀 About jumpgates

A jumpgate is a simple contract that transfers tokens via a cross-chain token bridge, such as Wormhole, Terra Shuttle, etc. The parameters of the transportation (the token, recipient, bridge) are predefined and immutable for each invididual jumpgate which makes its operation safe and permissionless. Jumpgates also provide permissioned ways to recover ether, ERC20, ERC721 and ERC1155 tokens.

As Ethereum-native Lido expands to other blockchains, jumpgates reduce operational overhead associated with routine cross-chain token transfers under the Lido DAO by providing a permissionless way to bridge tokens.

For further details [read ADR](https://hackmd.io/snwPWGqBS-ax5Ur0A5Ix5w?view).

## 🏁 Getting started

This project uses Brownie development framework. Learn more about [Brownie](https://eth-brownie.readthedocs.io/en/stable/index.html).

### Prerequisites

- Python 3.8+
- Poetry 1.1.13

#### Step 1. Install Python dependencies.
Install project dependendencies from the lockfile,

```bash
$ poetry install
```

#### Step 2. Activate venv.
Activate Poetry virtual environment,

```bash
$ poetry shell
```

Learn more about [Poetry](https://python-poetry.org/docs/).


#### Step 3. Specify your Infura project id.

Replace `%YOUR-INFURA-PROJECT-ID%` below with your actual project id. Learn more about [Infura](https://infura.io/).

```bash
$ export WEB3_INFURA_PROJECT_ID=%YOUR-INFURA-PROJECT-ID%
```

#### Step 4 (recommended). Specify your Etherscan API key.

Replace `%YOUR-ETHERSCAN-TOKEN%` below with your actual API key. Learn more about [Etherscan API](https://etherscan.io/apis).

```bash
$ export ETHERSCAN_TOKEN=%YOUR-ETHERSCAN-TOKEN%
```

#### Step 5 (optional). Add a Goerli development fork.

The project uses the `mainnet-fork` network by default. If you want to check your jumpgate deploys or run the test suite on Goerli, you can add `goerli-fork` by running the following command,

```bash
$ brownie networks add "Development" goerli-fork host=http://127.0.0.1 cmd=ganache-cli port=8545 gas_limit=12000000 fork=https://goerli.infura.io/v3/${WEB3_INFURA_PROJECT_ID} chain_id=5 mnemonic=brownie accounts=10 fork=goerli
```

## 🧪 Testing a jumpgate

Before you proceed, please follow [Getting Started](#-getting-started) instructions.

To run the entire test suite, execute the following command,

```bash
$ brownie test
```
Alternatively, you can run a specific test module by specifying the path,

```bash
$ brownie test tests/test_jumpgate_unit.py
```

Note! This project uses `mainnet-fork` by default.

Learn more about Brownie [tests](https://eth-brownie.readthedocs.io/en/stable/tests-pytest-intro.html).

## 🚛 Deploying a jumpgate

Before you proceed, please follow [Getting Started](#-getting-started) instructions.

#### Step 1. Add a local account.

You can add a local account either from a private key or a keystore. If you do not have either of them, consider generating a new account. Learn more about Brownie [local accounts](https://eth-brownie.readthedocs.io/en/v1.6.4/accounts.html#managing-local-accounts).

#### Step 2. Specify environment variables.

You can do this by copying the contents of `sample.env` into `.env` and filling it out. The necessary variables are listed below,

- `DEPLOYER` - your local account id;
- `NETWORK` - name of the network you want to deploy a jumpgate to, e.g., `mainnet`, `goerli`, `ropsten`, etc.;
- `TOKEN` - address of the ERC20 token you want to transfer;
- `BRIDGE` - address of the Wormhole Token Bridge;
- `RECIPIENT_CHAIN` - Wormhole id of the target chain, e.g. `1` for Solana, `3` for Terra;
- `RECIPIENT` - address of the recipient;
- `ARBITER_FEE` - bridge arbiter fee, defaults to 0.

#### Step 3. Run the deploy script.

```bash
$ brownie run scripts/deploy.py
```

Upon running the script you will prompted to enter the password to your local account. After that, all the deploy parameters will be displayed in your terminal. Confirm them and enter 'y' to proceed. E.g.,

<img alt="image" src="https://user-images.githubusercontent.com/39704351/161904797-9a0484a0-8c86-45bf-a842-ea04e0ca49f6.png">

If all is correct, you should be able to see your transaction hash and the address of the jumpgate in the terminal. You will also find the deployment parameters in a newly created JSON file in the [`deployed`](/deployed/) directory that is named `%NETWORK%-%RECIPIENT%.json`.

#### Step 4 (optional). Check your deployment.

Specify the newly deployed jumpgate address in `JUMPGATE` in `.env` and run the check script.

```bash
$ brownie run scripts/check_jumpgate.py
```

You should be able to tell whether the deployment was successful by the outputs in the terminal.

## 🕳 Bridging tokens

Before you proceed, please follow [Getting Started](#-getting-started) instructions.

The bridging of tokens is the core function of jumpgates. You can do it by running the [bridging](/scripts/bridge_tokens.py) script.

#### Step 1. Add a local account.

###### Skip this step if you have already done it in the [Deploying a jumpgate](#-deploying-a-jumpgate) section.

You can add a local account either from a private key or a keystore. If you do not have either of them, consider generating a new account. Learn more about Brownie [local accounts](https://eth-brownie.readthedocs.io/en/v1.6.4/accounts.html#managing-local-accounts).

#### Step 2. Specify environment variables.

You can do this by copying the contents of `sample.env` into `.env` and filling it out. The necessary variables are listed below,

- `DEPLOYER` - your local account id (in case of bridging the variable name is a bit misleading because bridging is permissionless and can be sent by any account with some ether);
- `NETWORK` - name of the network your jumpgate was deployed to, e.g., `mainnet`, `goerli`, `ropsten`, etc.;
- `JUMPGATE` - address of the jumpgate you want to active (you can find the list of deployed jumpgates in the [`deployed`](/deployed/) directory);

#### Step 3. Run the script

```bash
$ brownie run scripts/bridge_tokens.py
```

Upon running the script you will prompted to enter the password to your local account. After that, all the bridging parameters will be displayed in your terminal. Confirm them and enter 'y' to proceed. E.g.,
<img alt="image" src="https://user-images.githubusercontent.com/39704351/161904243-28ca16ea-71e6-40c1-90bc-2748c69bf429.png">

If all is correct, you should be able to see your transaction hash in the terminal.
