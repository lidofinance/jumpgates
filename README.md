<div style="display: flex;" align="center">
  <h1 align="center">Jumpgates</h1>
  <img src="https://raw.githubusercontent.com/lidofinance/jumpgates/main/img/logo.png" width="100" align="left" />
</div>

![solidity ^0.8.0](https://img.shields.io/badge/solidity-%5E0.8.0-lightgray)
![python ~3.8.9](https://img.shields.io/badge/python-~3.8.9-blue)
![eth_brownie 1.17.2](https://img.shields.io/badge/eth__brownie-1.17.2-brown)
![license GPL](https://img.shields.io/badge/license-GPL-green)

Jumpgates facilitate cross-chain token transfers under the Lido DAO incentive programs. Although autonomous, jumpgates are meant to be part of the Easy Track Rewards Program pipeline.

## 🌀 About jumpgates

A jumpgate is a simple contract that transfers tokens via a cross-chain token bridge, such as Wormhole, Terra Shuttle, etc. The parameters of the transportation (the token, recipient, bridge) are predefined and immutable for each invididual jumpgate which makes its operation safe and permissionless. Jumpgates also provide permissioned ways to recover ether, ERC20, ERC721 and ERC1155 tokens.

As Ethereum-native Lido expands other blockchains, jumpgates reduce operational overhead associated with routine cross-chain token transfers under the Lido DAO by providing a permissionless way to bridge tokens.

For further details [read ADR](https://hackmd.io/snwPWGqBS-ax5Ur0A5Ix5w?view).

## 🏁 Getting started

This project uses Brownie development framework. Learn more about [Brownie](https://eth-brownie.readthedocs.io/en/stable/index.html).

### Prerequisites

- Python 3.8+

#### Step 1. Create a Python virtual environment.

```bash
$ python3 -m venv venv
```

#### Step 2. Activate the virtual environment.

```bash
$ source venv/bin/activate
```

#### Step 3. Install Python dependencies.

```bash
$ pip3 install -r requirements.txt
```

#### Step 4. Specify your Infura project id.

Replace `%YOUR-INFURA-PROJECT-ID%` below with your actual project id. Learn more about [Infura](https://infura.io/).

```bash
$ export WEB3_INFURA_PROJECT_ID=%YOUR-INFURA-PROJECT-ID%
```

#### Step 5 (optional). Specify your Etherscan API key.

Replace `%YOUR-ETHERSCAN-TOKEN%` below with your actual API key. Learn more about [Etherscan API](https://etherscan.io/apis).

```bash
$ export ETHERSCAN_TOKEN=%YOUR-ETHERSCAN-TOKEN%
```

## 🧪 Testing a jumpgate
Before you proceed, please follow [Getting Started](#-getting-started) instructions.

To run the entire test suit, execute the following command,
```bash
$ brownie test
```

Alternatively, you can run a specific test module by specifying the path,
```bash
$ brownie test tests/test_jumpgate_unit.py
```

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

<img alt="image" src="https://user-images.githubusercontent.com/39704351/161552953-23b81a40-f468-4196-9c81-89ea8a5745e8.png">

If all is correct, you should be able to see your transaction hash and the address of the jumpgate in the terminal. You will also find the deployment parameters in a newly created JSON file in the [`deployed`](/deployed/) directory that is named `%NETWORK%-%RECIPIENT%.json`.

#### Step 4 (optional). Check your deployment.

Specify the newly deployed jumpgate address in `JUMPGATE` in `.env` and run the check script.

```bash
$ brownie run scripts/check_jumpgate.py
```

You should be able to tell whether the deployment was successful by the outputs in the terminal.
