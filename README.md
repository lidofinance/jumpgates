
<div style="display: flex;">
<h1>Jumpgates
<img src="https://raw.githubusercontent.com/lidofinance/jumpgates/main/img/logo.png" width="128" align="right" />
</div>


Jumpgates facilitate cross-chain token transfers under the Lido DAO incentive programs. Although autonomous, jumpgates are meant to be part of the Easy Track Rewards Program pipeline.
  
## What is a jumpgate?

A jumpgate is a simple contract that transfers tokens via cross-chain token bridges, such Wormhole, Terra Shuttle, etc. The parameters of the transportation (such as the token, recipient, bridge) are predefined and immutable for each invididual jumpgate which makes its operation safe and permissionless. Jumpgates also provide authorized ways to recover ether, ERC20, ERC721 and ERC1155 tokens.

## Which problem do they solve?
  
Ethereum-native Lido governance is seeking to incentivize the protocol adoption in other blockchains. Jumpgates reduce operational overhead associated with routine cross-chain token transfers by providing a permissionless way to bridge tokens. 
  
## How do jumpgates work?

A jumpgate contract features a public function that transfers all of its tokens to the cross-chain recipient via a token bridge. This public function accepts no arguments because the parameters necessary for the transfer are specified at the moment of deployment.

  
Read ADR: https://hackmd.io/snwPWGqBS-ax5Ur0A5Ix5w?view

## Development

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```
