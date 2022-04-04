
  
<div style="display: flex;" align="center">
  <h1 align="center">Jumpgates</h1>
  <img src="https://raw.githubusercontent.com/lidofinance/jumpgates/main/img/logo.png" width="100" align="left" />
</div>

![solidity ^0.8.0](https://img.shields.io/badge/solidity-%5E0.8.0-lightgray)
![python ~3.8.9](https://img.shields.io/badge/python-~3.8.9-blue)
![eth_brownie 1.18.1](https://img.shields.io/badge/eth__brownie-1.18.1-brown)
![license GPL](https://img.shields.io/badge/license-GPL-green)

Jumpgates facilitate cross-chain token transfers under the Lido DAO incentive programs. Although autonomous, jumpgates are meant to be part of the Easy Track Rewards Program pipeline.
  
## 🌀 About jumpgates

A jumpgate is a simple contract that transfers tokens via a cross-chain token bridge, such as Wormhole, Terra Shuttle, etc. The parameters of the transportation (the token, recipient, bridge) are predefined and immutable for each invididual jumpgate which makes its operation safe and permissionless. Jumpgates also provide permissioned ways to recover ether, ERC20, ERC721 and ERC1155 tokens.

Ethereum-native Lido governance is seeking to incentivize the protocol adoption in other blockchains. Jumpgates reduce operational overhead associated with routine cross-chain token transfers by providing a permissionless way to bridge tokens. 
  
For further details [read ADR](https://hackmd.io/snwPWGqBS-ax5Ur0A5Ix5w?view).

## 🏁 Getting started
This project uses Brownie development framework. Learn more about [Brownie](https://eth-brownie.readthedocs.io/en/stable/index.html).
### Prerequisites
- Python 3.8+

### Step 1.
Create a Python virtual environment.
```bash
$ python3 -m venv venv
```
### Step 2.
Activate the virtual environment.
```bash
$ source venv/bin/activate
```
### Step 3.
Install Python dependencies.
```bash
$ pip3 install -r requirements.txt
```
### Step 4.
Specify your Infura project id. Don't forget to replace `%YOUR-INFURA-PROJECT-ID%` below with your actual project id. Learn more about [Infura](https://infura.io/).
```bash
$ export WEB3_INFURA_PROJECT_ID=%YOUR-INFURA-PROJECT-ID% 
```

### Step 5 (optional).
Specify your Etherscan API key. Don't forget to replace `%YOUR-ETHERSCAN-TOKEN% ` below with your actual API key. Learn more about [Etherscan API](https://etherscan.io/apis).
```bash
$ export ETHERSCAN_TOKEN=%YOUR-ETHERSCAN-TOKEN% 
```

## 🚛 Deploying a jumpgate
Before you proceed, please follow [Getting Started](#getting-started) instructions.

### Step 1.
Specify environment variables required for deployment. You can do this by copying the contents of `sample.env` into `.env` and filling it out. The necessary variables are listed below,
- `PRIVATE_KEY` - your private key;
- `NETWORK` - name of the network you want to deploy a jumpgate to, e.g., `mainnet`, `goerli`, `ropsten`, etc.;
- `TOKEN` - address of the ERC20 token you want to transfer;
- `BRIDGE` - address of the Wormhole Token Bridge;
- `RECIPIENT_CHAIN` - Wormhole id of the target chain, e.g. `1` for Solana, `3` for Terra;
- `RECIPIENT` - address of the recipient;
- `ARBITER_FEE` - bridge arbiter fee, defaults to 0.

### Step 2.
Run the deploy script.
```bash
$ brownie run scripts/deploy.py
```
If you've specified all the necessary variables, they will be displayed in your terminal. Confirm them and enter 'y' to proceed. E.g.,
<img alt="image" src="https://user-images.githubusercontent.com/39704351/161552953-23b81a40-f468-4196-9c81-89ea8a5745e8.png">

If all is correct, you should be able to see your transaction hash and the address of the jumpgate in the terminal. You will also find the deployment parameters in a newly created JSON file in the root directory that is named `deployed-%NETWORK%-%RECIPIENT%.json`.

### Step 3 (optional).
Check your deployment. Specify the newly deployed jumpgate address in `JUMPGATE` in `.env` and run the check script.
```bash
$ brownie run scripts/check_jumpgate.py
```
You should be able to tell whether the deployment was successful by the outputs in the terminal.
