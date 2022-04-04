
  
<div style="display: flex;" align="center">
  <h1 align="center">Jumpgates</h1>
  <img src="https://raw.githubusercontent.com/lidofinance/jumpgates/main/img/logo.png" width="100" align="left" />
</div>

![solidity ^0.8.0](https://img.shields.io/badge/solidity-%5E0.8.0-lightgray)
![python ~3.8.9](https://img.shields.io/badge/python-~3.8.9-blue)
![eth_brownie 1.18.1](https://img.shields.io/badge/eth__brownie-1.18.1-brown)
![license GPL](https://img.shields.io/badge/license-GPL-green)

Jumpgates facilitate cross-chain token transfers under the Lido DAO incentive programs. Although autonomous, jumpgates are meant to be part of the Easy Track Rewards Program pipeline.
  
## About jumpgates

A jumpgate is a simple contract that transfers tokens via a cross-chain token bridge, such as Wormhole, Terra Shuttle, etc. The parameters of the transportation (the token, recipient, bridge) are predefined and immutable for each invididual jumpgate which makes its operation safe and permissionless. Jumpgates also provide permissioned ways to recover ether, ERC20, ERC721 and ERC1155 tokens.

Ethereum-native Lido governance is seeking to incentivize the protocol adoption in other blockchains. Jumpgates reduce operational overhead associated with routine cross-chain token transfers by providing a permissionless way to bridge tokens. 
  
For further details [read ADR](https://hackmd.io/snwPWGqBS-ax5Ur0A5Ix5w?view).

## Getting started
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

## Deploying a jumpgate

