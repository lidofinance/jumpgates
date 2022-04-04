
  
<div style="display: flex;" align="center">
  <h1 align="center">Jumpgates</h1>
  <img src="https://raw.githubusercontent.com/lidofinance/jumpgates/main/img/logo.png" width="100" align="left" />
</div>

![solidity ^0.8.0](https://img.shields.io/badge/solidity-%5E0.8.0-lightgray)
![python ~3.8.9](https://img.shields.io/badge/python-~3.8.9-blue)
![eth_brownie 1.18.1](https://img.shields.io/badge/eth__brownie-1.18.1-brown)
![license GPL](https://img.shields.io/badge/license-GPL-green)

Jumpgates facilitate cross-chain token transfers under the Lido DAO incentive programs. Although autonomous, jumpgates are meant to be part of the Easy Track Rewards Program pipeline.
  
## What are jumpgates?

A jumpgate is a simple contract that transfers tokens via a cross-chain token bridge, such as Wormhole, Terra Shuttle, etc. The parameters of the transportation (the token, recipient, bridge) are predefined and immutable for each invididual jumpgate which makes its operation safe and permissionless. Jumpgates also provide permissioned ways to recover ether, ERC20, ERC721 and ERC1155 tokens.

### Which problem do they solve?  
Ethereum-native Lido governance is seeking to incentivize the protocol adoption in other blockchains. Jumpgates reduce operational overhead associated with routine cross-chain token transfers by providing a permissionless way to bridge tokens. 
  
### How do jumpgates work?

A jumpgate contract features a public function that transfers all of its tokens to the cross-chain recipient via a token bridge. This public function accepts no arguments because the parameters necessary for the transfer are specified at the moment of deployment.

  
Read ADR: https://hackmd.io/snwPWGqBS-ax5Ur0A5Ix5w?view

## Development

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```
